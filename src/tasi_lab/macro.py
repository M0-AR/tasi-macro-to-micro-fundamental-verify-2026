"""Macro layer — peg, rates, oil, GDP. Implements video's macro->micro order."""
from __future__ import annotations

SAR_PEG = 3.75
SAR_PEG_BAND = 0.02  # historical 3.74-3.76

def check_peg(rate: float, peg: float = SAR_PEG) -> dict:
    return {"rate": rate, "peg": peg, "dev": rate - peg,
            "inside_band": abs(rate - peg) <= 0.05,
            "verdict": "PEGGED" if abs(rate - peg) <= 0.05 else "DEVIATING"}

def real_rate(nominal_pct: float, inflation_pct: float) -> float:
    return float(nominal_pct - inflation_pct)

def rate_pass_through(us_change_bps: float, sama_change_bps: float) -> dict:
    # Under hard peg, SAMA should mirror Fed 1:1 over time.
    ratio = (sama_change_bps / us_change_bps) if us_change_bps else None
    return {"us_bps": us_change_bps, "sama_bps": sama_change_bps, "ratio": ratio,
            "mirrors": ratio is not None and 0.75 <= ratio <= 1.25}

def oil_sensitivity_hint(sector: str) -> str:
    high = {"Energy", "Materials / Petrochemicals", "Materials", "Transport / Energy logistics"}
    med = {"Banks", "Utilities", "REITs"}
    if sector in high:
        return "HIGH direct oil/margin sensitivity"
    if sector in med:
        return "MEDIUM indirect (rates, credit, real-estate channel)"
    return "LOW-MEDIUM domestic-demand sensitivity"

def macro_scorecard(gdp: float | None, non_oil: float | None, inflation: float | None,
                    repo: float | None) -> dict:
    # Simple teaching scorecard, not a forecast.
    notes = []
    if gdp is not None and gdp > 3:
        notes.append("GDP expansion supports earnings breadth.")
    if non_oil is not None and non_oil > 3.5:
        notes.append("Non-oil >3.5% consistent with Vision 2030 diversification path.")
    if inflation is not None and inflation <= 2.5:
        notes.append("Inflation anchored — preserves real returns.")
    if repo is not None and repo >= 4.0:
        notes.append("Restrictive policy: headwind for leveraged/real-estate, tailwind for bank NIM up to a point.")
    return {"inputs": {"gdp": gdp, "non_oil": non_oil, "inflation": inflation, "repo": repo},
            "notes": notes}
