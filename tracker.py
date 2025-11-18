
import pandas as pd
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
        print("\n--- Portfolio Managment ---")
        print("1. Add a ticker")
        print("2. Remove a ticker")
        print("3. continue to portfolio check")

        choice = input("Enter your choice(1,2,or 3):").strip()

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

if len(portfolio_tickers) > 0:

    #Create empty lists to hold our results
    successful_results = []
    failed_results = []

    #loop and sort data into the two lists
    for ticker in portfolio_tickers:
        data = get_stock_data(ticker)

        if data['status'] == 'success':
            successful_results.append(data)
        else:
            failed_results.append(data)
    # --- Display success table ---
    if successful_results:
        print("\n--- Portfolio Report ---")

        #convert list of dictionaries to a Pandas DataFrame
        df = pd.DataFrame(successful_results)

        #set 'ticker' as the index (row labels)
        df = df.set_index('ticker')

        #Select and order our columns
        df = df[['name','price']]

        #Print the final,formatted table
        print(df)
        #--- Display failed tickers ---
    if failed_results:
        print("\n--- Failed tickers ---")
        for item in failed_results:
            if item['status'] == 'no_price_data':
                print(f"- {item['ticker']}: Price data not found.")
            else: #fail
                print(f"- {item['ticker']}: could not retrieve data.")
    
    #--- Display final summary count ---\
    total_count = len(portfolio_tickers)
    failed_count = len(failed_results)

    print("\n-----------------------")
    print(f"Summary: Failed {failed_count} out of {total_count} stocks.")
    print("-------------------------")

else:
    print("Your portfolio is empty. No stocks to check.")
