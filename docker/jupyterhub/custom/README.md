# Custom JupyterHub Templates for Neptune

This repo contains html jinja2 templates for customising the appearance of JupyterHub. Each HTML file here will override the files in `https://github.com/jupyterhub/jupyterhub/tree/master/share/jupyterhub/templates`.

## Usage

Static assets must be in the corresponding static folder: `/usr/local/share/jupyterhub/static/`.
Overriding templates can be linked to in `jupyterhub_config.py`.
