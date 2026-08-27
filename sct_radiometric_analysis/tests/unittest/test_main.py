# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing SCT Radiometric Analysis main implementation."""

from __future__ import annotations

import builtins
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sct_radiometric_analysis.main import (
    _import_ra_graphs_func,
    _ra_save_and_plot_results,
    full_average_elevation_profiles_analysis,
    full_nesz_analysis,
    full_rain_forest_analysis,
    full_scalloping_analysis,
)


class TestImportRAGraphsFunc:
    """Tests for _import_ra_graphs_func."""

    def test_disabled_returns_none(self):
        assert _import_ra_graphs_func(graphs=False) is None

    @patch("sct_radiometric_analysis.main.sct_logger")
    def test_import_error_raises(self, mock_logger):
        original_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if "graphical_output" in name:
                raise ImportError(f"No module named {name}")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            with pytest.raises(ImportError):
                _import_ra_graphs_func(graphs=True)

        mock_logger.critical.assert_called_once()


class TestRASaveAndPlotResults:
    """Tests for _ra_save_and_plot_results."""

    @patch("sct_radiometric_analysis.main.radiometric_profiles_to_netcdf")
    @patch("sct_radiometric_analysis.main.radiometric_statistical_analysis_to_df")
    @patch("sct_radiometric_analysis.main.sct_logger")
    def test_no_graphs(self, mock_logger, mock_stats_to_df, mock_profiles_to_nc):
        mock_stats_to_df.return_value = MagicMock()
        mock_profiles_to_nc.return_value = Path("/fake/output.nc")
        output = [MagicMock()]
        output_dir = Path("/fake/out")

        nc_result, kpi_result = _ra_save_and_plot_results(
            output=output,
            output_directory=output_dir,
            graphs_func=None,
            tag="NESZ",
            plot_mode="min",
        )

        mock_stats_to_df.assert_called_once_with(data=output)
        mock_profiles_to_nc.assert_called_once_with(data=output, out_path=output_dir, tag="NESZ")
        assert nc_result == Path("/fake/output.nc")
        assert kpi_result == output_dir / "radiometry_statistics.csv"

    @patch("sct_radiometric_analysis.main.radiometric_profiles_to_netcdf")
    @patch("sct_radiometric_analysis.main.radiometric_statistical_analysis_to_df")
    @patch("sct_radiometric_analysis.main.sct_logger")
    def test_with_graphs(self, mock_logger, mock_stats_to_df, mock_profiles_to_nc):
        mock_stats_to_df.return_value = MagicMock()
        mock_profiles_to_nc.return_value = Path("/fake/output.nc")

        item = MagicMock()
        item.general_info.polarization = "VV"
        item.general_info.channel = "CH1"
        output = [item]

        graphs_func = MagicMock()

        nc_result, kpi_result = _ra_save_and_plot_results(
            output=output,
            output_directory=Path("/fake/out"),
            graphs_func=graphs_func,
            tag="SCALLOPING",
            plot_mode="mean",
        )

        mock_stats_to_df.assert_called_once()
        mock_profiles_to_nc.assert_called_once()
        graphs_func.assert_called_once_with(
            data=item,
            out_dir=Path("/fake/out"),
            title="SCALLOPING Profiles CH1",
            plot_mode="mean",
        )
        assert nc_result == Path("/fake/output.nc")


class TestFullNeszAnalysis:
    """Tests for full_nesz_analysis."""

    @patch("sct_radiometric_analysis.main._ra_save_and_plot_results")
    @patch("sct_radiometric_analysis.main.sct_nesz_analysis")
    def test_happy_path(self, mock_nesz, mock_save):
        mock_nesz.return_value = [MagicMock()]
        mock_save.return_value = (Path("/fake/nc"), Path("/fake/kpi"))

        nc, kpi = full_nesz_analysis(
            product=Path("/fake/product"),
            output_directory=Path("/fake/out"),
            config=MagicMock(),
            graphs=False,
        )

        mock_nesz.assert_called_once()
        mock_save.assert_called_once()
        assert nc == Path("/fake/nc")
        assert kpi == Path("/fake/kpi")


class TestFullAverageElevationProfilesAnalysis:
    """Tests for full_average_elevation_profiles_analysis."""

    @patch("sct_radiometric_analysis.main._ra_save_and_plot_results")
    @patch("sct_radiometric_analysis.main.sct_average_elevation_profile_analysis")
    def test_happy_path(self, mock_avg, mock_save):
        mock_avg.return_value = [MagicMock()]
        mock_save.return_value = (Path("/fake/nc"), Path("/fake/kpi"))

        nc, kpi = full_average_elevation_profiles_analysis(
            product=Path("/fake/product"),
            output_radiometric_quantity=MagicMock(),
            output_directory=Path("/fake/out"),
            config=MagicMock(),
            graphs=False,
        )

        mock_avg.assert_called_once()
        mock_save.assert_called_once()
        assert nc == Path("/fake/nc")
        assert kpi == Path("/fake/kpi")


class TestFullRainForestAnalysis:
    """Tests for full_rain_forest_analysis."""

    @patch("sct_radiometric_analysis.main.full_average_elevation_profiles_analysis")
    def test_delegates_to_average_profiles(self, mock_avg):
        mock_avg.return_value = (Path("/fake/nc"), Path("/fake/kpi"))

        nc, kpi = full_rain_forest_analysis(
            product=Path("/fake/product"),
            output_directory=Path("/fake/out"),
            config=MagicMock(),
            graphs=False,
        )

        mock_avg.assert_called_once()
        assert nc == Path("/fake/nc")
        assert kpi == Path("/fake/kpi")


class TestFullScallopingAnalysis:
    """Tests for full_scalloping_analysis."""

    @patch("sct_radiometric_analysis.main._ra_save_and_plot_results")
    @patch("sct_radiometric_analysis.main.sct_scalloping_analysis")
    def test_happy_path(self, mock_scalloping, mock_save):
        mock_scalloping.return_value = [MagicMock()]
        mock_save.return_value = (Path("/fake/nc"), Path("/fake/kpi"))

        nc, kpi = full_scalloping_analysis(
            product=Path("/fake/product"),
            output_directory=Path("/fake/out"),
            config=MagicMock(),
            graphs=False,
        )

        mock_scalloping.assert_called_once()
        mock_save.assert_called_once()
        assert nc == Path("/fake/nc")
        assert kpi == Path("/fake/kpi")
