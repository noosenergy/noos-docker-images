FROM python:3.8.6-slim as builder

USER root

# Install Pipenv
# --------------
ARG PIP_NO_CACHE_DIR=0
ARG PIPENV_RELEASE="2020.11.4"
RUN pip install pipenv==$PIPENV_RELEASE

# Install python libs
# -------------------
WORKDIR /tmp/lib
COPY Pipfile* ./
# Install git checkouts natively
RUN pipenv install --system --deploy

# Add a user and related group with a home directory
# --------------------------------------------------
ARG APP_USER="neptune"
RUN useradd -m -U $APP_USER
USER $APP_USER
WORKDIR /home/${APP_USER}

COPY scripts/* /home/${APP_USER}
