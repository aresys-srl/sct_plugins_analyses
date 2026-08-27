# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing CLI module."""

from __future__ import annotations

from pathlib import Path

from sct_ambiguities_analysis.cli import pt_ambiguity_ratio_analysis_implementation
from sct_ambiguities_analysis.config import SCTTargetAmbiguityRatioConfig


def test_pt_ambiguity_ratio_analysis_implementation_calls_main(mocker) -> None:
    mock_main = mocker.patch("sct_ambiguities_analysis.main.full_pt_ambiguity_ratio_analysis")

    pt_ambiguity_ratio_analysis_implementation(
        product=Path("/p"),
        point_target_source=Path("/pts"),
        output_directory=Path("/out"),
        config=SCTTargetAmbiguityRatioConfig(),
        graphs=True,
        dump_config=False,
    )

    mock_main.assert_called_once_with(
        product=Path("/p"),
        point_target_source=Path("/pts"),
        output_directory=Path("/out"),
        config=SCTTargetAmbiguityRatioConfig(),
        graphs=True,
    )
