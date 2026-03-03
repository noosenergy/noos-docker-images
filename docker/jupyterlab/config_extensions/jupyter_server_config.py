from marimo_jupyter_extension.config import (
    MarimoProxyConfig,  # noqa: F401 - needed to register traitlets config class
)

# Explicit marimo path
# c.MarimoProxyConfig.marimo_path = "/opt/bin/marimo"

# Or use uvx mode (runs `uvx marimo` instead)
# c.MarimoProxyConfig.uvx_path = "/usr/local/bin/uvx"

# Do not use marimo sandboxing
# When True, disables --sandbox and skips venv picker (venv selection requires sandbox)
# WARNING: Consider setting up a virtual environment instead of using this flag.
# Sandbox mode enables per-notebook dependency management and venv selection.
c.MarimoProxyConfig.no_sandbox = True

# Startup timeout in seconds (default: 60)
# c.MarimoProxyConfig.timeout = 120
