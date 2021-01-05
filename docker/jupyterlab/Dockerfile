FROM jupyter/base-notebook:python-3.8.6

# https://github.com/jupyter/docker-stacks
# https://hub.docker.com/u/jupyter/

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

# Install packages
# ----------------
COPY environment.yml /tmp/
RUN conda env update -q -f /tmp/environment.yml \
    && conda clean --all -f -y \
    && fix-permissions $CONDA_DIR \
    && rm -rf /home/$NB_USER/work \
    && fix-permissions /home/$NB_USER

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

ARG LAB_EXTENSIONS=" \
    @jupyterlab/debugger \
    @jupyter-voila/jupyterlab-preview \
    dask-labextension \
    @jupyter-widgets/jupyterlab-manager \
    @jupyterlab/git \
    jupyterlab-code-snippets \
    @jupyterlab/toc \
    @aquirdturtle/collapsible_headings \
    "


ARG SERVER_EXTENSIONS=" \
    dask_labextension \
    jupyterlab_git \
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

# Configure snippets extension
# ------------------------
COPY snippets/ /home/$NB_USER/snippets

USER $NB_UID
