# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing SCT Spectral Analysis core module."""

from __future__ import annotations

from pathlib import Path

import pytest
from sct.io.io_manager import InvalidProductType

from sct_spectral_analysis.config import SCTSpectralAnalysisConfig


def test_point_target_spectral_analysis_success(mocker, tmp_path):
    mock_product_loader = mocker.patch(
        "sct_spectral_analysis.core.analysis.product_loader", return_value=(mocker.MagicMock(), None)
    )
    mock_extract = mocker.patch(
        "sct_spectral_analysis.core.analysis.extract_point_target_data_from_source",
        return_value=mocker.MagicMock(),
    )
    mock_convert = mocker.patch(
        "sct_spectral_analysis.core.analysis.convert_df_to_nominal_point_target",
        return_value=mocker.MagicMock(),
    )
    mock_pt_analysis = mocker.patch(
        "sct_spectral_analysis.core.analysis.point_target_spectral_analysis",
        return_value=[mocker.MagicMock()],
    )

    from sct_spectral_analysis.core.analysis import sct_point_target_spectral_analysis

    product_path = tmp_path / "product"
    product_path.mkdir()
    target_source = tmp_path / "targets.csv"
    target_source.touch()
    config = SCTSpectralAnalysisConfig()

    result = sct_point_target_spectral_analysis(
        product_path=str(product_path),
        external_target_source=str(target_source),
        config=config,
    )

    mock_product_loader.assert_called_once_with(product_path=Path(str(product_path)))
    mock_extract.assert_called_once_with(source=Path(str(target_source)))
    mock_convert.assert_called_once_with(data_df=mock_extract.return_value)
    mock_pt_analysis.assert_called_once_with(
        product=mock_product_loader.return_value[0],
        point_targets=mock_convert.return_value,
        cropping_size=config.cropping_size,
    )
    assert len(result) == 1


def test_distributed_spectral_analysis_success(mocker, tmp_path):
    mock_product_loader = mocker.patch(
        "sct_spectral_analysis.core.analysis.product_loader", return_value=(mocker.MagicMock(), None)
    )
    mock_dist_analysis = mocker.patch(
        "sct_spectral_analysis.core.analysis.block_wise_distributed_spectral_analysis",
        return_value=[mocker.MagicMock()],
    )

    from sct_spectral_analysis.core.analysis import sct_distributed_spectral_analysis

    product_path = tmp_path / "product"
    product_path.mkdir()
    config = SCTSpectralAnalysisConfig()

    result = sct_distributed_spectral_analysis(
        product_path=str(product_path),
        config=config,
    )

    mock_product_loader.assert_called_once_with(product_path=Path(str(product_path)))
    mock_dist_analysis.assert_called_once_with(
        product=mock_product_loader.return_value[0],
        azimuth_block_size=config.azimuth_block_size,
    )
    assert len(result) == 1


def test_point_target_spectral_analysis_invalid_product(mocker, tmp_path):
    mocker.patch(
        "sct_spectral_analysis.core.analysis.product_loader",
        side_effect=InvalidProductType,
    )

    from sct_spectral_analysis.core.analysis import sct_point_target_spectral_analysis

    product_path = tmp_path / "product"
    product_path.mkdir()
    target_source = tmp_path / "targets.csv"
    target_source.touch()

    with pytest.raises(InvalidProductType):
        sct_point_target_spectral_analysis(
            product_path=str(product_path),
            external_target_source=str(target_source),
        )


def test_distributed_spectral_analysis_invalid_product(mocker, tmp_path):
    mocker.patch(
        "sct_spectral_analysis.core.analysis.product_loader",
        side_effect=InvalidProductType,
    )

    from sct_spectral_analysis.core.analysis import sct_distributed_spectral_analysis

    product_path = tmp_path / "product"
    product_path.mkdir()

    with pytest.raises(InvalidProductType):
        sct_distributed_spectral_analysis(product_path=str(product_path))


def test_point_target_spectral_analysis_default_config(mocker, tmp_path):
    mocker.patch("sct_spectral_analysis.core.analysis.product_loader", return_value=(mocker.MagicMock(), None))
    mocker.patch(
        "sct_spectral_analysis.core.analysis.extract_point_target_data_from_source",
        return_value=mocker.MagicMock(),
    )
    mocker.patch(
        "sct_spectral_analysis.core.analysis.convert_df_to_nominal_point_target",
        return_value=mocker.MagicMock(),
    )
    mock_pt_analysis = mocker.patch(
        "sct_spectral_analysis.core.analysis.point_target_spectral_analysis",
        return_value=[],
    )

    from sct_spectral_analysis.core.analysis import sct_point_target_spectral_analysis

    product_path = tmp_path / "product"
    product_path.mkdir()
    target_source = tmp_path / "targets.csv"
    target_source.touch()

    sct_point_target_spectral_analysis(
        product_path=str(product_path),
        external_target_source=str(target_source),
    )

    default_config = SCTSpectralAnalysisConfig()
    mock_pt_analysis.assert_called_once_with(
        product=mocker.ANY,
        point_targets=mocker.ANY,
        cropping_size=default_config.cropping_size,
    )
