FROM python:3.8.6-slim

USER root

# Install Fluentd client
# ----------------------
# https://docs.fluentd.org/language-bindings/python
RUN pip install --no-cache holidays fluent-logger

# Set unprivileged user
# ---------------------
ARG APP_USER="neptune"
RUN useradd -m -U $APP_USER
USER $APP_USER
WORKDIR /home/${APP_USER}
