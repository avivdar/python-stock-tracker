

def ticker_exists(tickers_list, ticker):
    '''
    Checks if a ticker already exists in a lists,
    case insensitive.
    '''
    return any(existing_ticker.upper() == ticker.upper() for existing_ticker in tickers_list)\


def ask_confirmation(prompt):
    '''
    Asks the user a Yes/No question and return True for Yes
    and False for No.
    '''
    while True:
        choice = input(f"{prompt} (y/n):").strip().lower()
        if choice == 'y':
            return True
        if choice == 'n':
            return False
        print("Invalid input. Please enter 'y' or 'n'.")