# Makefile for Agentic Workflows

.PHONY: help install test lint format clean docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  install       - Install dependencies"
	@echo "  test          - Run tests"
	@echo "  lint          - Run linters"
	@echo "  format        - Format code"
	@echo "  clean         - Clean build artifacts"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-up     - Start Docker services"
	@echo "  docker-down   - Stop Docker services"

install:
	pip install -r requirements-full.txt
	pip install -e .

test:
	pytest -v --cov=agentic_workflows

lint:
	ruff check .
	mypy agentic_workflows

format:
	black agentic_workflows tests
	ruff check --fix .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov

docker-build:
	docker build -t agentic-workflows:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down
