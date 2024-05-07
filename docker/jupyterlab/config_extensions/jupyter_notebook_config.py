# more info:
# https://github.com/finos/jupyterlab_templates

c = get_config()

#------------------------------------------------------------------------------
# Jupyter-templates configuration
#------------------------------------------------------------------------------

# Directory to save templates files
c.JupyterLabTemplates.template_dirs = \
    ['/home/jovyan/.jupyter/lab/user-settings/jupyterlab_templates']
# Do not load default template examples
c.JupyterLabTemplates.include_default = False
c.JupyterLabTemplates.include_core_paths = False
