MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.SUFFIXES:

PYTHON_CMD_PREFIX ?=

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Build a docker image
	docker build -t walking_notification:latest .

.PHONY: fix_py_imports
fix_py_imports: ## Fixes python imports
	@$(PYTHON_CMD_PREFIX) isort --recursive .

.PHONY: lint_py
lint_py: ## Lint Python
	@echo "Checking code using flake8 ..."
	@$(PYTHON_CMD_PREFIX) flake8 .

.PHONY: lint_imports
lint_imports: ## Lint Python imports
	@echo "Checking python imports ..."
	@$(PYTHON_CMD_PREFIX) isort --recursive --check-only --diff .

PHONY: lint
lint: lint_py lint_imports  ## Lint Python and Python imports

.PHONY: run_bash
run_bash: ## Run bash in a docker container
	docker run -it -v `pwd`:/code \
	-e YAHOO_CLIENT_KEY=${YAHOO_CLIENT_KEY} \
	-e YAHOO_CLIENT_SECRET=${YAHOO_CLIENT_SECRET} \
	-e SLACK_API_TOKEN=${SLACK_API_TOKEN} \
	walking_notification:latest bash

.PHONY: test
test: ## Test the code
	docker run -it -v `pwd`:/code \
	-e YAHOO_CLIENT_KEY=${YAHOO_CLIENT_KEY} \
	-e YAHOO_CLIENT_SECRET=${YAHOO_CLIENT_SECRET} \
	walking_notification:latest py.test tests.py