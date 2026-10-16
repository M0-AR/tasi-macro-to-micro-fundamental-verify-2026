"""CLI — fetch-all + verify entry points for Docker/Make reproducibility."""
from __future__ import annotations
import argparse, json, pathlib
from .config import SAUDI_TICKERS, TASI_SYMBOLS, BENCHMARKS
from .data_fetcher import fetch_yahoo_history, fetch_yahoo_fast_info, fetch_worldbank_gdp, save_json

def cmd_fetch_all(out: str):
    base = pathlib.Path(out); base.mkdir(parents=True, exist_ok=True)
    manifest = {"tasi": {}, "stocks": {}, "benchmarks": {}, "worldbank": {}}
    for sym in TASI_SYMBOLS:
        try:
            df, prov = fetch_yahoo_history(sym, period="5y")
            df.to_csv(base / f"TASI_{sym.replace('^','').replace('.','_')}.csv")
            manifest["tasi"][sym] = prov
            if len(df):
                break
        except Exception as e:
            manifest["tasi"][sym] = {"error": str(e)[:300]}
    for sym in list(SAUDI_TICKERS.keys()) + list(BENCHMARKS.values()):
        try:
            df, prov = fetch_yahoo_history(sym, period="5y")
            df.to_csv(base / f"{sym.replace('^','').replace('.','_').replace('=','')}.csv")
            fi, fip = fetch_yahoo_fast_info(sym)
            save_json({"fast": fi, "prov": fip}, base / f"{sym.replace('^','').replace('.','_').replace('=','')}_info.json")
            manifest["stocks"][sym] = prov
        except Exception as e:
            manifest["stocks"][sym] = {"error": str(e)[:300]}
    try:
        series, prov = fetch_worldbank_gdp()
        save_json({"series": series, "prov": prov}, base / "worldbank_saudi_gdp.json")
        manifest["worldbank"] = prov
    except Exception as e:
        manifest["worldbank"] = {"error": str(e)[:300]}
    save_json(manifest, base / "manifest.json")
    print(json.dumps(manifest, indent=2, default=str))

def cmd_verify(out: str):
    # Lightweight CLI verify: delegates to experiments for full audit.
    import subprocess, sys
    print("Run: make verify (experiments/01..05). See evidence/ for JSON outputs.")
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out).write_text(json.dumps({"hint": "see evidence/*.json from experiments"}, indent=2))

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("fetch-all"); a.add_argument("--out", default="data/raw")
    b = sub.add_parser("verify"); b.add_argument("--out", default="evidence/verification.json")
    args = ap.parse_args()
    if args.cmd == "fetch-all":
        cmd_fetch_all(args.out)
    elif args.cmd == "verify":
        cmd_verify(args.out)

if __name__ == "__main__":
    main()
