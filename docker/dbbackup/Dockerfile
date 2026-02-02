FROM debian:bullseye

USER root

# Install Apt-packages
# --------------------
ARG APT_DEPS=" \
    # --- AWS CLI deps ---
    ca-certificates \
    wget \
    groff \
    less \
    unzip \
    # --- PostgreSQL deps ---
    lsb-release \
    gnupg \
    "
RUN apt-get update \
    && apt-get install -y --no-install-recommends $APT_DEPS

# Install AWSCLI
# --------------
# https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
ARG AWS_ARCHIVE="awscli-exe-linux-x86_64.zip"
ARG AWS_URL="https://awscli.amazonaws.com/${AWS_ARCHIVE}"
ARG AWS_SRC="/tmp/awscli"
WORKDIR $AWS_SRC
RUN wget $AWS_URL \
    && unzip $AWS_ARCHIVE \
    && ./aws/install \
    && rm -rf $AWS_SRC

# Install PostgreSQL-client
# -------------------------
# https://www.postgresql.org/download/linux/debian
ARG PG_DEPS=" \
    postgresql-client-18 \
    "
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && mkdir -p /usr/share/man/man1 \
    && mkdir -p /usr/share/man/man7 \
    && apt-get update \
    && apt-get install -y --no-install-recommends $PG_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Install config files
# --------------------
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set unprivileged user
# ---------------------
ARG APP_USER="noos"
RUN useradd -m -U $APP_USER
USER $APP_USER
WORKDIR /home/${APP_USER}

ENTRYPOINT ["docker-entrypoint.sh"]
