# https://github.com/jupyter/docker-stacks
# https://hub.docker.com/u/jupyter/
FROM jupyter/base-notebook:python-3.11.4

USER root

# Install Apt packages
# --------------------
COPY package.list /tmp/
RUN apt-get update && \
    grep -vE '^#' /tmp/package.list | xargs apt-get install -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/fontconfig/*

# Install Conda packages
# ----------------------
COPY environment.yml /tmp/
RUN mamba env update -q -f /tmp/environment.yml && \
    mamba clean --all -f -y

# Configure Lab extensions
# ------------------------
# https://jupyterlab.readthedocs.io/en/stable/user/directories.html
COPY lab/config/. ${CONDA_DIR}/etc/jupyter/labconfig
COPY lab/data/. ${CONDA_DIR}/share/jupyter/lab/settings

# Configure Jupyterlab extensions (nbconvert & jupyterlab-templates)
# ------------------------------------------------------------------
COPY config_extensions/. ${HOME}/.jupyter

# Cleanup
# -------
RUN rm -rf /tmp/* && \
    rm -rf ${HOME}/work ${HOME}/.cache ${HOME}/.npm ${HOME}/.yarn && \
    find ${CONDA_DIR} -follow -type f -name '*.pyc' -delete && \
    find ${CONDA_DIR} -follow -type f -name '*.js.map' -delete && \
    fix-permissions $CONDA_DIR

# Build Lab extensions
# --------------------
RUN jupyter lab clean && \
    jupyter lab build --dev-build=False

USER $NB_UID
