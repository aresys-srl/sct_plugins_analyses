# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Elevation Notch Analysis plugin entry point.

Lightweight module: importing it must not pull in the heavy analysis implementation
or the scientific stack. All heavy imports are deferred to the accessor methods.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from sct_notch_analysis import __version__

if TYPE_CHECKING:
    from sct.core.base import AnalysisHandler
    from typer import Typer

ANALYSIS_NAME = "elevation_notch"


class ElevationNotchAnalysisPlugin:
    """Elevation Notch Analysis plugin."""

    version = __version__
    short_help = "Elevation Notch Analysis."

    @classmethod
    def get_cli(cls) -> Typer | Callable:
        from sct_notch_analysis.cli import notch_analysis

        return notch_analysis

    @classmethod
    def get_handlers(cls) -> dict[str, AnalysisHandler]:
        from sct.core.base import AnalysisHandler, AnalysisTestingHandler

        from sct_notch_analysis.config import SCTElevationNotchAnalysisConfig
        from sct_notch_analysis.testing import (
            run_notch_api,
            run_notch_cli,
            validate_notch_results,
        )

        return {
            ANALYSIS_NAME: AnalysisHandler(
                config=SCTElevationNotchAnalysisConfig,
                cli=cls.get_cli(),
                testing=AnalysisTestingHandler(
                    api_runner=run_notch_api,
                    cli_runner=run_notch_cli,
                    validator=validate_notch_results,
                ),
            )
        }
