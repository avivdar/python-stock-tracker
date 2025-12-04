import os
import re
import json
import logging
import yfinance as yf
from datetime import datetime
from typing import Any, Dict, Optional
from helper_functions import (
                            ticker_exists,
                            ask_confirmation,
                            format_market_cap,
                            color_text
                            )


logger = logging.getLogger(__name__)

class Portfolio:
    """
    Represent a portfolio of stock tickers, with load/save/add/remove
    operation and a default JSON backing file.
    """

    def __init__(self,tickers: Optional[list[str]] = None, filename: str = "portfolio.json") -> None:
        self.tickers: list[str] = tickers or []
        self.filename: str = filename

    def __len__(self) -> int:
        return len(self.tickers)

    def __iter__(self):
        return iter(self.tickers)

    def __repr__(self) -> str:
        return f"Portfolio(tickers={self.tickers!r}, filename={self.filename!r})"

    # --------- Persistence ---------

    @classmethod
    def load(cls, filename: str = "portfolio.json") -> "Portfolio":
            """
            Load a portfolio from JSON if exists,
            otherwise create empty.
            """
            #JSON path
            if os.path.exists(filename):
                try:
                    with open(filename, "r",encoding="utf-8") as f:
                        data = json.load(f)
                    tickers = data.get("tickers", [])

                    #normalize and validate tickers
                    raw_portfolio = [str(t).strip().upper() for t in tickers if str(t).strip()]
                    valid_ticker_pattern = re.compile(r"^[A-Z0-9\.\-]+$")
                    cleaned = [t for t in raw_portfolio if valid_ticker_pattern.match(t)]


                    dropped = len(raw_portfolio) - len(cleaned)
                    if dropped > 0:
                        logger.warning(
                            "Dropped %d invalid tickers from %s when loading JSON.",
                            dropped,
                            filename,
                        )
                    logger.info("Loaded %d tickers from %s", len(cleaned), filename)
                    return cls(cleaned, filename=filename)
                except Exception:
                    logger.exception("Failed to load portfolio from %s", filename)
                    return cls([], filename=filename)

            legacy_text = "portfolio.txt"
            if os.path.exists(legacy_text):
                tickers: list[str] = []
                try:
                    with open(legacy_text, "r", encoding="utf-8") as f:
                        for line in f:
                            ticker = line.strip()
                            if ticker:
                                tickers.append(ticker.upper())
                    logger.info(
                        "Loaded %d tickers from legacy %s, will save as JSON next time.",
                        len(tickers),
                        legacy_text,
                    )
                    return cls(tickers, filename = filename)
                except Exception:
                    logger.exception("Failed to load legacy portfolio from %s", legacy_text)
                    return cls([], filename = filename)

    def save(self) -> None:
        """
        Save the portfolio to JSON file.
        """
        clean_tickers = [t.strip().upper() for t in self.tickers if t.strip()]
        data = {
            "tickers": clean_tickers,
            "updated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        }
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info("Saved %d tickers to %s", len(clean_tickers), self.filename)
        except Exception:
            logger.exception("Failed to save portfolio to %s", self.filename)

    # --------- Operations ---------

    def add(self, ticker : str) -> str:
        """
        Add a ticker if it doesn't already exist.
        Return a user-friendly status message.
        """
        ticker = ticker.strip().upper()
        if not ticker:
            return "No ticker entered."

        if ticker_exists(self.tickers, ticker):
            return f"{ticker} is already in the portfolio."
        
        self.tickers.append(ticker)
        return f"Added {ticker}"
    
    def remove(self,ticker: str) -> str:
        """
        Remove a ticker from the portfolio, with confirmation.
        Return a message to user.
        """
        ticker = ticker.strip().upper()
        if not ticker_exists(self.tickers, ticker):
            return f"{ticker} is not in the portfolio." 
        
        if ask_confirmation(f"Are you sure you want to remove {ticker}? (Y/N)"):
            self.tickers.remove(ticker)
            return f"Removed {ticker}."
        else:
            return f"Did not remove {ticker}"


def load_portfolio(filename: str = "portfolio.json") -> list[str]:
    """
     Backwards-compatible wrapper teturning a list of tickers.
    """
    return load_portfolio(filename=filename).tickers

def save_portfolio(tickers: list[str], filename: str = "portfolio.json") -> None:
    """
    Backwards-compatible wrapper saving a list of tickers
    """
    portfolio = Portfolio(tickers, filename=filename)
    portfolio.save()

def add_ticker(tickers: list[str],ticker: str) ->str:
    """
    Backwards-comtible wrapper to add a ticker to a raw list.
    Mutates the given list.
    """
    portfolio = Portfolio(tickers)
    return portfolio.add(ticker)
    

def remove_ticker(tickers: list[str], ticker: str) -> str:
    '''
    Backwards-compatible wrapper to remove a ticker from a raw list.
    Mutates the given list.
    '''
    portfolio = Portfolio(tickers)
    return portfolio.remove(ticker)

    
    

def _compute_change_percent(current_price: float, prev_close: Optional[float]) -> float:
    '''
    Compute percentage change between current and previous close.
    Return 0.0 safely if prev_close is None or 0.
    '''
    if prev_close is None or prev_close == 0:
        return 0.0
    return (current_price - prev_close) / prev_close * 100.0

def _format_change_colored(change_percent: float) -> str:
    '''
    Build the formatted, colored percentage string(e.g '+1.23%')
    whithput touching any yfinance objects.
    '''
    change_str = f"{change_percent:+.2f}%"
    return color_text(change_str, change_percent)

def get_stock_data(ticker_symbol: str) -> Dict[str, Any]:


    """
    Gets stock data for a single ticker and return it as a dictionary.
    - Normalize the ticker symbol
    - Fetch raw data safely from yfinance
    - Compute change %
    - Format fields for display
    - Return a dict with a 'status' field describing success/failure
    """

    #Normalize ticker symbol
    normalized_ticker = ticker_symbol.strip().upper()
    if not normalized_ticker:
        #nothing to look up
        return {"ticker": "", "status": "fail"}
    
    try:
        #create a Ticker object using the user's input
        stock = yf.Ticker(normalized_ticker)
        stock_info = stock.info
    except Exception as e:
        #Network error or other issue
        logger.exception("Error fetching data for %s", normalized_ticker)
        return {"ticker" : normalized_ticker, "status" : "fail"}

    # Safely pull the core fields we need

    current_price = stock_info.get("regularMarketPrice")
    if current_price is None:
        # Ticker exists but has no usable price data
        logger.warning("No price data for %s", normalized_ticker)
        return {"ticker": normalized_ticker, "status": "no_price_data"}
    
    prev_close = stock_info.get("regularMarketPreviousClose")
    market_cap_raw = stock_info.get("marketCap")

    # Compute change % using our helper
    change_percent = _compute_change_percent(current_price, prev_close)

    # Format colored change string using our helper
    colored_change = _format_change_colored(change_percent)

    # Build the final data dict in one place
    data: Dict[str, Any] = {
        "ticker": normalized_ticker,
        "name": stock_info.get("shortName", "N/A"),
        "price": current_price,
        "change_pct_raw": change_percent,
        "change_pct_display":colored_change, 
        "mkt_cap": format_market_cap(market_cap_raw),
        "status": "success",
    }
    return data


