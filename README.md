[![CircleCI](https://circleci.com/gh/noosenergy/noos-forge.svg?style=svg&circle-token=6ed140ddf30bafe312339a5d3adaec60106d0710)](https://circleci.com/gh/noosenergy/noos-forge)

# Noos Forge
Set of developer tools for working locally on the Neptune platform.

## Quickstart

### Docker installation

On Mac OSX, make sure [Homebrew](https://brew.sh/) has been pre-configured, then install Docker,

    $ brew cask install docker

### Local development

This project comes with a `Makefile` which is ready to do basic common tasks.

```
$ make
help                           Display this auto-generated help message
docker-login                   Login to docker hub image repository
docker-build                   Build docker image for specified COMPONENT
docker-tag                     Tag docker image for specified COMPONENT for upload
docker-push                    Push docker image for specified COMPONENT
```

## Deployment

The repository implements as well a set of utilities with their associated Docker images:

* a [backing-up service](./docker/db-back-up) for databases into local / remote storage
* a [jupyter-lab service](./docker/jupyter) for launching a k8s pre-configured notebook server
