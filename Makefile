.DEFAULT_GOAL := help

include .env

SRC_PATH=./app
VENV_PATH=.venv
export REGISTRY=$(DOCKERHUB_USERNAME)/$(IMAGE_NAME)
export TAGS=$(shell curl -s "https://hub.docker.com/v2/repositories/${REGISTRY}/tags/" | jq -r '.results[].name'| grep -E 'rc[0-9]{2}' | tr '\n' ' ')
export LATEST_TAG := $(if $(TAGS),$(lastword $(sort $(TAGS))),00)
export LATEST_VERSION := $(shell echo "$(LATEST_TAG)" | sed -E 's/([0-9]+\.[0-9]+\.[0-9]+)-rc[0-9]{2}+/\1/')
export LATEST_RC := $(if $(filter-out 00,$(LATEST_TAG)),$(shell echo "$(LATEST_TAG)" | sed -E 's/^.*-rc([0-9]{2})$$/\1/'),00)
ifneq ($(IMAGE_VERSION),$(LATEST_VERSION))
	NEXT_RC := 00
else
	NEXT_RC := $(if $(filter-out 00,$(LATEST_TAG)),$(shell printf "%02d" $$(($(LATEST_RC) + 1))),00)
endif
export NEXT_RC

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: todo
todo:  ## Show the TODOs in the code.
	@{ grep -n -w TODO Makefile | uniq || echo "No pending tasks"; } | sed '/grep/d'

.PHONY: show-env
show-env:  ## Show the environment variables.
	@echo "Showing the environment variables."
	@echo "REGISTRY: $(REGISTRY)"
	@echo "TAGS: $(TAGS)"
	@echo "LATEST_TAG: $(LATEST_TAG)"
	@echo "IMAGE_VERSION: $(IMAGE_VERSION)"
	@echo "LATEST_VERSION: $(LATEST_VERSION)"
	@echo "LATEST_RC: $(LATEST_RC)"
	@echo "NEXT_RC: $(NEXT_RC)"

.PHONY: debug
debug: ## Prepare the app for debugging.
	@echo "Preparing $(IMAGE_NAME) for debugging."
	@python -m venv $(VENV_PATH)
	@chmod +x $(VENV_PATH)/bin/activate
	@./scripts/create-requirements.sh
	@$(VENV_PATH)/bin/activate && pip install --upgrade pip setuptools
	@$(VENV_PATH)/bin/activate && pip install -r app/requirements.txt
	$(MAKE) run

.PHONY: run
run:  ## Start the app in development mode.
	@echo "Starting $(IMAGE_NAME) in development mode."
	docker-compose -f $(SRC_PATH)/docker-compose.yml up --build $(IMAGE_NAME)

.PHONY: clean
clean:  ## Clean the app.
	@echo "Cleaning $(IMAGE_NAME) docker image."
	@rm -rf $(VENV_PATH)
	docker-compose -f $(SRC_PATH)/docker-compose.yml down

.PHONY: build
build:  ## Build the app.
	@echo "Building $(IMAGE_NAME) docker image as $(IMAGE_NAME):$(IMAGE_VERSION)."
	docker build -t $(REGISTRY):$(IMAGE_VERSION) $(SRC_PATH)

## TODO: Tag the image in git  - check with GithubActions
.PHONY: publish-image-rc
publish-image-rc: build ## Push the release candidate to the registry.
	@echo "Publishing the image as release candidate -  $(REGISTRY):$(IMAGE_VERSION)-rc$(NEXT_RC)"
	docker tag $(REGISTRY):$(IMAGE_VERSION) $(REGISTRY):$(IMAGE_VERSION)-rc$(NEXT_RC)
	docker push $(REGISTRY):$(IMAGE_VERSION)-rc$(NEXT_RC)

.PHONY: publish-image-latest
publish-image-latest:  build ## Publish the latest release to the registry.
	@echo "Publishing the latest image as latest- $(REGISTRY):$(LATEST_TAG) as latest"
	docker pull $(REGISTRY):$(LATEST_TAG)
	docker tag $(REGISTRY):$(LATEST_TAG) $(REGISTRY):latest
	docker push $(REGISTRY):latest

.PHONY: test
test:  ## Run the unit, integration and acceptance tests.
	@echo "Running the unit, integration and acceptance tests."
	$(MAKE) test-unit
	$(MAKE) test-integration
	$(MAKE) test-acceptance

.PHONY: pre-commit
pre-commit:  ## Run the pre-commit checks.
	@echo "Running the pre-commit checks."
	$(MAKE) reformat
	$(MAKE) check-typing
	$(MAKE) check-style

.PHONY: check-typing
check-typing:  ## Check the typing.
	@echo "Checking the typing."
	docker-compose -f $(SRC_PATH)/docker-compose.yml run --rm $(IMAGE_NAME) mypy .

.PHONY: check-style
check-style:  ## Check the styling.
	@echo "Checking the styling."
	docker-compose -f $(SRC_PATH)/docker-compose.yml run --rm $(IMAGE_NAME) ruff check .
	
.PHONY: reformat
reformat:  ## Reformat the code.
	@echo "Reformatting the code."
	docker-compose -f $(SRC_PATH)/docker-compose.yml run --rm $(IMAGE_NAME) ruff format .

.PHONY: test-unit
test-unit:  ## Run the unit tests.
	@echo "Running the unit tests."
	docker-compose -f $(SRC_PATH)/docker-compose.yml run --rm $(IMAGE_NAME) pytest -n 4 tests/unit -ra 

.PHONY: test-acceptance
test-acceptance:  ## Run the acceptance tests.
	@echo "Running the acceptance tests."
	docker-compose -f $(SRC_PATH)/docker-compose.yml run --rm $(IMAGE_NAME) pytest -n 4 tests/acceptance -ra
	
.PHONY: test-integration
test-integration:  ## Run the integration tests.
	@echo "Running the integration tests."
	docker-compose -f $(SRC_PATH)/docker-compose.yml run --rm $(IMAGE_NAME) pytest -n 4 tests/integration -ra