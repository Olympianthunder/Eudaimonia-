PY ?= python3

metrics:
	$(PY) scripts/aggregate_daily.py && cat metrics_daily.json

evals:
	$(PY) evals/core/run_evals.py | tee eval_out.jsonl

api:
	set -a; [ -f .env ] && . ./.env; set +a; \
	$(PY) -m uvicorn svc.app:app --reload --port 8123

test:
	$(PY) -m pytest -q
