import pytest
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from stock_utils import (
    _compute_change_percent,
    _format_change_colored,
)



def test_compute_change_percent_normal():
    result = _compute_change_percent(current_price = 110.0, prev_close = 100.0)
    #10% increase
    assert result == pytest.approx(10.0)

def test_compute_change_percent_no_prev_close():
    result_none = _compute_change_percent(current_price = 110.0, prev_close = None)
    assert result_none == 0.0

    # 0 -> should safely give 0.0
    result_zero = _compute_change_percent(current_price = 110.0, prev_close = 0.0)
    assert result_zero == 0.0


def test_format_change_colored_wraps_sign_and_two_decimals():
    #We don't test colors here, just the formatting

    colored = _format_change_colored(10.0)
    #It should contain '+10.00%' somewhere inside (with ANSI codes around)
    assert "+10.00%" in colored

    colored_neg = _format_change_colored(-5.1234)
    #Rounded to two decimals and with a sign
    assert "-5.12%" in colored_neg