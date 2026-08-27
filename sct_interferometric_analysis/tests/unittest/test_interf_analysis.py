# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing SCT Interferometric Analysis core analysis module."""

from __future__ import annotations

from pathlib import Path

import pytest
from sct.io.io_manager import InvalidProductType

from sct_interferometric_analysis.config import SCTInterferometricAnalysisConfig
from sct_interferometric_analysis.core.analysis import sct_interferometric_coherence_analysis


@pytest.fixture
def mock_product_loader(mocker):
    mock_product = mocker.MagicMock()
    mock_product.name = "test_product"
    mock_product.channels_list = []
    return mocker.patch(
        "sct_interferometric_analysis.core.analysis.product_loader",
        return_value=(mock_product, None),
    )


@pytest.fixture
def mock_analysis_func(mocker):
    return mocker.patch(
        "sct_interferometric_analysis.core.analysis.interferometric_analysis",
        return_value=[],
    )


def test_default_config_when_none(mock_product_loader, mock_analysis_func):
    result = sct_interferometric_coherence_analysis(
        product_path=Path("dummy_product"),
        config=None,
    )
    assert result == []
    mock_product_loader.assert_called_once()
    mock_analysis_func.assert_called_once()


def test_with_second_product_path(mocker, mock_analysis_func):
    mock_product = mocker.MagicMock()
    mock_product.name = "test_product"
    mock_product.channels_list = []
    mocker.patch(
        "sct_interferometric_analysis.core.analysis.product_loader",
        return_value=(mock_product, None),
    )

    config = SCTInterferometricAnalysisConfig()
    config.base_config.enable_coherence_computation = False

    sct_interferometric_coherence_analysis(
        product_path=Path("dummy_product"),
        second_product_path=Path("dummy_product_2"),
        config=config,
    )

    assert config.base_config.enable_coherence_computation is True
    mock_analysis_func.assert_called_once()


def test_invalid_first_product(mocker):
    mocker.patch(
        "sct_interferometric_analysis.core.analysis.product_loader",
        side_effect=InvalidProductType("invalid product"),
    )

    with pytest.raises(InvalidProductType):
        sct_interferometric_coherence_analysis(
            product_path=Path("invalid_product"),
            config=SCTInterferometricAnalysisConfig(),
        )


def test_invalid_second_product(mocker):
    mock_product = mocker.MagicMock()
    mock_product.name = "test_product"
    mock_product.channels_list = []

    mocker.patch(
        "sct_interferometric_analysis.core.analysis.product_loader",
        side_effect=[(mock_product, None), InvalidProductType("invalid product")],
    )

    with pytest.raises(InvalidProductType):
        sct_interferometric_coherence_analysis(
            product_path=Path("valid_product"),
            second_product_path=Path("invalid_product"),
            config=SCTInterferometricAnalysisConfig(),
        )


def test_successful_result(mock_product_loader, mocker):
    expected_result = mocker.MagicMock()
    mocker.patch(
        "sct_interferometric_analysis.core.analysis.interferometric_analysis",
        return_value=[expected_result],
    )

    result = sct_interferometric_coherence_analysis(
        product_path=Path("valid_product"),
        config=SCTInterferometricAnalysisConfig(),
    )

    assert result == [expected_result]
