import logging
from typing import List, Dict, Any

from stock_utils import (
    get_stock_data,
    Portfolio,
)

logger = logging.getLogger(__name__)

def print_portfolio_table(successful_results: List[Dict[str, Any]]) -> None:
    """
    Print a simple, aligned portfolio table without relying on pandas' default
    console formatting (which can look odd in some terminals).
    """
    if not successful_results:
        print("No successful stock data to display.")
        return

    # Header
    header = f"{'Ticker':<8} {'Name':<28} {'Price':>10} {'Change %':>9} {'Mkt Cap':>10}"
    print(header)
    print("-" * len(header))

    # Rows
    for item in successful_results:
        ticker = item.get("ticker", "")
        name = item.get("name", "")[:27]  # truncate long names
        price = item.get("price", 0.0)
        # Use the raw numeric change for alignment
        change_raw = item.get("change_pct_raw", 0.0)
        change_str = f"{change_raw:+.2f}%"
        mkt_cap = item.get("mkt_cap", "")
        
        print(
            f"{ticker:<8} {name:<28} {price:>10.2f} {change_str:>9} {mkt_cap:>10}"
        )


def manage_portfolio(portfolio: Portfolio) -> Portfolio:
    """
    Handle the interactive menu for adding/removing tickers.

    Mutates and returns the same Portfolio object.
    """
    # Check if we loaded anything and show the user
    if portfolio.tickers:
        print("--- Welcome Back ---")
        print(f"Your current portfolio: {', '.join(portfolio.tickers)}")
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
                message = portfolio.add(ticker_to_add)
                print(f"\n{message}")
                print(f"Current portfolio: {', '.join(portfolio.tickers)}")
            else:
                print("No ticker entered.")

        # --- choice 2: Remove ---
        elif choice == "2":
            ticker_to_remove = input("Enter ticker to remove: ").strip()
            if ticker_to_remove:  # Ensure it's not empty
                message = portfolio.remove(ticker_to_remove)
                print(f"\n{message}")
                print(f"Current portfolio: {', '.join(portfolio.tickers)}")
            else:
                print("No ticker entered.")

        # --- choice 3: Continue ---
        elif choice == "3":
            print("\nFinalizing portfolio...")
            break

        # Invalid choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    return portfolio


def check_portfolio(portfolio: Portfolio) -> None:
    """
    Save the portfolio and check current prices for all tickers.
    Prints a report and summary.
    """
    # SAVE AND CHECK PRICES
    portfolio.save()
    print(f"\nPortfolio saved. You have {len(portfolio)} stocks")
    print("--- Checking Your Portfolio ---")

    if len(portfolio) == 0:
        print("Your portfolio is empty. No stocks to check.")
        return

    # Create empty lists to hold our results
    successful_results: list[dict[str, Any]] = []
    failed_results: list[dict[str, Any]] = []

    # Loop and sort data into the two lists
    for ticker in portfolio:
        data = get_stock_data(ticker)

        if data["status"] == "success":
            successful_results.append(data)
        else:
            failed_results.append(data)

    # --- Display success table ---
    if successful_results:
        print("\n--- Portfolio Report ---")
        print_portfolio_table(successful_results)
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
    total_count = len(portfolio)
    failed_count = len(failed_results)

    print("\n-----------------------")
    print(f"Summary: Failed {failed_count} out of {total_count} stocks.")
    print("-------------------------")


def main() -> None:
    """
    Entry point for the portfolio tracker CLI.
    """
    # 1. Load initial portfolio
    portfolio = Portfolio.load()

    # 2. Let the user manage the portfolio interactively
    portfolio = manage_portfolio(portfolio)

    # 3. Save and check prices
    check_portfolio(portfolio)

if __name__ == "__main__":
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    main()
