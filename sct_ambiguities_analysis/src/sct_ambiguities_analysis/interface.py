# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Target Ambiguity Ratio Analysis plugin entry point.

Lightweight module: importing it must not pull in the heavy analysis implementation
or the scientific stack. All heavy imports are deferred to the accessor methods.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from sct import __version__

if TYPE_CHECKING:
    from sct.core.base import AnalysisHandler
    from typer import Typer

ANALYSIS_NAME = "ambiguity_ratio"


class TargetAmbiguityRatioAnalysisPlugin:
    """Target Ambiguity Ratio Analysis plugin."""

    version = __version__
    short_help = "Point Target Ambiguity Ratio Analysis."

    @classmethod
    def get_cli(cls) -> Typer | Callable:
        from sct_ambiguities_analysis.cli import ptar_analysis

        return ptar_analysis

    @classmethod
    def get_handlers(cls) -> dict[str, AnalysisHandler]:
        from sct.core.base import AnalysisHandler

        from sct_ambiguities_analysis.config import SCTTargetAmbiguityRatioConfig

        return {
            ANALYSIS_NAME: AnalysisHandler(
                config=SCTTargetAmbiguityRatioConfig,
                cli=cls.get_cli(),
                testing=None,
            )
        }
