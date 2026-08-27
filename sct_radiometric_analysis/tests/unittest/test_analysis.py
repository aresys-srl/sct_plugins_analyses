# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing SCT Radiometric Analysis core."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sct_radiometric_analysis.config import SCTRadiometricAnalysisConfig
from sct_radiometric_analysis.core.analysis import (
    SupportedRadiometricProfiles,
    sct_average_elevation_profile_analysis,
    sct_nesz_analysis,
    sct_radiometric_profiles,
    sct_scalloping_analysis,
)


class TestSCTRadiometricProfiles:
    """Tests for sct_radiometric_profiles dispatch."""

    @patch("sct_radiometric_analysis.core.analysis.product_loader")
    @patch("sct_radiometric_analysis.core.analysis.nesz_profiles")
    def test_nesz_branch(self, mock_nesz, mock_loader):
        mock_product = MagicMock()
        mock_loader.return_value = (mock_product, None)
        mock_nesz.return_value = [MagicMock()]
        config = MagicMock()

        result = sct_radiometric_profiles(
            product_path=Path("/fake/product"),
            analysis_type=SupportedRadiometricProfiles.NESZ,
            config=config,
        )

        mock_loader.assert_called_once()
        mock_nesz.assert_called_once_with(product=mock_product, config=config)
        assert len(result) == 1

    @patch("sct_radiometric_analysis.core.analysis.product_loader")
    @patch("sct_radiometric_analysis.core.analysis.average_elevation_profiles")
    def test_profiles_branch(self, mock_profiles, mock_loader):
        mock_product = MagicMock()
        mock_loader.return_value = (mock_product, None)
        mock_profiles.return_value = [MagicMock()]
        config = MagicMock()
        output_quantity = MagicMock()

        result = sct_radiometric_profiles(
            product_path=Path("/fake/product"),
            analysis_type=SupportedRadiometricProfiles.PROFILES,
            config=config,
            output_quantity=output_quantity,
        )

        mock_loader.assert_called_once()
        mock_profiles.assert_called_once_with(product=mock_product, output_quantity=output_quantity, config=config)
        assert len(result) == 1

    @patch("sct_radiometric_analysis.core.analysis.product_loader")
    @patch("sct_radiometric_analysis.core.analysis.scalloping_profiles")
    def test_scalloping_branch(self, mock_scalloping, mock_loader):
        mock_product = MagicMock()
        mock_loader.return_value = (mock_product, None)
        mock_scalloping.return_value = [MagicMock()]
        config = MagicMock()

        result = sct_radiometric_profiles(
            product_path=Path("/fake/product"),
            analysis_type=SupportedRadiometricProfiles.SCALLOPING,
            config=config,
        )

        mock_loader.assert_called_once()
        mock_scalloping.assert_called_once_with(product=mock_product, config=config)
        assert len(result) == 1

    @patch("sct_radiometric_analysis.core.analysis.product_loader")
    def test_invalid_product_type_raises(self, mock_loader):
        from sct.io.io_manager import InvalidProductType

        mock_loader.side_effect = InvalidProductType

        with pytest.raises(InvalidProductType):
            sct_radiometric_profiles(
                product_path=Path("/fake/product"),
                analysis_type=SupportedRadiometricProfiles.NESZ,
                config=MagicMock(),
            )

    @patch("sct_radiometric_analysis.core.analysis.product_loader")
    @patch("sct_radiometric_analysis.core.analysis.sct_logger")
    def test_invalid_product_type_logs(self, mock_logger, mock_loader):
        from sct.io.io_manager import InvalidProductType

        mock_loader.side_effect = InvalidProductType

        with pytest.raises(InvalidProductType):
            sct_radiometric_profiles(
                product_path=Path("/fake/product"),
                analysis_type=SupportedRadiometricProfiles.NESZ,
                config=MagicMock(),
            )

        assert mock_logger.critical.call_count == 2


class TestSCTNeszAnalysis:
    """Tests for sct_nesz_analysis."""

    @patch("sct_radiometric_analysis.core.analysis.sct_radiometric_profiles")
    def test_with_explicit_config(self, mock_radiometric):
        mock_radiometric.return_value = [MagicMock()]
        config = SCTRadiometricAnalysisConfig()

        result = sct_nesz_analysis(product_path=Path("/fake/product"), config=config)

        mock_radiometric.assert_called_once_with(
            product_path=Path("/fake/product"),
            analysis_type=SupportedRadiometricProfiles.NESZ,
            config=config.base_config,
        )
        assert len(result) == 1

    @patch("sct_radiometric_analysis.core.analysis.sct_radiometric_profiles")
    def test_default_config(self, mock_radiometric):
        mock_radiometric.return_value = [MagicMock()]

        result = sct_nesz_analysis(product_path=Path("/fake/product"), config=None)

        mock_radiometric.assert_called_once()
        assert len(result) == 1


class TestSCTAverageElevationProfileAnalysis:
    """Tests for sct_average_elevation_profile_analysis."""

    @patch("sct_radiometric_analysis.core.analysis.sct_radiometric_profiles")
    def test_with_explicit_config(self, mock_radiometric):
        mock_radiometric.return_value = [MagicMock()]
        config = SCTRadiometricAnalysisConfig()
        output_quantity = MagicMock()

        result = sct_average_elevation_profile_analysis(
            product_path=Path("/fake/product"),
            output_quantity=output_quantity,
            config=config,
        )

        mock_radiometric.assert_called_once_with(
            product_path=Path("/fake/product"),
            output_quantity=output_quantity,
            analysis_type=SupportedRadiometricProfiles.PROFILES,
            config=config.base_config,
        )
        assert len(result) == 1

    @patch("sct_radiometric_analysis.core.analysis.sct_radiometric_profiles")
    def test_default_config(self, mock_radiometric):
        mock_radiometric.return_value = [MagicMock()]

        result = sct_average_elevation_profile_analysis(
            product_path=Path("/fake/product"),
            output_quantity=MagicMock(),
            config=None,
        )

        mock_radiometric.assert_called_once()
        assert len(result) == 1


class TestSCTScallopingAnalysis:
    """Tests for sct_scalloping_analysis."""

    @patch("sct_radiometric_analysis.core.analysis.sct_radiometric_profiles")
    def test_with_explicit_config(self, mock_radiometric):
        mock_radiometric.return_value = [MagicMock()]
        config = SCTRadiometricAnalysisConfig()

        result = sct_scalloping_analysis(product_path=Path("/fake/product"), config=config)

        mock_radiometric.assert_called_once_with(
            product_path=Path("/fake/product"),
            analysis_type=SupportedRadiometricProfiles.SCALLOPING,
            config=config.base_config,
        )
        assert len(result) == 1

    @patch("sct_radiometric_analysis.core.analysis.sct_radiometric_profiles")
    def test_default_config(self, mock_radiometric):
        mock_radiometric.return_value = [MagicMock()]

        result = sct_scalloping_analysis(product_path=Path("/fake/product"), config=None)

        mock_radiometric.assert_called_once()
        assert len(result) == 1
