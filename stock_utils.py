import os
import yfinance as yf
from typing import Any, Dict, Optional
from helper_functions import (
                            ticker_exists,
                            ask_confirmation,
                            format_market_cap,
                            color_text
                            )

def load_portfolio(filename="portfolio.txt"):
    '''
    Loads a portfolio from a text file.
    Returns a list of tickers.
    '''
    portfolio = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                #.strip() removes whitespace and newline chars
                ticker = line.strip()
                if ticker: #Make sure the line wasn't empty
                    portfolio.append(ticker)
    return portfolio


def save_portfolio(tickers, filename="portfolio.txt"):
    '''
    Saves a list of tickers to a text file, one per line.
    '''

    with open(filename, 'w') as f:
        for ticker in tickers:
            f.write(f"{ticker}\n")


def add_ticker(tickers_list, ticker_to_add):
    '''
    Adds a ticker to the list if it doesn't already exist.
    Return a status message.'''
    if ticker_exists(tickers_list,ticker_to_add):
        return f"{ticker_to_add.upper()} is already in the list."
    else:
        #If not append it
        tickers_list.append(ticker_to_add.upper())
        return f"Added {ticker_to_add.upper()}."

def remove_ticker(tickers_list, ticker_to_remove):
    '''
    Removes a ticker from the list if exists,with confirmation.
    Return a status message.
    '''
    #Find the real ticker to remove (to handle case insensitivity)
    ticker_to_remove_upper = ticker_to_remove.upper()

    if not ticker_exists(tickers_list,ticker_to_remove_upper):
        return f"{ticker_to_remove_upper} was not in your portfolio."
    
    #Ask for confirmation
    if ask_confirmation(f"Are you sure you want to remove {ticker_to_remove_upper}?"):
        #Find the item to remove
        for ticker in tickers_list:
            if ticker.upper() == ticker_to_remove_upper:
                tickers_list.remove(ticker)
                break
        return f"Removed {ticker_to_remove_upper}."
    else:
        return f"Removal of {ticker_to_remove_upper} cancelled."
    

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
    except Exception:
        #Network error or other issue
        return {"ticker" : normalized_ticker, "status" : "fail"}

    # Safely pull the core fields we need

    current_price = stock_info.get("regularMarketPrice")
    if current_price is None:
        # Ticker exists but has no usable price data
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


