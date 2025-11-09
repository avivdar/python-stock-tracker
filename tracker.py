from stock_utils import(
     get_stock_data,
     load_portfolio,
     save_portfolio,
     add_ticker,
     remove_ticker
)

#Load the portfolio first
portfolio_tickers = load_portfolio()

#Check if we loaded anything and show the user
if len(portfolio_tickers) > 0:
    print("--- Welcome Back ---")
    print(f"Your current portfolio: {', '.join(portfolio_tickers)}")
else:
    print(" --- Welcome! your portfolio is empty. ---")


#'add' loop works if list is empty or not
while True:
    while True:
        print("\n--- Portfolio Managment ---")
        print("1. Add a ticker")
        print("2. Remove a ticker")
        print("3. continue to portfolio check")

        choice = input("Enter youe choice(1,2,or 3):").strip()

        #--- choice 1: Add ---
        if choice == '1':
            ticker_to_add = input("Enter ticker to add:").strip()
            if ticker_to_add: #Ensure it's not empty
                message = add_ticker(portfolio_tickers,ticker_to_add)
                print(f"\n{message}")
                print(f"Current portfolio: {', '.join(portfolio_tickers)}")
            else:
                print("No ticker enteres.")
        # -- choice 2: Remove ---
        elif choice == '2':
            ticker_to_remove = input("Enter ticker to remove: ").strip()
            if ticker_to_remove: #Ensure it's not empty
                message = remove_ticker(portfolio_tickers,ticker_to_remove)
                print(f"\n{message}")
                print(f"Current portfolio: {', '.join(portfolio_tickers)}")
            else:
                print("No ticker entered.")

        # -- choice 3: Continue ---
        elif choice == '3':
            print("\nFinalizing portfolio...")
            break
        # Invalid choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


#SAVE AND CHECK PRICES
save_portfolio(portfolio_tickers)
print(f"\nPortfolio saved. You have {len(portfolio_tickers)} stocks")
print("--- Checking Your Portfolio ---")

#Now we check each stock in the portfolio
if len(portfolio_tickers) > 0:
    for ticker in portfolio_tickers:
        data = get_stock_data(ticker)

        if data['status'] == 'success':
            print(f"{data['ticker']} ({data['name']}): ${data['price']}")
        elif data['status'] == 'no_price_data':
            print(f"{data['ticker']}: Price data not found.")
        elif data['status'] == 'fail':
            print(f"{data['ticker']} : could not retrieve data.")

    print("--- End of Portfolio ---")
else:
    print("Your portfolio is empty. Nothing to check.")
