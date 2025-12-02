import logging
import pandas as pd
from stock_utils import (
    get_stock_data,
    load_portfolio,
    save_portfolio,
    add_ticker,
    remove_ticker,
)

logger = logging.getLogger(__name__)


def manage_portfolio(portfolio_tickers: list[str]) -> list[str]:
    """
    Handle the interactive menu for adding/removing tickers.

    Mutates and returns the portfolio_tickers list.
    """
    # Check if we loaded anything and show the user
    if portfolio_tickers:
        print("--- Welcome Back ---")
        print(f"Your current portfolio: {', '.join(portfolio_tickers)}")
    else:
        print(" --- Welcome! your portfolio is empty. ---")

    # 'add/remove' loop works whether the list is empty or not
    while True:
        print("\n--- Portfolio Management ---")
        print("1. Add a ticker")
        print("2. Remove a ticker")
        print("3. Continue to portfolio check")

        choice = input("Enter your choice (1, 2, or 3): ").strip()

        # --- choice 1: Add ---
        if choice == "1":
            ticker_to_add = input("Enter ticker to add: ").strip()
            if ticker_to_add:  # Ensure it's not empty
                message = add_ticker(portfolio_tickers, ticker_to_add)
                print(f"\n{message}")
                print(f"Current portfolio: {', '.join(portfolio_tickers)}")
            else:
                print("No ticker entered.")

        # --- choice 2: Remove ---
        elif choice == "2":
            ticker_to_remove = input("Enter ticker to remove: ").strip()
            if ticker_to_remove:  # Ensure it's not empty
                message = remove_ticker(portfolio_tickers, ticker_to_remove)
                print(f"\n{message}")
                print(f"Current portfolio: {', '.join(portfolio_tickers)}")
            else:
                print("No ticker entered.")

        # --- choice 3: Continue ---
        elif choice == "3":
            print("\nFinalizing portfolio...")
            break

        # Invalid choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    return portfolio_tickers


def check_portfolio(portfolio_tickers: list[str]) -> None:
    """
    Save the portfolio and check current prices for all tickers.
    Prints a report and summary.
    """
    # SAVE AND CHECK PRICES
    save_portfolio(portfolio_tickers)
    print(f"\nPortfolio saved. You have {len(portfolio_tickers)} stocks")
    print("--- Checking Your Portfolio ---")

    if not portfolio_tickers:
        print("Your portfolio is empty. No stocks to check.")
        return

    # Create empty lists to hold our results
    successful_results: list[dict] = []
    failed_results: list[dict] = []

    # Loop and sort data into the two lists
    for ticker in portfolio_tickers:
        data = get_stock_data(ticker)

        if data["status"] == "success":
            successful_results.append(data)
        else:
            failed_results.append(data)

    # --- Display success table ---
    if successful_results:
        print("\n--- Portfolio Report ---")
        df = pd.DataFrame(successful_results)
        df = df.set_index("ticker")
        df = df[["name", "price", "change_pct_display", "mkt_cap"]]
        df.columns = ["Name", "Price", "Change %", "Mkt Cap"]
        print(df)
    else:
        print("No successful stock data to display.")

    # --- Display errors / missing data ---
    if failed_results:
        print("\n--- Failed or Missing Data ---")
        for item in failed_results:
            if item["status"] == "no_price_data":
                print(f"- {item['ticker']}: Price data not found.")
            else:  # 'fail'
                print(f"- {item['ticker']}: could not retrieve data.")

    # --- Display final summary count ---
    total_count = len(portfolio_tickers)
    failed_count = len(failed_results)

    print("\n-----------------------")
    print(f"Summary: Failed {failed_count} out of {total_count} stocks.")
    print("-------------------------")


def main() -> None:
    """
    Entry point for the portfolio tracker CLI.
    """
    # 1. Load initial portfolio
    portfolio_tickers = load_portfolio()

    # 2. Let the user manage the portfolio interactively
    portfolio_tickers = manage_portfolio(portfolio_tickers)

    # 3. Save and check prices
    check_portfolio(portfolio_tickers)


if __name__ == "__main__":
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    main()
