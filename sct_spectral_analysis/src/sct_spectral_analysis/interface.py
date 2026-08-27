# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Spectral Analysis plugin entry point.

Lightweight module: importing it must not pull in the heavy analysis implementation
or the scientific stack. All heavy imports are deferred to the accessor methods.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from sct_spectral_analysis import __version__

if TYPE_CHECKING:
    from sct.core.base import AnalysisHandler
    from typer import Typer

ANALYSIS_NAME = "spectra"


class SpectralAnalysisPlugin:
    """Spectral Analysis plugin."""

    version = __version__
    short_help = "Point and Distributed Target Spectral Analysis."

    @classmethod
    def get_cli(cls) -> Typer | Callable:
        from sct_spectral_analysis.cli import spectral_analysis

        return spectral_analysis

    @classmethod
    def get_handlers(cls) -> dict[str, AnalysisHandler]:
        from sct.core.base import AnalysisHandler, AnalysisTestingHandler

        from sct_spectral_analysis.config import SCTSpectralAnalysisConfig
        from sct_spectral_analysis.testing import (
            run_spectral_api,
            run_spectral_cli,
            validate_spectral_results,
        )

        return {
            ANALYSIS_NAME: AnalysisHandler(
                config=SCTSpectralAnalysisConfig,
                cli=cls.get_cli(),
                testing=AnalysisTestingHandler(
                    api_runner=run_spectral_api,
                    cli_runner=run_spectral_cli,
                    validator=validate_spectral_results,
                ),
            )
        }
