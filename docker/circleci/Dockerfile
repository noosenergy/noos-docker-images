# https://circleci.com/developer/images/image/cimg/python
# https://github.com/CircleCI-Public/cimg-python
# https://hub.docker.com/r/cimg/python
FROM cimg/python:3.8.17

USER root

# # Provision Selenium (Firefox)
# # ----------------------------
ARG FIREFOX_VERSION="v0.30.0"
RUN apt-get update && \
    apt-get install -y firefox && \
    apt-get clean && \
    curl -sSL "https://github.com/mozilla/geckodriver/releases/download/${FIREFOX_VERSION}/geckodriver-${FIREFOX_VERSION}-linux64.tar.gz" | \
    tar -xz -C /usr/local/bin

# Install Node.js
# ---------------
ARG NODE_VERSION="v16.13.1"
RUN curl -sSL "https://nodejs.org/dist/${NODE_VERSION}/node-${NODE_VERSION}-linux-x64.tar.xz" | \
	tar -xJ -C /usr/local --strip-components=1

# Install JavaScript package manager
# ----------------------------------
ARG YARN_VERSION="v1.22.17"
RUN npm install --global yarn@${YARN_VERSION}

# Install Python package managers
# -------------------------------
ARG PIPENV_RELEASE="2022.1.8"
ARG POETRY_RELEASE="1.5.1"
ENV PIPENV_VENV_IN_PROJECT=true
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_HOME=/home/circleci/.poetry
RUN pip install --upgrade pip && \
    pip install pipenv==$PIPENV_RELEASE && \
    curl -sSL "https://install.python-poetry.org" | \
    python - --version=$POETRY_RELEASE

# Install Noos CI/CD SDKs
# -----------------------
ARG NOOSINV_VERSION="0.0.11"
ARG NOOSTF_VERSION="0.0.6"
RUN pip install noos-inv==$NOOSINV_VERSION noos-tf==$NOOSTF_VERSION

WORKDIR /home/circleci/project
USER circleci
