import yfinance as yf

#Create a "Ticker" object for BHB
#This opbject represent the stock we want to track

bhb_stock = yf.Ticker("BHB")

#Get the stock's information.
#info gives us a Python dictionary full of data

stock_info = bhb_stock.info

#Print one piece of that info: the current market price

print(f"The current market price for BHB is: {stock_info['regularMarketPrice']}")
