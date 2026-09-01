# SCT Analyses Plugins

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://python.org)
[![Docs](https://img.shields.io/badge/docs-github.io-blue)](https://opensource.aresys.it/sct_plugins_analyses)

**SAR** L1 quality assessment analyses plugins collection for [SCT (SAR Calibration Toolbox)](https://github.com/aresys-srl/sct).

This repository is a monorepo consisting of several standalone Python packages, each dedicated to a specific
analysis method applied to Level 1 SAR products. Plugins integrate with SCT via a unified protocol, enabling
a wide range of quality assessment and calibration analyses regardless of the input format.

## Available Plugins

| Package                          | PyPI                                                                                                                          | CI                                                                                                                                                                                                  | Description                                                       |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **sct-point-target-analysis**    | [![PyPI](https://img.shields.io/pypi/v/sct-point-target-analysis)](https://pypi.org/project/sct-point-target-analysis/)       | [![CI](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/point_target.yml/badge.svg)](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/point_target.yml)     | Point Target Analysis of L1 SAR Products                          |
| **sct-radiometric-analysis**     | [![PyPI](https://img.shields.io/pypi/v/sct-radiometric-analysis)](https://pypi.org/project/sct-radiometric-analysis/)         | [![CI](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/radiometry.yml/badge.svg)](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/radiometry.yml)         | Distributed Radiometric Analysis of L1 SAR Products               |
| **sct-spectral-analysis**        | [![PyPI](https://img.shields.io/pypi/v/sct-spectral-analysis)](https://pypi.org/project/sct-spectral-analysis/)               | [![CI](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/spectra.yml/badge.svg)](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/spectra.yml)               | Point and Distributed Target Spectral Analysis of L1 SAR Products |
| **sct-interferometric-analysis** | [![PyPI](https://img.shields.io/pypi/v/sct-interferometric-analysis)](https://pypi.org/project/sct-interferometric-analysis/) | [![CI](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/interferometry.yml/badge.svg)](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/interferometry.yml) | Interferometric Analysis of L1 SAR Products                       |
| **sct-ambiguities-analysis**     | [![PyPI](https://img.shields.io/pypi/v/sct-ambiguities-analysis)](https://pypi.org/project/sct-ambiguities-analysis/)         | [![CI](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/ambiguities.yml/badge.svg)](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/ambiguities.yml)       | Ambiguity Ratio Analysis of L1 SAR Products                       |
| **sct-notch-analysis**           | [![PyPI](https://img.shields.io/pypi/v/sct-notch-analysis)](https://pypi.org/project/sct-notch-analysis/)                     | [![CI](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/notch.yml/badge.svg)](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/notch.yml)                   | Elevation Notch Analysis of L1 SAR Products                       |

## Documentation

Full documentation is available at [https://opensource.aresys.it/sct_plugins_analyses](https://opensource.aresys.it/sct_plugins_analyses).

## Installation

Each plugin is a standalone Python package available on [PyPI](https://pypi.org/user/aresys/) and can be installed
using ``pip``:

``` bash
pip install <package-name>
```

## License

All plugins in this repository are licensed under the **MIT License**.

## Contributing

Contributions are welcome! If you encounter a bug, have a feature request, or want to contribute code:

- **Report bugs & request features**: open an issue on [GitHub](https://github.com/aresys-srl/sct_plugins_analyses/issues).
  Include a clear description, steps to reproduce, and your environment details.
- **Submit changes**: fork the repository, create a feature branch, and open a pull request. Ensure your code passes
  the existing linting and test suite.
- **Questions**: use GitHub Discussions for general questions and discussions.

## Copyright

Copyright &copy; 2026-present Aresys S.r.l. <info@aresys.it>
