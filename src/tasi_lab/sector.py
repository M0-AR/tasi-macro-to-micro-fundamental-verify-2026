"""Sector layer — weights, concentration, rotation teaching model."""
from __future__ import annotations

# May-2026 public snapshot (Invesense/MSCI): Financials ~40.45%, Materials ~15.05%, Energy ~12.64%.
# Used as prior; live constituent check via yfinance sector fields where available.
PRIOR_WEIGHTS = {"Financials": 40.45, "Materials": 15.05, "Energy": 12.64,
                 "Others": 31.86}

# Teaching rotation order (NOT a timing signal): recovery -> banks/credit first,
# then energy/materials on oil margins, then domestic demand (telecom, health,
# consumer), then rate-sensitive (real estate/REITs) as policy eases.
ROTATION_STAGES = [
    ("Early recovery / liquidity returns", ["Banks", "Financials"]),
    ("Commodity margin expansion", ["Energy", "Materials / Petrochemicals"]),
    ("Domestic demand broadening", ["Telecom", "Health", "Consumer", "Industrials"]),
    ("Policy easing / duration bid", ["REITs", "Real Estate", "Utilities"]),
]

def concentration_flag(top1_pct: float, top4_pct: float) -> str:
    if top4_pct > 30:
        return f"HIGH concentration: top-4 {top4_pct:.1f}% (e.g. banks) dominates index — index != market breadth. Check EGX30-style analogy: CIB effect."
    return "Moderate concentration."

def rotation_note(stage_idx: int) -> str:
    name, groups = ROTATION_STAGES[stage_idx % len(ROTATION_STAGES)]
    return f"{name}: watch {', '.join(groups)}"
