[![CircleCI](https://circleci.com/gh/noosenergy/noos-forge.svg?style=svg&circle-token=6ed140ddf30bafe312339a5d3adaec60106d0710)](https://circleci.com/gh/noosenergy/noos-forge)

# Noos Forge
Set of developer tools for working locally on the Neptune platform and build optimized base images.

## Quickstart

### Docker installation

On Mac OSX, make sure [Homebrew](https://brew.sh/) has been pre-configured, then install Docker,

    $ brew cask install docker

### Docker image optimisation

#### Analysis

You can use [dive](https://github.com/wagoodman/dive) to look into the image build process and each layer.\
Dive gives an "image efficiency" ratio and makes it easier to find wasted space in the final image.

    $ brew install dive

#### Optimisation tips

- Bundle commands with `&&` to minimize the layer number (created by each `RUN`, `COPY` or `ADD`).
- Clean unnecessary files at each layer phase.
- Use `MultiBuild` to only copy the necessary resulting files from a heavy install.
- When possible, squash layers that should not be used. An optimized base image could theoretically be squashed entirely.

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
* a [jupyter-lab service](docker/jupyterlab) for launching a k8s pre-configured notebook server
