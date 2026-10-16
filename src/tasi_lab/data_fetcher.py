"""Live data fetchers — Yahoo Finance + World Bank + SAMA/IMF pages.
Design rules (from online best-practice synthesis):
- No lookahead: every fundamental snapshot is point-in-time; price history split by date.
- Cache raw responses under data/raw with UTC timestamp.
- Every function returns (payload, provenance dict) so evidence is auditable.
"""
from __future__ import annotations
import json, datetime, pathlib, time
import requests
import yfinance as yf
import pandas as pd

UA = {"User-Agent": "tasi-fundamental-lab/0.1.0 (research; contact: lab@localhost)"}

def utcnow() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def fetch_yahoo_history(symbol: str, period: str = "5y", interval: str = "1d") -> tuple[pd.DataFrame, dict]:
    t = yf.Ticker(symbol)
    df = t.history(period=period, interval=interval, auto_adjust=False)
    prov = {"source": "yfinance.history", "symbol": symbol, "period": period,
            "interval": interval, "fetched_at": utcnow(), "rows": int(len(df))}
    return df, prov

def fetch_yahoo_fast_info(symbol: str) -> tuple[dict, dict]:
    t = yf.Ticker(symbol)
    out: dict = {}
    try:
        fi = t.fast_info
        for k in ["last_price", "previous_close", "open", "day_high", "day_low",
                  "year_high", "year_low", "market_cap", "currency", "exchange",
                  "last_volume", "ten_day_average_volume"]:
            try:
                out[k] = getattr(fi, k, None)
                if hasattr(out[k], "item"):
                    out[k] = out[k].item()
            except Exception:
                pass
    except Exception as e:
        out["fast_info_error"] = str(e)
    try:
        info = t.get_info() if hasattr(t, "get_info") else t.info
        for k in ["trailingPE", "forwardPE", "priceToBook", "trailingEps",
                  "bookValue", "dividendYield", "returnOnEquity", "marketCap",
                  "sector", "industry", "longName", "currency"]:
            if k in info:
                out[k] = info[k]
    except Exception as e:
        out["info_error"] = str(e)[:500]
    prov = {"source": "yfinance.fast_info+info", "symbol": symbol, "fetched_at": utcnow()}
    return out, prov

def fetch_worldbank_gdp(country: str = "Saudi Arabia", indicator: str = "NY.GDP.MKTP.KD.ZG",
                         start: int = 2015, end: int = 2025) -> tuple[dict, dict]:
    url = f"https://api.worldbank.org/v2/country/SAU/indicator/{indicator}"
    params = {"format": "json", "date": f"{start}:{end}", "per_page": 100}
    r = requests.get(url, params=params, headers=UA, timeout=30)
    r.raise_for_status()
    js = r.json()
    rows = js[1] if len(js) > 1 else []
    series = {x["date"]: x["value"] for x in rows if x.get("value") is not None}
    prov = {"source": "api.worldbank.org", "url": url, "fetched_at": utcnow()}
    return series, prov

def fetch_url_text(url: str, timeout: int = 30) -> tuple[str, dict]:
    r = requests.get(url, headers=UA, timeout=timeout)
    prov = {"source": "http", "url": url, "status": r.status_code, "fetched_at": utcnow(),
            "bytes": len(r.content)}
    r.raise_for_status()
    return r.text[:20000], prov

def save_json(obj, path: str | pathlib.Path):
    p = pathlib.Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, default=str))
