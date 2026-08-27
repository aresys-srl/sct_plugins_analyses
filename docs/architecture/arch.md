---
icon: lucide/landmark
---

# Plugin Architecture

SCT supports multiple quality analyses algorithms through a **plugin-based architecture**.
Instead of embedding analysis-specific logic directly in the core library, analyses are handled by **external plugin packages**
that implement a common interface.

This page explains how to create and distribute a new **Quality Analysis Plugin** for SCT.

## Overview

An SCT analysis plugin is a **separate Python package** that:

1. Implements the ``sct.plugins.protocols.AnalysisPluginProtocol``.
2. Exposes the plugin class through a **Python entry point** in the ``sct.analyses`` namespace.
3. Is installed alongside SCT so it can be **automatically discovered**.

Once installed, SCT will detect the plugin at runtime and make it available to the analysis pipeline.

??? info "Analysis Algorithm vs Plugin"

    The plugin itself does not necessarily need to implement all the low-level logic required to perform the analysis.
    In many cases, existing plugins rely on external libraries such as [Perseo-Quality](https://opensource.aresys.it/perseo/documentation/quality/) 
    to handle the algorithm definition and parameters tuning for the given analysis. The plugin acts primarily as an adapter layer:
    it uses external tools or libraries to process data and then wrap and re-organize input and output conforming to the
    SCT internal data model required.

## Package Structure

A minimal plugin package may look like the following:

```
📁 root
├── 📁 src
│   └── 📁 sct_<analysis_name>_analysis
│       ├── 🐍 __init__.py
│       ├── 🐍 interface.py
│       ├── 🐍 cli.py
│       ├── 🐍 config.py
│       ├── 🐍 testing.py
│       └── 🐍 main.py
├── ⚙️ pyproject.toml
├── 📄 LICENSE.txt
└── 📄 README.md
```

Typical responsibilities:

- ``interface.py``: defines the plugin class implementing the SCT Analysis protocol.
- ``main.py``: contains the full analysis logic pipeline implementation API entry point.
- ``config.py``: defines the analysis configuration class and its schema.
- ``testing.py``: defines the analysis testing class and its schema.
- ``cli.py``: defines the analysis CLI commands that will be available in the SCT CLI.
- ``pyproject.toml``: declares the plugin entry point.
