FROM jupyterhub/k8s-hub:0.10.3

# https://github.com/jupyter/docker-stacks
# https://hub.docker.com/u/jupyterhub/

USER root

# Copy custom assets
# --------------------
# https://jupyterlab.readthedocs.io/en/stable/user/extensions.html#settings
COPY custom /usr/local/share/jupyterhub/custom

USER $NB_UID
