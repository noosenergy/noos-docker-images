[![CircleCI](https://circleci.com/gh/noosenergy/noos-forge.svg?style=svg&circle-token=6ed140ddf30bafe312339a5d3adaec60106d0710)](https://circleci.com/gh/noosenergy/noos-forge)

# Noos Forge

Set of developer tools for working locally on the Neptune platform and build optimized [Docker base images](https://hub.docker.com/u/noosenergy):

* a [CircleCI image](./docker/circleci) for running CI/CD pipelines
* a [Backup service](./docker/dbbackup) for persisting databases into local / remote storage
* a [Fluentd service](./docker/fluentd) for launching a k8s pre-configured Fluentd daemonset
* a [JupyterLab service](./docker/jupyterlab) for launching a k8s pre-configured Jupyter notebook server

## Quickstart

### Docker installation

On Mac OSX, make sure [Homebrew](https://brew.sh/) has been pre-configured, then install Docker,

```sh
brew cask install docker
```

### Docker image optimisation

#### Analysis

You can use [dive](https://github.com/wagoodman/dive) to look into the image build process and each layer.\
Dive gives an "image efficiency" ratio and makes it easier to find wasted space in the final image.

```sh
brew install dive
```

#### Optimisation tips

* Bundle commands with `&&` to minimize the layer number (created by each `RUN`, `COPY` or `ADD`).
* Clean unnecessary files at each layer phase.
* Use `MultiBuild` to only copy the necessary resulting files from a heavy install.
* When possible, squash layers that should not be used. An optimized base image could theoretically be squashed entirely.

### Local development

The development workflows of this project can be managed by [noos-invoke](https://github.com/noosenergy/noos-invoke), a ready-made CLI for common CI/CD tasks.

```shell
~$ noosinv
Usage: noosinv [--core-opts] <subcommand> [--subcommand-opts] ...
```
