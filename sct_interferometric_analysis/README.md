# SCT Plugin: Interferometric Analysis

[![PyPI version](https://img.shields.io/pypi/v/sct-interferometric-analysis)](https://pypi.org/project/sct-interferometric-analysis/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)

[![CI](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/interferometry.yml/badge.svg)](https://github.com/aresys-srl/sct_plugins_analyses/actions/workflows/interferometry.yml)

[SCT (SAR Calibration Toolbox)](https://github.com/aresys-srl/sct) plugin for performing
Interferometric Analysis on L1 SAR products. Enables interferometric quality assessment
including coherence and phase analysis through SCT.

## Installation

``` bash
pip install sct-interferometric-analysis
```

SCT is automatically installed as a dependency.

## Compatibility

This plugin must be installed in the same Python environment as SCT. Once installed,
the plugin is automatically discovered and registered by SCT through its entry-point
based plugin system; no additional configuration is required.

## Documentation

- [SCT documentation](https://opensource.aresys.it/sct/)
- [Quality Analysis documentation](https://opensource.aresys.it/perseo/documentation/quality/)
- [Analysis Plugins documentation](https://opensource.aresys.it/sct_plugins_analyses)

## License

This project is licensed under the MIT License. See the [LICENSE.txt](LICENSE.txt) file for details.

Copyright &copy; 2026-present Aresys S.r.l. <info@aresys.it>
