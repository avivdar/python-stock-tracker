from stock_utils import check_price

#Start with an empty list
portfolio_tickers = []

print("--- Build your Portfolio ---")
print("Enter stock tickers one by one. Press Enter to finish.")

#A while loop to get user input
while True:
    #Ask for ticker
    ticker_symbol = input("Add ticker: ")

    #check for the "stop signal" (empty string)
    if ticker_symbol == "":
        break #Exit the while loop

    #Add the ticker to our list
    #.upper() cleans the input
    portfolio_tickers.append(ticker_symbol)

print(f"\nPortfolio created. You have {len(portfolio_tickers)} stocks.")
print("--- Checking Your Portfolio ---")

#Check if the list has anything in it befor running
if len(portfolio_tickers) > 0:
    for ticker in portfolio_tickers:
        check_price(ticker)

    print("--- End of Report ---")
else:
    print("Your portfolio is empty. Nothing to check.")