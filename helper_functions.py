

def ticker_exists(tickers_list, ticker):
    '''
    Checks if a ticker already exists in a lists,
    case insensitive.
    '''
    return any(existing_ticker.upper() == ticker.upper() for existing_ticker in tickers_list)


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

def format_market_cap(value):
    '''
    Converts a large market cap number into a human-readable string.
    return N/A if value is None.
    '''

    if value is None:
        return 'N/A'
    elif value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T" #Trillions
    elif value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B" #Billions
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M" #Millions
    else:
       return f"{value:.0f}"

def color_text(text, value):
    '''
    Wraps text in ANSI coloer codes based on the value.
    green if value positive, 
    red if negetive
    '''

    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    if value > 0:
        return f"{GREEN}{text}{RESET}"
    elif value < 0:
        return f"{RED}{text}{RESET}"
    else:
        return text