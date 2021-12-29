# https://github.com/CircleCI-Public/cimg-python/blob/master/3.8/Dockerfile
FROM cimg/python:3.8.6

USER root

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
ARG PIPENV_RELEASE="2020.11.4"
ARG POETRY_RELEASE="1.1.12"
ENV PIPENV_VENV_IN_PROJECT=true
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_HOME=/home/circleci/.poetry
RUN pip install pipenv==$PIPENV_RELEASE && \
    curl -sSL "https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py" | \
    python - --uninstall && \
    curl -sSL "https://install.python-poetry.org" | \
    python - --version=$POETRY_RELEASE

# Install Noos CI/CD SDKs
# -----------------------
ARG NOOSINV_VERSION="0.0.8"
ARG NOOSTF_VERSION="0.0.6"
RUN pip install noos-inv==$NOOSINV_VERSION noos-tf==$NOOSTF_VERSION

WORKDIR /home/circleci/project
USER circleci
