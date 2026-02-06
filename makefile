.PHONY: setup test lint lint-fix clean

# Task 3.2: Containerization & Automation
setup:
	uv sync --group dev
	uv pip install -e .

test:
	docker compose run --rm chimera-api uv run pytest tests/

# Task 3.3: CI/CD & AI Governance
# Combined duplicate lint targets and ensured proper find syntax
lint:
	uv run ruff check .
	uv run mypy .

lint-fix:
	uv run ruff check . --fix

clean:
	docker compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} +