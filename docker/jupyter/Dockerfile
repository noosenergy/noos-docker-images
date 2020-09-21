FROM jupyter/base-notebook:python-3.7.6

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
    texlive-fonts-extra \
    # ----
    tzdata \
    unzip \
    nano \
    # ---- JSON document parser ---
    jq \
    "
RUN apt-get update \
    && apt-get install -y --no-install-recommends $APT_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Install packages
# ----------------
COPY environment.yml /tmp/
RUN conda env update -q -f /tmp/environment.yml

# Install debugger
# ----------------
# https://github.com/jupyterlab/debugger
# https://www.npmjs.com/package/@jupyterlab/debugger
RUN jupyter labextension install @jupyterlab/debugger --no-build

# Install plotly
# --------------
# https://github.com/plotly/plotly.py
# https://www.npmjs.com/package/jupyterlab-plotly
RUN jupyter labextension install jupyterlab-plotly --no-build

# Install voila
# -------------
# https://github.com/voila-dashboards/voila
# https://www.npmjs.com/package/@jupyter-voila/jupyterlab-preview
RUN jupyter labextension install @jupyter-voila/jupyterlab-preview --no-build

# Install dask
# ------------
# https://github.com/dask/dask-labextension
# https://www.npmjs.com/package/dask-labextension
RUN jupyter labextension install dask-labextension --no-build && \
    jupyter serverextension enable dask_labextension --py --sys-prefix

# Install ipywidgets
# -------------------
# https://github.com/jupyter-widgets/ipywidgets
# https://www.npmjs.com/package/@jupyter-widgets/jupyterlab-manager
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager --no-build

# Install jupyterlab-git
# ----------------------
# https://github.com/jupyterlab/jupyterlab-git
# https://www.npmjs.com/package/@jupyterlab/git
RUN jupyter labextension install @jupyterlab/git --no-build && \
    jupyter serverextension enable jupyterlab_git --py --sys-prefix

# TODO: investigate compatibility with Jupyter Lab > 2.0
# Install jupyterlab-sql
# ----------------------
# (with tentaclio support)
# https://github.com/octoenergy/jupyterlab-sql/tree/tentaclio
# RUN git clone -b tentaclio https://github.com/octoenergy/jupyterlab-sql.git /tmp/hub/jupyterlab-sql
# RUN pip install /tmp/hub/jupyterlab-sql && \
#     jupyter labextension install /tmp/hub/jupyterlab-sql --no-build && \
#     jupyter serverextension enable jupyterlab_sql --py --sys-prefix

# Build all extensions
# --------------------
ARG NODE_OPTIONS=--max-old-space-size=4096
RUN jupyter lab build

# Fix dir permissions
# -------------------
RUN conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

USER $NB_UID
