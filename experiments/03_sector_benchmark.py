"""Exp 03 — Sector benchmark (Yahoo-optional; public reports primary)."""
from __future__ import annotations
import json, pathlib, datetime
OUT = pathlib.Path("evidence/03_sector_benchmark.json")
res = {"fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "method": "Cap-weight illusion test via public Sep-2026 reports (Yahoo rate-limited 429 on 2026-10-16; honest fallback).",
 "inputs": {
   "TASI_Sep30_2026": 10441, "MoM": "-6.2%", "YTD_note": "-0.5% YTD (Albilad) vs -6.4% YoY peer rank (Tharaa)",
   "value_traded_Sep": "SAR 79.2bn, avg 3.8bn/day, -29.6% MoM",
   "sectors_all_down": "21/21 down; Media -14.9%, Consumer Durables -12.8%",
   "weights_May2026": {"Financials": 40.45, "Materials": 15.05, "Energy": 12.64},
   "contributors_Jul": "SNB+HMG +53.9pts vs AlRajhi+Alinma -96.1pts (concentration proof)",
   "contributors_Sep": "Bahri+ANB +8.9pts vs AlRajhi+Aramco -136.2pts"
 },
 "concentration_verdict": "CONFIRMED: 2 heavyweights can erase 136pts — index != breadth. Video CIB analogy holds for TASI.",
 "rotation_map": [
   "Early recovery/liquidity -> Banks (NIM tailwind to a point)",
   "Commodity margin expansion -> Energy/Materials (oil, product margins)",
   "Domestic broadening -> Telecom/Health/Consumer/Industrials (Vision 2030 non-oil)",
   "Policy easing -> REITs/Real Estate (rate-sensitive; SAMA 4.5% = headwind now)"
 ],
 "H5_pretest": "Equal-weight would have trailed cap-weight cushion in Sep drawdown (heavyweights drove index) — needs daily PIT panel for formal test; pre-registered in 05."}
OUT.write_text(json.dumps(res, indent=2, default=str))
print(json.dumps(res, indent=2, default=str))
print(f"Wrote {OUT}")
