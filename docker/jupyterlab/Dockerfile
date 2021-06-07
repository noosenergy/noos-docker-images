# https://hub.docker.com/u/noosenergy/
# https://github.com/jupyter/docker-stacks
# https://hub.docker.com/u/jupyter/
FROM jupyter/base-notebook:python-3.8.6

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
    && rm -rf /var/lib/apt/lists/* /var/cache/fontconfig/*

# Install Conda packages
# ----------------
COPY environment.yml /tmp/
RUN conda install nomkl \
    && conda env update -q -f /tmp/environment.yml \
    && conda clean --all -f -y \
    && rm -rf /home/$NB_USER/work \
    && find ${CONDA_DIR} -follow -type f -name '*.a' -delete \
    && find ${CONDA_DIR} -follow -type f -name '*.pyc' -delete \
    && find ${CONDA_DIR} -follow -type f -name '*.js.map' -delete \
    && find ${CONDA_DIR}/lib/python*/site-packages/bokeh/server/static -follow -type f -name '*.js' ! -name '*.min.js' -delete \
    && fix-permissions $CONDA_DIR

# Install extensions
# ----------------
# https://github.com/plotly/plotly.py
# https://www.npmjs.com/package/jupyterlab-plotly
# https://github.com/voila-dashboards/voila
# https://www.npmjs.com/package/@jupyter-voila/jupyterlab-preview
# https://github.com/dask/dask-labextension
# https://www.npmjs.com/package/dask-labextension
# https://github.com/jupyter-widgets/ipywidgets
# https://www.npmjs.com/package/@jupyter-widgets/jupyterlab-manager
# https://github.com/jupyterlab/jupyterlab-git
# https://github.com/jupytercalpoly/jupyterlab-code-snippets
# https://github.com/aquirdTurtle/Collapsible_Headings

# jupyterlab can't build with @voila-dashboards/jupyterlab-preview@2.0.1

ARG LAB_EXTENSIONS=" \
    jupyterlab-plotly \
    plotlywidget \
    @voila-dashboards/jupyterlab-preview@2.0.0 \
    dask-labextension \
    @jupyter-widgets/jupyterlab-manager \
    jupyterlab-code-snippets@2.1.0 \
    @aquirdturtle/collapsible_headings \
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
    && find ${CONDA_DIR} -follow -type f -name '*.js.map' -delete \
    && fix-permissions $CONDA_DIR

# Build all extensions
# --------------------
ARG NODE_OPTIONS=--max-old-space-size=4096
RUN jupyter lab clean \
    && jupyter lab build --dev-build=False --name='Neptune'

USER $NB_UID
