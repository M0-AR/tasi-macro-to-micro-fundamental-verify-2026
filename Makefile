.PHONY: verify test paper data clean
verify:
	python -m src.tasi_lab.cli verify --out evidence/verification.json
	python experiments/01_verify_video_claims.py
	python experiments/02_macro_to_micro.py
	python experiments/03_sector_benchmark.py
	python experiments/04_valuation_benchmark.py
	python experiments/05_hidden_patterns.py
test:
	pytest -q
data:
	python -m src.tasi_lab.cli fetch-all --out data/
clean:
	rm -rf data/cache/* evidence/*.json __pycache__
