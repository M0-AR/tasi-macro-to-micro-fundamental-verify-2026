"""Central config — all tickers, claims, and thresholds versioned for reproducibility."""
from __future__ import annotations

# Yahoo Finance symbols (verified via yfinance docs + live probing in experiments).
# TASI index itself: ^TASI.SR commonly quoted; fallback ^TASI.
TASI_SYMBOLS = ["^TASI.SR", "^TASI"]

# Representative Saudi heavyweights for macro-to-micro verification.
# Format: yahoo_symbol -> (company, sector)
SAUDI_TICKERS: dict[str, tuple[str, str]] = {
    "2222.SR": ("Saudi Aramco", "Energy"),
    "1120.SR": ("Al Rajhi Bank", "Banks"),
    "1180.SR": ("Saudi National Bank SNB", "Banks"),
    "2010.SR": ("SABIC", "Materials / Petrochemicals"),
    "2020.SR": ("SABIC Agri-Nutrients", "Materials"),
    "7010.SR": ("STC", "Telecom"),
    "5110.SR": ("Saudi Electricity", "Utilities"),
    "1150.SR": ("Alinma Bank", "Banks"),
    "1060.SR": ("Arab National Bank", "Banks"),
    "4030.SR": ("Bahri", "Transport / Energy logistics"),
    "2380.SR": ("Petro Rabigh", "Materials / Petrochemicals"),
    "4334.SR": ("Al Rajhi REIT", "REITs"),
    "1020.SR": ("Bank AlJazira", "Banks"),
}

# Benchmarks
BENCHMARKS: dict[str, str] = {
    "SP500": "^GSPC",
    "MSCI_EM_proxy": "EEM",
    "Brent": "BZ=F",
    "WTI": "CL=F",
    "US10Y": "^TNX",
}

# Video claims to verify (transcript-derived, each must be checked vs live data).
VIDEO_CLAIMS = {
    "tasi_level_oct5": 10500,
    "tasi_jan_level": 11382,
    "tasi_drawdown_claim_pct": -8.0,
    "pe_ratio_early26": 16.4,
    "pb_ratio_early26": 2.95,
    "sama_repo_2026_09_16": 4.50,
    "sama_reverse_repo_2026_09_16": 4.00,
    "sar_usd_peg": 3.75,
    "non_oil_growth_25_26_claim": 4.2,
    "gdp_growth_25_26_claim": 4.6,
    "gdp_growth_26_forecast_claim": 1.7,
    "inflation_forecast_claim": 2.2,
}

# Tolerances for verification (_live data moves_).
TOL = {
    "tasi_pct": 0.25,   # 25% band for level checks (market moves fast)
    "pe_abs": 4.0,      # P/E moves with earnings cycle
    "pb_abs": 1.2,
    "rate_abs": 0.30,   # 30 bps
    "fx_abs": 0.02,
    "growth_abs": 1.8,  # pp
}

WORLD_BANK_SAUDI = {"country": "Saudi Arabia", "indicator": "NY.GDP.MKTP.KD.ZG"}
