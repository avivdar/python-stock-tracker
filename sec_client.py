from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Dict, Any

import requests

# ---- Constants ---------------------------------------------------------------

SEC_HEADERS = {
    "User-Agent": "Aviv Dar avivzeevdar@gmail.com",  
    "Accept-Encoding": "gzip, deflate",
    "Host": "www.sec.gov",
}

COMPANY_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SUBMISSIONS_URL_TEMPLATE = "https://data.sec.gov/submissions/CIK{cik}.json"

# cache the ticker mapping locally so we don't re-download every time
CACHE_DIR = Path(".sec_cache")
CACHE_DIR.mkdir(exist_ok=True)
TICKERS_CACHE_FILE = CACHE_DIR / "company_tickers.json"

# ---- Helper: download or load company_tickers.json --------------------------

def _load_company_tickers() -> Dict[str, Any]:
    """
    Load the SEC company_tickers.json file, with a simple local cache.
    """
    # Use cache if exists
    if TICKERS_CACHE_FILE.exists():
        with open(TICKERS_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    # Otherwise download from SEC
    try:
        resp = requests.get(COMPANY_TICKERS_URL, headers=SEC_HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            "Could not download SEC company_tickers.json. "
            "Check your internet connection, DNS, VPN, or try adding a cached file "
            "to .sec_cache/company_tickers.json."
        ) from e

    data = resp.json()

    with open(TICKERS_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

    return data


# ---- Public: ticker -> CIK ---------------------------------------------------

def get_cik_for_ticker(ticker: str) -> Optional[str]:
    """
    Given a stock ticker (e.g. "AAPL"), return the corresponding SEC CIK string
    (e.g. "0000320193"). Returns None if not found.
    """
    ticker = ticker.strip().upper()
    if not ticker:
        return None
    
    data = _load_company_tickers()

    for entry in data.values():
        if entry.get("ticker", "").upper() == ticker:
            cik_int = int(entry["cik_str"])
            cik_str = f"{cik_int:010d}" # zero-padded to 10 digits
            return cik_str
    
    return None

# ---- Public: CIK -> submissions JSON ----------------------------------------


def fetch_submissions_json(cik: str) -> Dict[str, Any]:
    """
    Fetch the submissions JSON for a given 10-digit CIK string.
    Raises requests.HTTPError on failure.
    """

    cik = cik.strip()
    if not cik or not cik.isdigit():
        raise ValueError(f"Invalid cik: {cik!r}")
    
    if len(cik) < 10:
        raise ValueError(f"CIK must be at least 10 digit: (got {len(cik)}:) {cik!r}")
    
    url = SUBMISSIONS_URL_TEMPLATE.format(cik=cik)
    resp = requests.get(url, headers=SEC_HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()

# ---- Convenience: ticker -> submissions JSON --------------------------------

def fetch_submissions_for_ticker(ticker:str) -> Dict[str, Any]:
    """
    Convenience helper: resolve ticker to CIK, then fetch submissions JSON.
    """

    cik = get_cik_for_ticker(ticker)
    if cik is None:
        raise ValueError(f"Unknown ticker (no CIK found): {ticker!r}")

    return fetch_submissions_json(cik)