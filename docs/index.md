---
icon: lucide/rocket
title: "Analyses Plugins"
---

# Quality Analyses Plugins

Welcome to the official Quality Analyses Plugins documentation for the [SCT (SAR Calibration Toolbox)](https://opensource.aresys.it/sct/)
python ecosystem.

This documentation hub collects the documentation for all the quality analyses plugins developed so far, providing
a small overview of the functionalities of the available plugins, their structure and usage and the python API references.

<figure markdown="span">
    ![Analyses Plugins](assets/images/plugin.png){ width="800" }
    <figcaption>Analyses plugins.</figcaption>
</figure>

Here you will find:

* A list of all the quality analyses plugins available in the ecosystem
* Description of the plugins system and architecture
* A guide to create your own plugins

## Available Plugins

Here is an up-to-date list of the available plugins:

| Analysis Scope | Package Name | Documentation |
| ----------- | --------- | --------- |
| Point Target | *sct-point-target-analysis* | [Point Target Plugin](./plugins/point-target/pt.md) |
| Radiometry | *sct-radiometric-analysis* | [Radiometric Plugin](./plugins/radiometry/rad.md) |
| Spectra | *sct-spectral-analysis* | [Spectral Plugin](./plugins/spectra/spectra.md) |
| Elevation Notch | *sct-notch-analysis* | [Notch Plugin](./plugins/notch/notch.md) |
| Interferometry | *sct-interferometric-analysis* | [Interferometric Plugin](./plugins/interferometry/interf.md) |
| Ambiguity Ratio | *sct-ambiguities-analysis* | [Ambiguities Plugin](./plugins/ambiguities/ar.md) |

## Installation

Each plugin can be installed separately as it is a full fledged standalone python package. All plugins are available on
[PyPI](https://pypi.org/user/aresys/) and can be installed using ``pip``.

> Refer to the [installation](./install.md) page for more details.

!!! note

    Few SCT analyses plugins can be installed directly when installing SCT itself using the dedicated optional dependency
    group. Refer to the [SCT installation guide](https://opensource.aresys.it/sct/install/) page for more details.
