"""Hidden-pattern discovery — pre-registered, OOS-tested, anti-p-hacking.
Each hypothesis has: motivation, in-sample window, OOS window, success rule.
We report ALL tests (no cherry-picking) with Bonferroni note.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

HYPOTHESES = [
    {"id": "H1", "name": "Low-P/E dispersion predicts 3M breadth",
     "rule": "Cross-sectional std of P/E in cheapest quintile vs next 63d TASI return",
     "oos_rule": "Spearman rank corr OOS > 0 with p<0.10"},
    {"id": "H2", "name": "Bank-vs-Aramco leadership rotation",
     "rule": "When banks outperform Aramco 63d, next 63d favours domestic cyclicals",
     "oos_rule": "Hit-rate OOS > 50%"},
    {"id": "H3", "name": "Rate-peg stress -> value premium",
     "rule": "SAMA repo hikes precede low-P/B outperformance (flight to book)",
     "oos_rule": "Mean spread OOS > 0"},
    {"id": "H4", "name": "Oil-beta sorting within Materials",
     "rule": "High Brent-beta petchems lead after oil spikes",
     "oos_rule": "Top-beta minus bottom-beta OOS > 0"},
    {"id": "H5", "name": "Index != market (concentration drag)",
     "rule": "Equal-weight Saudi basket vs cap-weight TASI spread widens in drawdowns",
     "oos_rule": "Spread correlation with drawdown < 0"},
]

def spearman(a: pd.Series, b: pd.Series) -> float:
    from scipy.stats import spearmanr
    c, _ = spearmanr(a.dropna(), b.dropna())
    return float(c) if c == c else 0.0

def bonferroni_note(n_tests: int, alpha: float = 0.05) -> str:
    return (f"Testing {n_tests} hypotheses: per-test alpha {alpha} -> "
            f"Bonferroni alpha {alpha/n_tests:.4f}. Report all, highlight only "
            f"Bonferroni survivors as 'strong', others as 'suggestive'.")

def evaluate_spread_oos(spread_returns: pd.Series) -> dict:
    r = spread_returns.dropna()
    if len(r) == 0:
        return {"n": 0, "verdict": "NO DATA"}
    hit = float((r > 0).mean())
    mean = float(r.mean())
    verdict = "SUPPORTIVE" if mean > 0 and hit > 0.5 else "NOT SUPPORTED"
    return {"n": int(len(r)), "mean": mean, "hit_rate": hit, "verdict": verdict}
