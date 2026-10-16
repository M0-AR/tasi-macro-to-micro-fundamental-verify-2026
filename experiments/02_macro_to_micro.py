"""Exp 02 — Macro-to-Micro pipeline (resilient: 1 Yahoo call max, WB primary, snapshots fallback)."""
from __future__ import annotations
import json, pathlib, datetime
from src.tasi_lab.config import SAUDI_TICKERS
from src.tasi_lab.data_fetcher import fetch_worldbank_gdp
from src.tasi_lab.macro import macro_scorecard, check_peg

OUT = pathlib.Path("evidence/02_macro_to_micro.json")
res = {"fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "macro": {}, "sectors": {}, "companies_snapshot": []}
try:
    series, prov = fetch_worldbank_gdp()
    res["macro"]["worldbank_gdp_SAU"] = series
    res["macro"]["prov_wb"] = prov
except Exception as e:
    res["macro"]["worldbank_error"] = str(e)[:300]
    # hard fallback from live probe earlier (verified 2026-10-16)
    res["macro"]["worldbank_gdp_SAU"] = {"2024": 2.64893068308965, "2025": 4.50246560191663}

res["macro"]["peg_check"] = check_peg(3.75)
res["macro"]["SAMA_Sep16_2026"] = {"repo": 4.5, "reverse": 4.0, "source": "SAMA N267877 + SPA + Arab News"}
res["macro"]["IMF_2026_ArtIV"] = {"GDP_2025": 4.6, "non_oil_to_2027": "~4%", "inflation": "<2%",
  "source": "IMF 2026 Article IV press release"}
res["macro"]["scorecard"] = macro_scorecard(gdp=4.5, non_oil=4.2, inflation=2.0, repo=4.5)
res["sectors"]["prior_weights_May2026_Invesense"] = \
    {"Financials": 40.45, "Materials": 15.05, "Energy": 12.64, "Others": 31.86,
     "top4_banks": 30.66, "Aramco": 11.4, "AlRajhi": 13.92,
     "note": "Banks 4 largest > Energy; TASI is a bank trade with oil hedge. Matches video concentration warning."}
res["sectors"]["Sep2026_trading"] = {"Banks+Materials_share_value_traded": "38.2%",
  "source": "Aljazira Sep-2026 review"}

# Public valuation snapshot (no Yahoo hammering): Sep/Oct 2026 reports
res["companies_snapshot"] = [
  {"symbol": "Bahri", "pe": "5.2 (Sep) / 3.31 (Oct14)", "note": "lowest P/E TTM"},
  {"symbol": "AlBabtain", "pe": "6.2 (Sep) / 5.46 recurring", "note": "2nd cheapest"},
  {"symbol": "Cenomi Centers", "pb": 0.44, "price": 13.61, "bvps": 31.10, "note": "lowest P/B"},
  {"symbol": "Najran Cement", "pb": 0.45, "note": "distress/cyclical flag"},
  {"symbol": "TASI", "pe": "15.6 TTM (Albilad Sep) / 17.65 ex-Aramco (Aljazira) / 13.43 (Argaam Oct14)",
   "pb": "2.84 (Argaam) / 2.2 (Tharaa Q1)", "div_yield": "3.5% avg; Alujain 11.1%, City Cement 9.1%"}
]
res["value_screen_lesson"] = "Cheapest P/E = Bahri/PetroRabigh (cyclical trough); cheapest P/B = Cenomi/Cements (verify, don't buy blindly)."
OUT.write_text(json.dumps(res, indent=2, default=str))
print(json.dumps(res, indent=2, default=str))
print(f"Wrote {OUT}")
