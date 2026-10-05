# proyecto-abel — tareas del repositorio del skill / skill repository tasks
SHELL := /bin/bash
.DEFAULT_GOAL := help
.PHONY: help test test-slow lint format check page

help: ## Lista los objetivos / List targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

test: ## Pruebas rápidas del scaffolder / Fast tests
	uv run --with pytest pytest -q tests

test-slow: ## Incluye uv sync + make check en un proyecto generado / Full end-to-end
	RUN_SLOW=1 uv run --with pytest pytest -q tests

lint: ## Ruff sobre scripts y pruebas / Lint
	uvx ruff check --line-length 100 --select E,F,I,B,UP,SIM skills/proyecto-abel/scripts tests tools

format: ## Formatea scripts y pruebas / Format
	uvx ruff format --line-length 100 skills/proyecto-abel/scripts tests tools

check: lint test ## lint + pruebas / lint + tests

page: ## Regenera docs/workflow.html desde el fragmento / Rebuild standalone workflow page
	python3 tools/build_workflow_page.py
