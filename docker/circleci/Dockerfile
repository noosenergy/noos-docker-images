# ARG UV_RELEASE=0.3.0
# FROM ghcr.io/astral-sh/uv:$UV_RELEASE AS stageforcopy

# https://circleci.com/developer/images/image/cimg/python
# https://github.com/CircleCI-Public/cimg-python
# https://hub.docker.com/r/cimg/python
FROM cimg/python:3.11.4

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
ARG NODE_VERSION="v18.18.0"
RUN curl -sSL "https://nodejs.org/dist/${NODE_VERSION}/node-${NODE_VERSION}-linux-x64.tar.xz" | \
    tar -xJ -C /usr/local --strip-components=1

# Install JavaScript package manager
# ----------------------------------
ARG YARN_VERSION="v1.22.19"
RUN npm install --global yarn@${YARN_VERSION}

# Install Python package managers
# -------------------------------
ARG PIPENV_RELEASE="2023.6.2"
ARG POETRY_RELEASE="1.5.1"
ARG UV_RELEASE="0.3.0"
ENV PIPENV_VENV_IN_PROJECT=tre
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_HOME=/home/circleci/.poetry
ENV CARGO_HOME=/home/circleci/.cargo
ENV PATH="/home/circleci/.cargo/bin/:$PATH"
RUN pip install --upgrade pip && \
    pip install pipenv==$PIPENV_RELEASE && \
    curl -sSL "https://install.python-poetry.org" | \
    python - --version=$POETRY_RELEASE && \
    curl -LsSf https://astral.sh/uv/$UV_RELEASE/install.sh | sh

# Install Noos CI/CD SDKs
# -----------------------
ARG NOOSINV_VERSION="0.0.17"
ARG NOOSTF_VERSION="0.0.8"
RUN pip install noos-inv==$NOOSINV_VERSION noos-tf==$NOOSTF_VERSION

WORKDIR /home/circleci/project
USER circleci
