# https://hub.docker.com/u/noosenergy/
# https://github.com/jupyter/docker-stacks
# https://hub.docker.com/u/jupyter/
FROM jupyter/base-notebook:python-3.8.6 AS base-builder

USER root

# Install OS dependencies
# -----------------------
ARG APT_DEPS=" \
    build-essential \
    git \
    inkscape \
    jed \
    libsm6 \
    libxext-dev \
    libxrender1 \
    lmodern \
    netcat \
    pandoc \
    python-dev \
    # ---- nbconvert dependencies ----
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-plain-generic \
    # ----
    tzdata \
    unzip \
    # ---- JSON document parser ---
    jq \
    "

RUN apt-get update \
    && apt-get install -y --no-install-recommends $APT_DEPS \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# ------------------
# Multi-stage-build:
# ------------------

FROM base-builder AS python-builder

# Install Pipenv
# --------------
ARG PIP_NO_CACHE_DIR=0
ARG PIPENV_RELEASE="2020.11.4"
RUN pip install pipenv==$PIPENV_RELEASE

# Install python libs
# -------------------
WORKDIR /tmp/lib
COPY Pipfile* ./
RUN pipenv install --system --deploy


# ------------------
# Multi-stage-build:
# ------------------

FROM base-builder

USER root

# Copy python dependencies
# ------------------------
COPY --from=python-builder $CONDA_DIR/lib/python3.8/site-packages $CONDA_DIR/lib/python3.8/site-packages
RUN fix-permissions $CONDA_DIR/lib/python3.8/site-packages

# Install extensions
# ----------------
# https://github.com/jupyterlab/debugger
# https://www.npmjs.com/package/@jupyterlab/debugger
# https://github.com/plotly/plotly.py
# https://www.npmjs.com/package/jupyterlab-plotly
# https://github.com/voila-dashboards/voila
# https://www.npmjs.com/package/@jupyter-voila/jupyterlab-preview
# https://github.com/dask/dask-labextension
# https://www.npmjs.com/package/dask-labextension
# https://github.com/jupyter-widgets/ipywidgets
# https://www.npmjs.com/package/@jupyter-widgets/jupyterlab-manager
# https://github.com/jupyterlab/jupyterlab-git
# https://www.npmjs.com/package/@jupyterlab/git
# https://github.com/jupytercalpoly/jupyterlab-code-snippets
# https://github.com/jupyterlab/jupyterlab-toc
# https://github.com/aquirdTurtle/Collapsible_Headings

# @jupyterlab/debugger \normally included in lab 3.0. To be tested. TOC removed.
# @jupyterlab/git lab and server extension normally not needed anymore in 0.30 compatible with Lab 3.0

ARG LAB_EXTENSIONS=" \
    @jupyterlab/debugger \
    jupyterlab-plotly \
    plotlywidget \
    @voila-dashboards/jupyterlab-preview \
    dask-labextension \
    @jupyter-widgets/jupyterlab-manager \
    jupyterlab-code-snippets \
    @aquirdturtle/collapsible_headings \
    @jupyterlab/git \
    "


ARG SERVER_EXTENSIONS=" \
    dask_labextension \
    "

RUN jupyter labextension install --no-build --clean $LAB_EXTENSIONS \
    && jupyter serverextension enable $SERVER_EXTENSIONS \
    && rm -rf /tmp/* \
    && rm -rf ${HOME}/.cache ${HOME}/.npm ${HOME}/.yarn \
    && find ${CONDA_DIR} -follow -type f -name '*.a' -delete \
    && find ${CONDA_DIR} -follow -type f -name '*.pyc' -delete \
    && find ${CONDA_DIR} -follow -type f -name '*.js.map' -delete

# Configure extensions
# --------------------
# https://jupyterlab.readthedocs.io/en/stable/user/extensions.html#settings
COPY settings/ ${CONDA_DIR}/share/jupyter/lab/settings

# Build all extensions
# --------------------
ARG NODE_OPTIONS=--max-old-space-size=4096
RUN jupyter lab clean \
    && jupyter lab build --dev-build=False --name='Neptune'

USER $NB_UID
