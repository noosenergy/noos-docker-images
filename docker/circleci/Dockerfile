# https://circleci.com/developer/images/image/cimg/python
# https://github.com/CircleCI-Public/cimg-python
# https://hub.docker.com/r/cimg/python

# The Node.js image is multi-architecture, so by using a separate Node.js image,
# we can ensure that the Node.js version is compatible with the chosen target architecture of the final stage.
FROM node:18.18 AS builder

FROM cimg/python:3.12.8

USER root

# Provision Selenium (Firefox)
# Change package source to install Firefox .deb instead of snap, as snap is now the default
# Install geckodriver
# ----------------------------
ARG GECKODRIVER_VERSION="v0.33.0"
COPY mozilla-firefox /etc/apt/preferences.d/
RUN apt-get update && \
    add-apt-repository ppa:mozillateam/ppa -y && \
    apt install firefox && \
    curl -sSL "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz" | \
    tar -xzv -C /usr/local/bin

# Install Node.js
# ---------------
# Copy Node.js from the builder stage.
COPY --from=builder /usr/local/bin/node /usr/local/bin/node
COPY --from=builder /usr/local/bin/npm /usr/local/bin/npm
COPY --from=builder /usr/local/lib/node_modules /usr/local/lib/node_modules

# Reconfigure npm path
RUN rm /usr/local/bin/npm
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm

# Install JavaScript package manager
# ----------------------------------
ARG YARN_VERSION="v1.22.19"
RUN npm install --global yarn@${YARN_VERSION}


# Install Python package managers
# -------------------------------
ARG PIPENV_RELEASE="2023.6.2"
ARG POETRY_RELEASE="1.5.1"
ENV PIPENV_VENV_IN_PROJECT=true
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_HOME=/home/circleci/.poetry
ENV UV_CACHE_DIR=./.uv-cache
COPY --from=ghcr.io/astral-sh/uv:0.5.24 /uv /uvx /usr/local/bin/
RUN pip install --upgrade pip && \
    pip install pipenv==$PIPENV_RELEASE && \
    curl -sSL "https://install.python-poetry.org" | \
    python - --version=$POETRY_RELEASE

# Install Noos CI/CD SDKs
# -----------------------
ARG NOOSINV_VERSION="0.2.3"
ARG NOOSTF_VERSION="0.0.9"
RUN pip install noos-inv==$NOOSINV_VERSION noos-tf==$NOOSTF_VERSION

WORKDIR /home/circleci/project
USER circleci
