import pytest
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from helper_functions import(
    ticker_exists,
    format_market_cap,
    color_text,
)


def test_ticker_case_insensitive():
    tickers = ["AAPL", "msft", "goOg"]

    assert ticker_exists(tickers, "aapl") is True
    assert ticker_exists(tickers, "MSFT") is True
    assert ticker_exists(tickers, "goog") is True
    assert ticker_exists(tickers, "TSLA") is False

def test_format_market_cap_none():
    assert format_market_cap(None) == "N/A"


def test_format_market_cap_millions_billions_trillions():

    #Millions
    assert format_market_cap(1_500_000) == "1.50M"
    #Billions
    assert format_market_cap(2_300_000_000) == "2.30B"
    #Trillions
    assert format_market_cap(5_100_000_000_000) == "5.10T"


def test_format_market_cap_small_numbers():
    #Below 1M should printed as integer without suffix
    assert format_market_cap(1234) == "1234"

def test_color_text_positive_negative_zero():
    
    text = "1.23%"

    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"

    #Positive -> green

    pos = color_text(text, 1.0)
    assert pos.startswith(GREEN)
    assert pos.endswith(RESET)
    assert text in pos

    #Negative -> red
    neg = color_text(text, -1.0)
    assert neg.startswith(RED)
    assert neg.endswith(RESET)
    assert text in neg

    #Zero -> unchanged
    zero = color_text(text, 0.0)
    assert zero == text