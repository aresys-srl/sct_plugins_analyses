# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing SCT Spectral Analysis main module."""

from __future__ import annotations

import pytest


def test_full_spectral_analysis_distributed(mocker, tmp_path):
    mock_dist = mocker.patch(
        "sct_spectral_analysis.main.sct_distributed_spectral_analysis",
        return_value=[mocker.MagicMock()],
    )
    mock_pt = mocker.patch(
        "sct_spectral_analysis.main.sct_point_target_spectral_analysis",
    )
    mock_to_netcdf = mocker.patch(
        "sct_spectral_analysis.main.spectral_analysis_profiles_to_netcdf",
        return_value=tmp_path / "output.nc",
    )
    mock_graphs_import = mocker.patch(
        "sct_spectral_analysis.main._import_spectral_graphs_func",
        return_value=None,
    )

    from sct_spectral_analysis.main import full_spectral_analysis

    product = tmp_path / "product"
    product.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    result = full_spectral_analysis(
        product=product,
        point_target_source=None,
        output_directory=output_dir,
        config=None,
        graphs=False,
    )

    mock_dist.assert_called_once_with(product_path=product, config=None)
    mock_pt.assert_not_called()
    mock_to_netcdf.assert_called_once_with(data=mock_dist.return_value, out_path=output_dir)
    mock_graphs_import.assert_called_once_with(False)
    assert result == tmp_path / "output.nc"


def test_full_spectral_analysis_point_target(mocker, tmp_path):
    mock_dist = mocker.patch(
        "sct_spectral_analysis.main.sct_distributed_spectral_analysis",
    )
    mock_pt = mocker.patch(
        "sct_spectral_analysis.main.sct_point_target_spectral_analysis",
        return_value=[mocker.MagicMock()],
    )
    mock_to_netcdf = mocker.patch(
        "sct_spectral_analysis.main.spectral_analysis_profiles_to_netcdf",
        return_value=tmp_path / "output.nc",
    )
    mock_graphs_import = mocker.patch(
        "sct_spectral_analysis.main._import_spectral_graphs_func",
        return_value=None,
    )

    from sct_spectral_analysis.main import full_spectral_analysis

    product = tmp_path / "product"
    product.mkdir()
    point_targets = tmp_path / "targets.csv"
    point_targets.touch()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    result = full_spectral_analysis(
        product=product,
        point_target_source=point_targets,
        output_directory=output_dir,
        config=None,
        graphs=False,
    )

    mock_pt.assert_called_once_with(
        product_path=product,
        external_target_source=point_targets,
        config=None,
    )
    mock_dist.assert_not_called()
    mock_to_netcdf.assert_called_once_with(data=mock_pt.return_value, out_path=output_dir)
    mock_graphs_import.assert_called_once_with(False)
    assert result == tmp_path / "output.nc"


def test_full_spectral_analysis_with_graphs(mocker, tmp_path):
    mock_graph_func = mocker.MagicMock()
    mock_dist = mocker.patch(
        "sct_spectral_analysis.main.sct_distributed_spectral_analysis",
        return_value=[mocker.MagicMock()],
    )
    mocker.patch(
        "sct_spectral_analysis.main.spectral_analysis_profiles_to_netcdf",
        return_value=tmp_path / "output.nc",
    )
    mocker.patch(
        "sct_spectral_analysis.main._import_spectral_graphs_func",
        return_value=mock_graph_func,
    )

    from sct_spectral_analysis.main import full_spectral_analysis

    product = tmp_path / "product"
    product.mkdir()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    full_spectral_analysis(
        product=product,
        point_target_source=None,
        output_directory=output_dir,
        config=None,
        graphs=True,
    )

    expected_graphs_dir = output_dir / "graphs"
    assert expected_graphs_dir.exists()
    mock_graph_func.assert_called_once_with(data=mock_dist.return_value, output_dir=expected_graphs_dir)


def test_import_spectral_graphs_func_disabled(mocker):
    from sct_spectral_analysis.main import _import_spectral_graphs_func

    result = _import_spectral_graphs_func(graphs=False)
    assert result is None


def test_import_spectral_graphs_func_import_error(mocker):
    import builtins

    original_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if "perseo_quality.spectral_analysis.graphical_output" in name:
            raise ImportError("Missing dependency")
        return original_import(name, *args, **kwargs)

    mocker.patch.object(builtins, "__import__", mock_import)

    from sct_spectral_analysis.main import _import_spectral_graphs_func

    with pytest.raises(ImportError):
        _import_spectral_graphs_func(graphs=True)
