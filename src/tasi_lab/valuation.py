"""Valuation primitives — P/E, P/B, fair-value framing exactly as video teaches them.
Definitions (pedagogical, then formal):
- P/E = Price / EPS (trailing). Payback years = P/E under zero-growth assumption.
- P/B = Price / BookValuePerShare. Book != market value (depreciation, historical cost).
- Fair value != book value: forward earnings + required return.
We implement point-in-time, no-lookahead versions for backtests.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

def trailing_pe(price: float, eps: float) -> float | None:
    if eps is None or eps <= 0 or price is None:
        return None
    return float(price / eps)

def payback_years(pe: float | None) -> float | None:
    return pe

def price_to_book(price: float, bvps: float) -> float | None:
    if bvps is None or bvps <= 0 or price is None:
        return None
    return float(price / bvps)

def graham_number(eps: float, bvps: float) -> float | None:
    """Classic Graham number sqrt(22.5 * EPS * BVPS) — screening upper bound, not a target."""
    if eps is None or bvps is None or eps <= 0 or bvps <= 0:
        return None
    return float((22.5 * eps * bvps) ** 0.5)

def earnings_yield(pe: float | None) -> float | None:
    if pe is None or pe == 0:
        return None
    return 1.0 / pe

def value_spread(earnings_yield_: float | None, risk_free: float | None) -> float | None:
    """Equity risk compensation vs risk-free (10Y). Positive = compensated for equity risk."""
    if earnings_yield_ is None or risk_free is None:
        return None
    return float(earnings_yield_ - risk_free)

def drawdown_from_peak(series: pd.Series) -> pd.Series:
    peak = series.cummax()
    return (series / peak - 1.0) * 100.0

def max_drawdown(series: pd.Series) -> float:
    return float(drawdown_from_peak(series).min())

def ttm_pe_from_history(prices: pd.Series, eps_ttm: float) -> pd.Series:
    return prices / eps_ttm
