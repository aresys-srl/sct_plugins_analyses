# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Point Target Analysis plugin entry point.

Lightweight module: importing it must not pull in the heavy analysis implementation
or the scientific stack. All heavy imports are deferred to the accessor methods.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from sct_point_target_analysis import __version__

if TYPE_CHECKING:
    from sct.core.base import AnalysisHandler
    from typer import Typer

ANALYSIS_NAME = "point_target"


class PointTargetAnalysisPlugin:
    """Point Target Analysis plugin."""

    version = __version__
    short_help = "Point Target Analysis (IRF, Localization and RCS)."

    @classmethod
    def get_cli(cls) -> Typer | Callable:
        from sct_point_target_analysis.cli import target_analysis

        return target_analysis

    @classmethod
    def get_handlers(cls) -> dict[str, AnalysisHandler]:
        from sct.core.base import AnalysisHandler, AnalysisTestingHandler

        from sct_point_target_analysis.config import SCTPointTargetAnalysisConfig
        from sct_point_target_analysis.testing import run_pta_api, run_pta_cli, validate_pta_results

        return {
            ANALYSIS_NAME: AnalysisHandler(
                config=SCTPointTargetAnalysisConfig,
                cli=cls.get_cli(),
                testing=AnalysisTestingHandler(
                    api_runner=run_pta_api,
                    cli_runner=run_pta_cli,
                    validator=validate_pta_results,
                ),
            )
        }
