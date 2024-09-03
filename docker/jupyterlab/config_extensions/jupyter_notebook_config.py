# more info:
# https://github.com/finos/jupyterlab_templates

c = get_config()

# ------------------------------------------------------------------------------
# Jupyter-templates configuration
# ------------------------------------------------------------------------------

# Directory to save templates files
c.JupyterLabTemplates.template_dirs = [
    "/home/jovyan/.jupyter/lab/user-settings/jupyterlab_templates"
]
# Do not load default template examples
c.JupyterLabTemplates.include_default = False
c.JupyterLabTemplates.include_core_paths = False

# Disable launching browser by redirect file
# For versions of notebook > 5.7.2, a security feature measure was added that
# prevented the authentication token used to launch the browser from being visible.
# This feature makes it difficult for other users on a multi-user system from
# running code in your Jupyter session as you.
# However, some environments (like Windows Subsystem for Linux (WSL) and Chromebooks),
# launching a browser using a redirect file can lead the browser failing to load.
# This is because of the difference in file structures/paths between the runtime and
# the browser.
# Disabling this setting to False will disable this behavior, allowing the browser
# to launch by using a URL and visible token (as before).
c.ServerApp.use_redirect_file = False
