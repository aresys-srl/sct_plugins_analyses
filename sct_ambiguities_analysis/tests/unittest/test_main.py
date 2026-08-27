# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing main orchestrator module."""

from __future__ import annotations

from pathlib import Path

from perseo_quality.tar_analysis.graphical_output import ambiguities_graphs

from sct_ambiguities_analysis.main import _import_ptar_graphs_func, full_pt_ambiguity_ratio_analysis


def test_full_analysis_with_graphs(mocker) -> None:
    mock_analysis = mocker.patch(
        "sct_ambiguities_analysis.main.sct_point_target_ambiguity_ratio_analysis",
        return_value=[mocker.MagicMock()],
    )
    mocker.patch(
        "sct_ambiguities_analysis.main._import_ptar_graphs_func",
        return_value=mocker.MagicMock(),
    )
    mock_graphs_dir = mocker.MagicMock()
    mock_output_dir = mocker.MagicMock()
    mock_output_dir.joinpath.return_value = mock_graphs_dir

    full_pt_ambiguity_ratio_analysis(
        product=Path("/p"),
        point_target_source=Path("/pts"),
        output_directory=mock_output_dir,
        config=mocker.MagicMock(),
        graphs=True,
    )

    mock_analysis.assert_called_once_with(
        product_path=Path("/p"),
        external_target_source=Path("/pts"),
        config=mocker.ANY,
    )
    mock_output_dir.joinpath.assert_called_once_with("graphs")
    mock_graphs_dir.mkdir.assert_called_once_with(exist_ok=True)


def test_full_analysis_without_graphs(mocker) -> None:
    mock_analysis = mocker.patch(
        "sct_ambiguities_analysis.main.sct_point_target_ambiguity_ratio_analysis",
        return_value=[],
    )

    full_pt_ambiguity_ratio_analysis(
        product=Path("/p"),
        point_target_source=Path("/pts"),
        output_directory=Path("/out"),
        config=mocker.MagicMock(),
        graphs=False,
    )

    mock_analysis.assert_called_once()


def test_import_graphs_func_with_graphs() -> None:
    result = _import_ptar_graphs_func(graphs=True)
    assert result is ambiguities_graphs


def test_import_graphs_func_without_graphs() -> None:
    result = _import_ptar_graphs_func(graphs=False)
    assert result is None
