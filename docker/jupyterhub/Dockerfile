# hub image in sync with helm chart in repo neptune-jupyter-hub
FROM jupyterhub/k8s-hub:0.10.3

# https://github.com/jupyter/docker-stacks
# https://hub.docker.com/u/jupyterhub/

USER root

# Copy custom extra-assets
# --------------------
# https://jupyterlab.readthedocs.io/en/stable/user/extensions.html#settings
COPY custom/templates /usr/local/share/jupyterhub/custom_templates
COPY custom/assets /usr/local/share/jupyterhub/static/custom

USER $NB_UID
