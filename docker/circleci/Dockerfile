FROM cimg/python:3.8.6

USER root

# Install Python package managers
# -------------------------------
ARG PIPENV_RELEASE="2020.11.4"
ARG POETRY_RELEASE="1.1.4"
ENV PIPENV_VENV_IN_PROJECT=true
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN pip install --upgrade pip \
    && pip install pipenv==$PIPENV_RELEASE poetry==$POETRY_RELEASE

# Install Noos CI/CD SDKs
# -----------------------
ARG NOOSINV_VERSION="0.0.8"
ARG NOOSTF_VERSION="0.0.6"
RUN pip install noos-inv==$NOOSINV_VERSION noos-tf==$NOOSTF_VERSION

WORKDIR $HOME/project
USER circleci
