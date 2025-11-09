import os
import yfinance as yf
from helper_functions import ticker_exists, ask_confirmation

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
        return f"{ticker_to_add.upper()}"

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
    

def get_stock_data(ticker_symbol):


    '''
    Gets stock data for a single ticker and return it as a dictionary.
    '''
    try:
        #create a Ticker object using the user's input
        stock = yf.Ticker(ticker_symbol)
        stock_info = stock.info

        #Check if the core data exists
        if 'regularMarketPrice' in stock_info and stock_info['regularMarketPrice'] is not None:
            #We found the data, we build a dictionary to return
            data = {
                'ticker' : ticker_symbol.upper(),
                'price' : stock_info['regularMarketPrice'],
                'name' : stock_info.get('shortName', 'N/A'), # .get() is safer
                'status' : 'success'
            }
            return data
        else:
            #This handles tickers that exist but have no price data
            return {'ticker' : ticker_symbol.upper(), 'status' : 'no_price_data'}
           
    except Exception as e:
        #The ticker is invalid or a network error occurred
        #print(f"DEBUG: Error for {ticker_symbol} : {e}") #Debug line
        return {'ticker' : ticker_symbol.upper(), 'status' : 'fail'}
    


