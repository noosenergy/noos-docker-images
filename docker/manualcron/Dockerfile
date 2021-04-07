FROM python:3.8.6 as builder

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


# -----------------
# Multi-stage-build
# -----------------


FROM python:3.8.6-slim

# Copy python dependencies
# ------------------------
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

# Add a user and related group with a home directory
# --------------------------------------------------
ARG APP_USER="neptune"
RUN useradd -m -U $APP_USER
USER $APP_USER
WORKDIR /home/${APP_USER}

COPY *.py /home/${APP_USER}
