PY := $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

metrics:
	$(PY) scripts/aggregate_daily.py && cat metrics_daily.json

evals:
	$(PY) evals/core/run_evals.py | tee eval_out.jsonl

test:
	$(PY) -m pytest -q

api:
	set -a; [ -f .env ] && . ./.env; set +a; \
	$(PY) -m uvicorn svc.app:app --reload --port $${PORT:-8123}

docker-build:
	docker build -t eudaimonia-api:local .

docker-run:
	docker run --rm -p 8080:8080 -e API_TOKEN=dev-secret-123 eudaimonia-api:local

test:
	$(PY) -m pytest -q
