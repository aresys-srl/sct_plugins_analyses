# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Interferometric Analysis plugin entry point.

Lightweight module: importing it must not pull in the heavy analysis implementation
or the scientific stack. All heavy imports are deferred to the accessor methods.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from sct_interferometric_analysis import __version__

if TYPE_CHECKING:
    from sct.core.base import AnalysisHandler
    from typer import Typer

ANALYSIS_NAME = "interferometry"


class InterferometricAnalysisPlugin:
    """Interferometric Analysis plugin."""

    version = __version__
    short_help = "Interferometric Analysis (coherence and 2D histograms)."

    @classmethod
    def get_cli(cls) -> Typer | Callable:
        from sct_interferometric_analysis.cli import interf_coherence_analysis

        return interf_coherence_analysis

    @classmethod
    def get_handlers(cls) -> dict[str, AnalysisHandler]:
        from sct.core.base import AnalysisHandler, AnalysisTestingHandler

        from sct_interferometric_analysis.config import SCTInterferometricAnalysisConfig
        from sct_interferometric_analysis.testing import (
            run_interf_api,
            run_interf_cli,
            validate_interf_results,
        )

        return {
            ANALYSIS_NAME: AnalysisHandler(
                config=SCTInterferometricAnalysisConfig,
                cli=cls.get_cli(),
                testing=AnalysisTestingHandler(
                    api_runner=run_interf_api,
                    cli_runner=run_interf_cli,
                    validator=validate_interf_results,
                ),
            )
        }
