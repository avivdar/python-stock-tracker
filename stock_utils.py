import yfinance as yf

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