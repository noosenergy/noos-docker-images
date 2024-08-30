# -----------
# Build stage
# -----------

# https://github.com/jupyter/docker-stacks
# https://hub.docker.com/u/jupyter/
FROM quay.io/jupyter/base-notebook:python-3.11.9 as builder

USER root

# Install Apt packages
# --------------------
COPY build_package.list /tmp/
RUN apt-get update && \
    grep -vE '^#' /tmp/build_package.list | xargs apt-get install -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/fontconfig/*

USER ${NB_UID}

# Install Conda packages
# ----------------------
COPY environment.yml /tmp/
RUN umask 002 && \
    mamba env update -q -f /tmp/environment.yml && \
    mamba clean --all -f -y

# Configure Lab extensions
# ------------------------
# https://jupyterlab.readthedocs.io/en/stable/user/directories.html
COPY lab/config/. ${CONDA_DIR}/etc/jupyter/labconfig
COPY lab/data/. ${CONDA_DIR}/share/jupyter/lab/settings

# Configure Jupyterlab extensions (nbconvert & jupyterlab-templates)
# ------------------------------------------------------------------
COPY config_extensions/. /home/${NB_USER}/.jupyter

# Build Lab extensions
# --------------------
RUN umask 002 && \
    jupyter lab build --dev-build=False && \
    jupyter lab clean 

# Cleanup
# -------
USER root
RUN find ${CONDA_DIR} -follow -type f -name '*.pyc' -delete && \
    find ${CONDA_DIR} -follow -type f -name '*.js.map' -delete && \
    fix-permissions ${CONDA_DIR} && \
    fix-permissions /home/${NB_USER}/.jupyter


# -----------
# Final stage
# -----------

FROM quay.io/jupyter/base-notebook:python-3.11.9

USER root

COPY final_package.list /tmp/
RUN apt-get update && \
    grep -vE '^#' /tmp/final_package.list | xargs apt-get install -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/fontconfig/*

# Make sure we do not keep old folders/files from the jupyterlab/base-notebook image 
# (some existing libs were reinstalled with another version by mamba during the build stage)
RUN rm -rf ${CONDA_DIR} && rm -rf /home/${NB_USER}/.jupyter
COPY --from=builder ${CONDA_DIR} ${CONDA_DIR}
COPY --from=builder /home/${NB_USER}/.jupyter /home/${NB_USER}/.jupyter

USER ${NB_UID}