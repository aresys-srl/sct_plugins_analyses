# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing core analysis module."""

from __future__ import annotations

from pathlib import Path

import pytest

from sct_ambiguities_analysis.core.analysis import sct_point_target_ambiguity_ratio_analysis


def test_happy_path(mocker) -> None:
    mock_product = mocker.MagicMock()
    mock_product_loader = mocker.patch(
        "sct_ambiguities_analysis.core.analysis.product_loader",
        return_value=(mock_product, None),
    )
    mock_extract = mocker.patch(
        "sct_ambiguities_analysis.core.analysis.extract_point_target_data_from_source",
        return_value=mocker.MagicMock(),
    )
    mock_convert = mocker.patch(
        "sct_ambiguities_analysis.core.analysis.convert_df_to_nominal_point_target",
        return_value=mocker.MagicMock(),
    )
    mock_perseo = mocker.patch(
        "sct_ambiguities_analysis.core.analysis.point_target_ambiguity_ratio_analysis",
        return_value=[mocker.MagicMock()],
    )

    config = mocker.MagicMock()
    result = sct_point_target_ambiguity_ratio_analysis(
        product_path="/input/product",
        external_target_source="/input/targets",
        config=config,
    )

    assert len(result) == 1
    mock_product_loader.assert_called_once_with(product_path=Path("/input/product"))
    mock_extract.assert_called_once_with(source=Path("/input/targets"))
    mock_convert.assert_called_once_with(data_df=mock_extract.return_value)
    mock_perseo.assert_called_once_with(
        product=mock_product,
        point_targets=mock_convert.return_value,
        config=config.base_config,
    )


def test_default_config_when_none(mocker) -> None:
    mocker.patch(
        "sct_ambiguities_analysis.core.analysis.product_loader",
        return_value=(mocker.MagicMock(), None),
    )
    mocker.patch(
        "sct_ambiguities_analysis.core.analysis.extract_point_target_data_from_source",
        return_value=mocker.MagicMock(),
    )
    mocker.patch(
        "sct_ambiguities_analysis.core.analysis.convert_df_to_nominal_point_target",
        return_value=mocker.MagicMock(),
    )
    mock_perseo = mocker.patch(
        "sct_ambiguities_analysis.core.analysis.point_target_ambiguity_ratio_analysis",
        return_value=[],
    )

    sct_point_target_ambiguity_ratio_analysis(
        product_path="/input/product",
        external_target_source="/input/targets",
        config=None,
    )

    # When config is None, a default SCTTargetAmbiguityRatioConfig is created,
    # and its base_config (an AmbiguityRatioConfig) is passed to perseo
    call_config = mock_perseo.call_args[1]["config"]
    from perseo_quality.tar_analysis.config import AmbiguityRatioConfig

    assert isinstance(call_config, AmbiguityRatioConfig)


def test_invalid_product_type_raises(mocker) -> None:
    from sct.io.io_manager import InvalidProductType

    mocker.patch(
        "sct_ambiguities_analysis.core.analysis.product_loader",
        side_effect=InvalidProductType,
    )

    with pytest.raises(InvalidProductType):
        sct_point_target_ambiguity_ratio_analysis(
            product_path="/input/product",
            external_target_source="/input/targets",
        )
