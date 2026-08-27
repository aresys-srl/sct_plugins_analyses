# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Radiometric Analysis plugin entry point.

Lightweight module: importing it must not pull in the heavy analysis implementation
or the scientific stack. All heavy imports are deferred to the accessor methods.

This single plugin exposes several analysis types (NESZ, rain-forest, elevation
profiles, scalloping) that share one CLI group.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from sct_radiometric_analysis import __version__

if TYPE_CHECKING:
    from sct.core.base import AnalysisHandler
    from typer import Typer

ANALYSIS_BASE_NAME = "radiometry"
ANALYSES_NAMES = ["nesz", "rain-forest", "profiles", "scalloping"]


class RadiometricAnalysisPlugin:
    """Radiometric Analysis plugin (exposes several analysis types, one CLI group)."""

    version = __version__
    short_help = "Block-wise Radiometric Analysis."

    @classmethod
    def get_cli(cls) -> Typer | Callable:
        from sct_radiometric_analysis.cli import radiometric_app

        return radiometric_app

    @classmethod
    def get_handlers(cls) -> dict[str, AnalysisHandler]:
        from sct.core.base import AnalysisHandler, AnalysisTestingHandler

        from sct_radiometric_analysis.config import SCTRadiometricAnalysisConfig
        from sct_radiometric_analysis.testing import (
            run_nesz_api,
            run_nesz_cli,
            run_rain_forest_api,
            run_rain_forest_cli,
            validate_ra_results,
        )

        cli = cls.get_cli()

        return {
            "-".join([ANALYSIS_BASE_NAME, ANALYSES_NAMES[0]]): AnalysisHandler(
                config=SCTRadiometricAnalysisConfig,
                cli=cli,
                cli_group_name=ANALYSIS_BASE_NAME,
                testing=AnalysisTestingHandler(
                    api_runner=run_nesz_api,
                    cli_runner=run_nesz_cli,
                    validator=validate_ra_results,
                ),
            ),
            "-".join([ANALYSIS_BASE_NAME, ANALYSES_NAMES[1]]): AnalysisHandler(
                config=SCTRadiometricAnalysisConfig,
                cli=cli,
                cli_group_name=ANALYSIS_BASE_NAME,
                testing=AnalysisTestingHandler(
                    api_runner=run_rain_forest_api,
                    cli_runner=run_rain_forest_cli,
                    validator=validate_ra_results,
                ),
            ),
            "-".join([ANALYSIS_BASE_NAME, ANALYSES_NAMES[2]]): AnalysisHandler(
                config=SCTRadiometricAnalysisConfig,
                cli=cli,
                cli_group_name=ANALYSIS_BASE_NAME,
                testing=None,
            ),
            "-".join([ANALYSIS_BASE_NAME, ANALYSES_NAMES[3]]): AnalysisHandler(
                config=SCTRadiometricAnalysisConfig,
                cli=cli,
                cli_group_name=ANALYSIS_BASE_NAME,
                testing=None,
            ),
        }
