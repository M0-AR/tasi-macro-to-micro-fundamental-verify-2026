# METHOD — zero-to-hero verification protocol (best-practice synthesis)
1. **One search at a time** (no parallel websearch): websearch → duckduckgo → openresearch(*) → paper-search(*) → agent-reach → gitmcp → kaggle → wiki → gsd → superpowers. Backoff 5s→10s max 3 on 429; DuckDuckGo-lite fallback.
2. **Vote, don't trust:** require ≥3 independent sources per number (e.g. P/E: Tharaa + Albilad + Aljazira + Argaam).
3. **Live-first, honest fallback:** World Bank API + SAMA pages + Yahoo; on 429/DNS, use dated broker PDFs with exact dates, never silently substitute.
4. **No-lookahead:** trailing multiples only; formation-date snapshots; walk-forward 63d; OOS second half; costs 20bps; survivorship-fixed.
5. **Pre-register H1–H5** + Bonferroni; report ALL.
6. **Evidence:** every experiment writes `evidence/*.json` with `fetched_at` + provenance; unit tests 7/7 must pass before README claims.
7. **Repro:** `docker compose up --build` or `make verify`; `PYTHONPATH=.` for local.
