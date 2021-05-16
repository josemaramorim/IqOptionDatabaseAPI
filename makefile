# Variables
SRC_DIR := ./src
LINE_LENGTH := 120
PYTHONPATH := $(shell pwd)


run:
	gunicorn "src.app:app" -c "./src/gunicorn.py"

format:
	black $(SRC_DIR)/* --line-length=$(LINE_LENGTH) --skip-string-normalization
	isort $(SRC_DIR)/* --line-length=$(LINE_LENGTH) --multi-line=0
	flake8 $(SRC_DIR)/* --max-line-length=$(LINE_LENGTH) --exclude ./src/utils/iqoptionapi

revision:
	@PYTHONPATH="${PYTHONPATH}" alembic revision --autogenerate

upgrade:
	@PYTHONPATH="${PYTHONPATH}" alembic upgrade head

downgrade:
	@PYTHONPATH="${PYTHONPATH}" alembic downgrade -1


clean-pyc:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -rf {} +
	find . -name '*.pyo' -exec rm -rf {} +
	find . -name '*~' -exec rm -rf {} +
