[![CircleCI](https://dl.circleci.com/status-badge/img/gh/noosenergy/noos-docker-images/tree/master.svg?style=svg&circle-token=0137e0b415488ec2150fd2c329d2a350c8bcc0f1)](https://dl.circleci.com/status-badge/redirect/gh/noosenergy/noos-docker-images/tree/master)

# Noos Docker Images

Set of developer tools for working locally on the Noos platform and build optimized [Docker base images](https://hub.docker.com/u/noosenergy):

* a [CircleCI base image](./docker/circleci) for running CI/CD pipelines
* a [DB backup script image](./docker/dbbackup) for persisting databases into local / remote storage
* a [JupyterLab server image](./docker/jupyterlab) for launching a k8s pre-configured Jupyter notebook server
* a [Python script image](./docker/pyscript) for running Python scripts within a k8s pre-configured container

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
