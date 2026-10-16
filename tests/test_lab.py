from src.tasi_lab.valuation import trailing_pe, price_to_book, graham_number, max_drawdown
from src.tasi_lab.macro import check_peg, real_rate
from src.tasi_lab.backtest import form_value_sleeve, summary_stats
import pandas as pd

def test_pe_payback():
    assert trailing_pe(100, 10) == 10.0
    assert trailing_pe(100, 20) == 5.0
    assert trailing_pe(100, 0) is None
    assert trailing_pe(100, -5) is None

def test_pb():
    assert price_to_book(31.10, 31.10) == 1.0
    assert price_to_book(13.61, 31.10) < 0.5  # Cenomi-style discount

def test_graham():
    g = graham_number(10, 31.1)
    assert g and g > 0

def test_peg():
    assert check_peg(3.75)["verdict"] == "PEGGED"
    assert check_peg(3.90)["verdict"] == "DEVIATING"

def test_value_sleeve_no_lookahead():
    snap = pd.DataFrame({"pe": [3.3, 3.5, 25.0, 5.4, 40.0], "pb": [1.2, 0.9, 3.0, 0.5, 5.0]},
                        index=["Bahri", "Rabigh", "BankA", "CementA", "Froth"])
    hold = form_value_sleeve(snap, top_n=2)
    assert hold == ["Bahri", "Rabigh"]

def test_summary():
    s = summary_stats(pd.Series([0.01, -0.005, 0.02]))
    assert s["n"] == 3 and "sharpe" in s

def test_drawdown():
    s = pd.Series([100, 110, 105, 90, 95])
    assert max_drawdown(s) < 0
