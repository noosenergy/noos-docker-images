SHELL := /bin/sh -e

COMPONENT ?= base
IMAGE_TAG ?= test
IMAGE_NAME ?= noosforge

.DEFAULT_GOAL := help


# Helper
.PHONY: help

help:  ## Display this auto-generated help message
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


# Installation
.PHONY: dotenv services

dotenv:  ## Create docker-compose dotenv file
	cd local/ && cp docker-env.template .env

services:  ## Instantiate all services via docker-compose
	cd local/ && docker-compose up


# Deployment
.PHONY: docker-build docker-tag docker-login docker-push

docker-build:  ## Build docker image for specified COMPONENT
	docker build -t ${IMAGE_NAME}/${COMPONENT} docker/${COMPONENT}

docker-tag:  ## Tag docker image for specified COMPONENT for upload
	docker tag ${IMAGE_NAME}/${COMPONENT} noosenergy/${COMPONENT}:${IMAGE_TAG}
	docker tag ${IMAGE_NAME}/${COMPONENT} noosenergy/${COMPONENT}:latest

docker-login:  # Login to docker hub image repository
	# https://hub.docker.com/u/octoenergy/
	docker login -u ${DOCKER_HUB_USER} -p ${DOCKER_HUB_PASSWORD}

docker-push:  ## Push docker image for specified COMPONENT
	docker push noosenergy/${COMPONENT}:${IMAGE_TAG}
	docker push noosenergy/${COMPONENT}:latest
