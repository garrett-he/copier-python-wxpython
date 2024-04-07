.DEFAULT_GOAL := help

.PHONY: help
help: ## Show help information
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: init
init: ## Initialize project
	pdm install
	pdm run pre-commit install

.PHONY: lint
lint: ## Code analyse and lint
	pdm run pylint --recursive=yes copier/ tests/

.PHONY: test
test: ## Run tests
	pdm run pytest

.PHONY: clean
clean: ## Clean up cache files
	find . -name '__pycache__' -type d | xargs rm -rf
	rm -rf .pytest_cache/ .venv/
	rm -f .python-version .pdm-python
