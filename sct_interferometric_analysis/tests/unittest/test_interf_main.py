# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing SCT Interferometric Analysis main module."""

from __future__ import annotations

from pathlib import Path

import pytest

from sct_interferometric_analysis.config import SCTInterferometricAnalysisConfig
from sct_interferometric_analysis.main import (
    _import_interf_graphs_func,
    full_interferometric_analysis,
)


@pytest.fixture
def mock_coherence_analysis(mocker):
    result = mocker.MagicMock()
    return mocker.patch(
        "sct_interferometric_analysis.main.sct_interferometric_coherence_analysis",
        return_value=[result],
    )


@pytest.fixture
def mock_netcdf_export(mocker):
    return mocker.patch(
        "sct_interferometric_analysis.main.coherence_histograms_to_netcdf",
        return_value=Path("output/coherence_histograms.nc"),
    )


def test_full_analysis_no_graphs(mock_coherence_analysis, mock_netcdf_export):
    result = full_interferometric_analysis(
        product=Path("dummy_product"),
        product_2=None,
        output_directory=Path("output"),
        config=SCTInterferometricAnalysisConfig(),
        graphs=False,
    )

    assert result == Path("output/coherence_histograms.nc")
    mock_coherence_analysis.assert_called_once()
    mock_netcdf_export.assert_called_once()


def test_full_analysis_with_graphs(mocker, mock_coherence_analysis, mock_netcdf_export):
    mock_graphs_func = mocker.MagicMock()
    mocker.patch(
        "perseo_quality.interferometric_analysis.graphical_output.generate_coherence_graphs",
        mock_graphs_func,
    )

    result = full_interferometric_analysis(
        product=Path("dummy_product"),
        product_2=None,
        output_directory=Path("output"),
        config=SCTInterferometricAnalysisConfig(),
        graphs=True,
    )

    assert result == Path("output/coherence_histograms.nc")
    assert mock_graphs_func.call_count == 2
    mock_graphs_func.assert_any_call(
        data=mock_coherence_analysis.return_value[0],
        output_dir=Path("output"),
        mode="magnitude",
        config=mocker.ANY,
    )
    mock_graphs_func.assert_any_call(
        data=mock_coherence_analysis.return_value[0],
        output_dir=Path("output"),
        mode="phase",
        config=mocker.ANY,
    )


def test_import_graphs_func_error(mocker):
    import builtins

    original_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if "graphical_output" in name:
            raise ImportError(f"No module named {name}")
        return original_import(name, *args, **kwargs)

    mocker.patch("builtins.__import__", side_effect=mock_import)

    with pytest.raises(ImportError):
        _import_interf_graphs_func(graphs=True)
