FROM cimg/python:3.8.6

USER root

# Install Node.js
# ---------------
ARG NODE_VERSION="v16.13.1"
RUN curl -L -o node.tar.xz "https://nodejs.org/dist/${NODE_VERSION}/node-${NODE_VERSION}-linux-x64.tar.xz" \
	&& tar -xJf node.tar.xz -C /usr/local --strip-components=1 \
	&& rm node.tar.xz \
	&& ln -s /usr/local/bin/node /usr/local/bin/nodejs

# Install JavaScript package manager
# ----------------------------------
ARG YARN_VERSION="v1.22.17"
RUN npm install --global yarn@${YARN_VERSION}

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
