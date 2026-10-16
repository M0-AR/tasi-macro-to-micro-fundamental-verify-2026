"""Exp 04 — Valuation benchmark (formulas + public multiples; no Yahoo hammer)."""
from __future__ import annotations
import json, pathlib, datetime
from src.tasi_lab.valuation import trailing_pe, price_to_book, graham_number, earnings_yield, value_spread
OUT = pathlib.Path("evidence/04_valuation_benchmark.json")
# formula self-check (video's 100/10=10y, 100/20=5y)
checks = {"pe_100_10": trailing_pe(100,10), "pe_100_20": trailing_pe(100,20),
          "pb_Cenomi": price_to_book(13.61,31.10), "graham_10_31": graham_number(10,31.10),
          "ey_16p4": earnings_yield(16.4), "spread_ey_minus_repo": value_spread(earnings_yield(16.4),0.045)}
res = {"fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "formula_checks": checks,
 "market_table_public": {
   "TASI_PE": "16.9 (Q1 Tharaa) / 15.6 TTM (Sep Albilad) / 17.65 ex-Aramco (Sep Aljazira) / 13.43 (Oct14 Argaam)",
   "TASI_PB": "2.2 (Q1) / 2.84 (Oct14) / 2.21 (May Invesense, from 1.49 decade)",
   "cheapest_PE": "Bahri 5.2->3.31, Albabtain 6.2, Arabian Mills 7.3, Tasheel 7.5",
   "cheapest_PB": "Cenomi 0.44, Najran 0.45, Northern 0.50, Tabuk 0.52",
   "yield": "avg 3.5%; Alujain 11.1%, City Cement 9.1%, YCC 8.7%"
 },
 "lessons": {
  "book": "Book = cost minus depreciation (1m office /20y -> 0). Market 2-3x book normal for quality banks; <1x flags distress/cyclical — verify.",
  "pe": "P/E = payback years at flat earnings. Low P/E often cyclical trough (Bahri 3x) — need forward margins + oil beta.",
  "repo": "SAMA 4.5%: EY 1/16.4=6.1% minus 4.5% = +1.6% thin compensation; banks NIM tailwind then credit stress dominates.",
  "fair_value": "SNB bottom-up fair 12000 @16.1x vs 10441 Sep close => ~15% upside IF multiples normalise; Tharaa: premium reflects Vision growth bet."
 },
 "backtest_discipline": "Point-in-time ranks only, survivorship-fixed, walk-forward 63d, costs 20bps, OOS-only, Bonferroni for H1-H5. See backtest.py."}
OUT.write_text(json.dumps(res, indent=2, default=str))
print(json.dumps(res, indent=2, default=str))
print(f"Wrote {OUT}")
