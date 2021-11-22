FROM python:3.8.6-slim

USER root

# Install postgresql-client
# -------------------------
ARG APT_DEPS=" \
    postgresql-client \
    groff \
    less \
    wget \
    unzip \
    "
RUN mkdir -p /usr/share/man/man1 \
    && mkdir -p /usr/share/man/man7 \
    && apt-get update \
    && apt-get install -y --no-install-recommends $APT_DEPS \
	&& rm -rf /var/lib/apt/lists/*

# Install AWS CLI
# ---------------
# https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
ARG AWS_ARCHIVE="awscli-exe-linux-x86_64.zip"
ARG AWS_URL="https://awscli.amazonaws.com/${AWS_ARCHIVE}"
ARG AWS_SRC="/tmp/awscli"
ENV AWS_REGION="eu-west-1"
WORKDIR $AWS_SRC
RUN wget $AWS_URL \
    && unzip $AWS_ARCHIVE \
    && ./aws/install \
    && rm -rf $AWS_SRC

# Install config files
# --------------------
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set unprivileged user
# ---------------------
ARG APP_USER="neptune"
RUN useradd -m -U $APP_USER
USER $APP_USER
WORKDIR /home/${APP_USER}

ENTRYPOINT ["docker-entrypoint.sh"]
