---
icon: lucide/arrow-big-down-dash
---

# Installation

All official SCT plugins are available on [PyPI](https://pypi.org/user/aresys/) and can be installed using ``pip`` or any other
python package manager.

## Installing from PyPI

!!! note

    Few SCT analyses plugins can be installed directly when installing SCT itself using the dedicated optional dependency
    group. Refer to the [SCT installation guide](https://opensource.aresys.it/sct/install/) page for more details.

To install a plugin from PyPI, you can use the following command:

```bash
pip install sct-<name>-analysis
```

where `<name>` is the name of the plugin you want to install. The list of available plugins [can be found here](./index.md#available-plugins).

!!! important "Virtual Environments"
    We recommend using a dedicated virtual environment to install the plugins and the main SCT software.  
    This will ensure that the plugin is installed in a separate environment and avoids conflicts with other packages
    or dependencies.
