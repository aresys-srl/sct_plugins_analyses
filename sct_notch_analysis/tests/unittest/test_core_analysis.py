# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing SCT Elevation Notch Analysis core."""

from __future__ import annotations

from pathlib import Path

import pytest
from sct.io.io_manager import InvalidProductType

from sct_notch_analysis.core.analysis import sct_elevation_notch_analysis


class TestSCTElevationNotchAnalysis:
    """Tests for sct_elevation_notch_analysis error paths."""

    def test_invalid_product_type(self, mocker) -> None:
        """InvalidProductType from product_loader should propagate."""
        mocker.patch(
            "sct_notch_analysis.core.analysis.product_loader",
            side_effect=InvalidProductType("unknown product"),
        )
        with pytest.raises(InvalidProductType):
            sct_elevation_notch_analysis(product_path=Path("/nonexistent"))

    def test_antenna_pattern_load_error(self, mocker) -> None:
        """Exception from read_antenna_pattern_netcdf should raise RuntimeError."""
        mocker.patch(
            "sct_notch_analysis.core.analysis.product_loader",
            return_value=(mocker.MagicMock(), mocker.MagicMock()),
        )
        mocker.patch(
            "sct_notch_analysis.core.analysis.read_antenna_pattern_netcdf",
            side_effect=ValueError("corrupted file"),
        )
        with pytest.raises(RuntimeError):
            sct_elevation_notch_analysis(
                product_path=Path("/some/product"),
                antenna_pattern_file=Path("/some/antenna.nc"),
            )
