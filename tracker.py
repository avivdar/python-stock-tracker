import yfinance as yf

# Ask the user for a stock ticker
#the input() function pauses the script and waits for user input

ticker_symbol = input("Enter the stock ticker symbol: ")

try:
    #create a Ticker object using the user's input
    stock = yf.Ticker(ticker_symbol)

    #Get the stock's information
    stock_info = stock.info
    #Check if the price data exits BEFORE trying to access it
    if 'regularMarketPrice' in stock_info and stock_info['regularMarketPrice'] is not None:
        price = stock_info['regularMarketPrice']
        #We also use .upper() to make the output look clean
        print(f"The current market price for {ticker_symbol.upper()} is : {price}")
    else:
        #This handles tickers that exist but have no price data
        print(f"could not find current market price data for '{ticker_symbol.upper()}.'")   
except Exception as e:
    #This handles invalid tickers or other errors
    print(f"An error occurred: {e}")