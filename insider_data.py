from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, date
from typing import Literal, Optional, List

# ---- Types for clarity -------------------------------------------------------

TransactionType = Literal["Buy", "Sell"]
InsiderRole = Literal["CEO", "CFO", "Director", "Officer", "10% Owner" , "Other"]


# ---- Core domain model -------------------------------------------------------

@dataclass
class InsiderTrade:
    """
    Represents a single insider transaction (one row in an insider report).
    This is our *internal* canonical format, independent of any website/API.
    Any scraper or data source should convert into this shape.
    """

    tikcer: str

    insider_name: str
    role: InsiderRole

    trade_date: date  # when the trade occurred
    filed_date: Optional[date] # when it was filed with the SEC

    transaction_type: TransactionType # Buy or Sell

    shares: int  # number of shares traded
    price: float # price per share
    value_usd:float  #total value = shares * price
    ownership_after: Optional[int] = None # shares owned after the trade
    source: Optional[str] = None # e.g. "OpenInsider", "SEC", etc.
    link: Optional[str] = None #URL to the original filing/page

    @property
    def is_buy(self) -> bool:
        return self.transaction_type =="Buy"
    
    @property
    def is_sell(self) -> bool:
        return self.transaction_type == "Sell"
    
    @property
    def trade_datetime_key(self) -> datetime:
        """
        A helper property that gives us a datetime-like key we can use
        for sorting by "most recent" trades. If we only know the date,
        we treat it as midnight that day.
        """
        return datetime.combine(self.trade_date,datetime.min.time())
    
# ---- Interface for data fetching (to be implemented later) -------------------
    
    def fetch_insider_trades_for_ticker(ticker: str) -> List[InsiderTrade]:
        """
        Fetch insider trades for a single ticker from one or more data sources.

        This is the main entry point the rest of the app will use.

        Later implementation (not now):
            - Normalize ticker (upper)
            - Scrape e.g. OpenInsider / SEC / other
            - Parse HTML/JSON into InsiderTrade objects
            - Sort by trade_date descending
        """

        raise NotImplementedError("fetch_insider_trades_for_ticker is not implemented yet.")
    

    def fetch_recent_insider_buys(limit: int = 50) -> List[InsiderTrade]:
        """
        Fetch a list of recent insider BUY transactions across many tickers.

        Later implementation:
            - Scrape some 'latest insider buys' page
            - Filter to 'Buy' rows
            - Limit to `limit`
        """

        raise NotImplementedError("fetch_recent_insider_buys is not implemented yet.")
    
# ---- Interface for scoring / signals (logic, not data source) ----------------

    def compute_insider_score(trades: list[InsiderTrade]) -> float:
        """
        Compute a numeric 'insider score' for a list of trades on a single ticker.

        High-level idea (for later):
            - Recent large BUYS -> positive score
            - Multiple insiders buying in a short window -> more positive
            - CEO/CFO buying -> heavier weight than Director
            - Recent large SELLS -> negative score
            - Very old trades -> small or zero impact

        For now, we just define the interface. We’ll implement the logic later.
        """

        raise NotImplementedError("compute_insider_score is not implemented yet.")
    
    