FROM python:3.6.6-slim

USER root

# Install postgresql-client
# -------------------------
ARG APT_DEPS=" \
    postgresql-client-9.6 \
    ca-certificates \
    groff \
    less \
    "
RUN mkdir -p /usr/share/man/man1 \
    && mkdir -p /usr/share/man/man7 \
    && apt-get update \
    && apt-get install -y --no-install-recommends $APT_DEPS \
	&& rm -rf /var/lib/apt/lists/*

# Install AWS CLI
# ---------------
ARG AWS_CLI_VERSION="1.17.10"
ENV AWS_REGION="eu-west-1"
RUN pip --no-cache-dir install awscli==${AWS_CLI_VERSION}

# Install config files
# --------------------
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set unprivileged user
# ---------------------
RUN useradd -U noosbackup

WORKDIR /tmp
USER noosbackup

ENTRYPOINT ["docker-entrypoint.sh"]
