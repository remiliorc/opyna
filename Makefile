.PHONY: install data api web test lint

install:
	pip install -r requirements.txt && pip install -e .

data:
	python -m opyna.data.download --category Electronics --n-per-rating 5000

api:
	uvicorn opyna.api.main:app --reload

web:
	python -m opyna.web.app

test:
	pytest -q

lint:
	ruff check src
