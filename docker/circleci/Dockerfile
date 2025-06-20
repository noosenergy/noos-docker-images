# https://circleci.com/developer/images/image/cimg/python
# https://github.com/CircleCI-Public/cimg-python
# https://hub.docker.com/r/cimg/python

# The Node.js image is multi-architecture, so by using a separate Node.js image,
# we can ensure that the Node.js version is compatible with the chosen target architecture of the final stage.
FROM node:18.18 AS builder

FROM cimg/python:3.12.8

USER root

# Provision Selenium (Firefox + GeckoDriver)

#==============================
# Firefox Nightly installation
#==============================
ARG FIREFOX_VERSION="nightly-latest"
# Determine the correct OS string for Firefox
RUN if [ "${TARGETPLATFORM}" = "linux/arm64" ]; then \
        FIREFOX_OS="linux-aarch64"; \
        FIREFOX_VERSION="nightly-latest"; \
    else \
        FIREFOX_OS="linux64"; \
        FIREFOX_VERSION="latest"; \
    fi && \
    apt-get update -qqy && \
    apt-get -qqy --no-install-recommends install \
        libavcodec-extra \
        libgtk-3-dev \
        libdbus-glib-1-dev \
        libasound2 \
        xz-utils && \
    curl -sSL "https://download.mozilla.org/?product=firefox-${FIREFOX_VERSION}-ssl&os=${FIREFOX_OS}&lang=en-US" | \
    tar xJv -C /usr/lib/ && \
    ln -fs /usr/lib/firefox/firefox /usr/bin/firefox && \
    rm -rf /var/lib/apt/lists/*

#==============================
# GeckoDriver
#
# SOURCE: docker-selenium/NodeFirefox
# https://github.com/SeleniumHQ/docker-selenium/blob/70ac588d567b253c93c91d990a5b197f5f8d146a/NodeFirefox/Dockerfile#L66
#==============================
ARG GECKODRIVER_VERSION="latest"
RUN LATEST_VERSION=$(curl -sk https://api.github.com/repos/mozilla/geckodriver/releases/latest | jq -r '.tag_name') \
    && DRIVER_ARCH=$(if [ "$(dpkg --print-architecture)" = "amd64" ]; then echo "linux64"; else echo "linux-aarch64"; fi) \
    && GK_VERSION=$(if [ ${GECKODRIVER_VERSION:-latest} = "latest" ]; then echo "${LATEST_VERSION}"; else echo $GECKODRIVER_VERSION; fi) \
    && wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/${GK_VERSION}/geckodriver-${GK_VERSION}-${DRIVER_ARCH}.tar.gz \
    && rm -rf /opt/geckodriver \
    && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
    && rm /tmp/geckodriver.tar.gz \
    && mv /opt/geckodriver /opt/geckodriver-$GK_VERSION \
    && chmod 755 /opt/geckodriver-$GK_VERSION \
    && ln -fs /opt/geckodriver-$GK_VERSION /usr/bin/geckodriver


# Install Node.js
# ---------------
# Copy Node.js from the builder stage.
COPY --from=builder /usr/local/bin/node /usr/local/bin/node
COPY --from=builder /usr/local/bin/npm /usr/local/bin/npm
COPY --from=builder /usr/local/lib/node_modules /usr/local/lib/node_modules

# Reconfigure npm path
RUN rm /usr/local/bin/npm
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm

# Install JavaScript package manager
# ----------------------------------
ARG YARN_VERSION="v1.22.19"
RUN npm install --global yarn@${YARN_VERSION}


# Install Python package managers
# -------------------------------
ARG PIPENV_RELEASE="2023.6.2"
ARG POETRY_RELEASE="1.5.1"
ENV PIPENV_VENV_IN_PROJECT=true
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_HOME=/home/circleci/.poetry
ENV UV_CACHE_DIR=./.uv-cache
COPY --from=ghcr.io/astral-sh/uv:0.7.13 /uv /uvx /usr/local/bin/
RUN pip install --upgrade pip && \
    pip install pipenv==$PIPENV_RELEASE && \
    curl -sSL "https://install.python-poetry.org" | \
    python - --version=$POETRY_RELEASE

# Install Noos CI/CD SDKs
# -----------------------
ARG NOOSINV_VERSION="0.2.7"
ARG NOOSTF_VERSION="0.0.9"
RUN pip install noos-inv==$NOOSINV_VERSION noos-tf==$NOOSTF_VERSION
RUN noosinv --print-completion-script=bash >> /home/circleci/.bashrc

WORKDIR /home/circleci/project
USER circleci
