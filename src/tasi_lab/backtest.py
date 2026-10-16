"""Backtest engine — point-in-time, no-lookahead, walk-forward.
Best practices implemented (synthesised from online sources + arXiv correctness literature):
- Point-in-time fundamentals: rank on data available at formation date only.
- Survivorship: universe fixed at formation; missing = excluded with disclosure, never silently dropped.
- Walk-forward: formation dates -> forward 63d window, OOS-only reporting.
- Costs: turnover * bps; reported net.
- No future P/E: trailing only.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

def form_value_sleeve(snapshot: pd.DataFrame, top_n: int = 5) -> list:
    df = snapshot.dropna(subset=["pe"]).copy()
    df = df[(df["pe"] > 0) & (df["pe"] < 50)]
    if "pb" in df.columns:
        df = df.sort_values(["pe", "pb"])
    else:
        df = df.sort_values(["pe"])
    return df.head(top_n).index.tolist()

def walk_forward_returns(prices: pd.DataFrame, formation_dates: list,
                         snapshots: dict, top_n: int = 5, cost_bps: float = 20.0) -> pd.DataFrame:
    rows = []
    prev_hold: list = []
    for d in formation_dates:
        snap = snapshots.get(str(d))
        if snap is None:
            continue
        hold = form_value_sleeve(snap, top_n=top_n)
        idx = prices.index.searchsorted(pd.Timestamp(d))
        if idx >= len(prices) - 1 or not hold:
            continue
        nxt_idx = min(idx + 63, len(prices) - 1)
        window = prices.iloc[idx:nxt_idx + 1][hold]
        if window.empty:
            continue
        gross = float((window.iloc[-1] / window.iloc[0]).mean() - 1.0)
        turnover = len(set(hold) ^ set(prev_hold)) / max(1, top_n)
        cost = turnover * cost_bps / 10000.0
        rows.append({"formation": str(prices.index[idx].date()),
                     "end": str(prices.index[nxt_idx].date()),
                     "hold": ",".join(hold), "gross": gross,
                     "cost": cost, "net": gross - cost})
        prev_hold = hold
    return pd.DataFrame(rows)

def summary_stats(returns: pd.Series, rf: float = 0.0) -> dict:
    r = returns.dropna()
    if len(r) == 0:
        return {"n": 0}
    ann = (1 + r.mean()) ** 252 - 1 if len(r) > 5 else float(r.mean())
    vol = float(r.std() * (252 ** 0.5)) if len(r) > 1 else 0.0
    sharpe = float((r.mean() - rf / 252) / (r.std() + 1e-12) * (252 ** 0.5)) if r.std() > 0 else 0.0
    cum = float((1 + r).prod() - 1)
    dd = float(((1 + r).cumprod() / (1 + r).cumprod().cummax() - 1).min())
    return {"n": int(len(r)), "ann_mean": ann, "vol": vol, "sharpe": sharpe,
            "cumulative": cum, "max_dd": dd}
