SHELL := /bin/sh -e

COMPONENT ?= jupyter
IMAGE_TAG ?= test
IMAGE_NAME ?= noosforge

.DEFAULT_GOAL := help


# Helper
.PHONY: help

help:  ## Display this auto-generated help message
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


# Docker workflow
.PHONY: docker-login docker-build docker-tag docker-push

docker-login:  ## Login to docker hub image repository
	# https://hub.docker.com/u/noosenergy/
	docker login --username noosenergy --password ${DOCKERHUB_TOKEN}

docker-build:  ## Build docker image for specified COMPONENT
	docker build --pull --tag ${IMAGE_NAME}/${COMPONENT} docker/${COMPONENT}

docker-tag:  ## Tag docker image for specified COMPONENT for upload
	docker tag ${IMAGE_NAME}/${COMPONENT} noosenergy/${COMPONENT}:${IMAGE_TAG}
	docker tag ${IMAGE_NAME}/${COMPONENT} noosenergy/${COMPONENT}:latest

docker-push:  ## Push docker image for specified COMPONENT
	docker push noosenergy/${COMPONENT}:${IMAGE_TAG}
	docker push noosenergy/${COMPONENT}:latest
