# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Command Line Interface for Interferometric Analysis."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from sct.cli import common
from sct.configuration.config import GeneralConfiguration
from sct.configuration.logger import sct_logger

from sct_interferometric_analysis.config import SCTInterferometricAnalysisConfig

SecondProductOption = Annotated[
    Path | None,
    typer.Option(
        "--product_2",
        "-pp",
        exists=True,
        dir_okay=True,
        resolve_path=True,
        help="Second co-registered product, must be provided if the first product is not an interferogram",
    ),
]


def interf_coherence_analysis(
    ctx: typer.Context,
    product: common.InputProductOption,
    output_directory: common.OutputDirectoryOption,
    product_2: SecondProductOption = None,
    graphs: common.GraphsOption = False,
) -> None:
    """Interferometric Analysis (Coherence and Coherence intensity 2D histograms).

    \b
    It can be performed:
    - using a single interferogram product, via -p/--product argument
    - using two co-registered products, respectively with -p/--product and -pp/--product_2
    """

    config: GeneralConfiguration = ctx.obj

    log_path = output_directory / "sct_interf_analysis.log" if config.save_log else None

    with common.logging_to_file(log_path):
        if product_2:
            sct_logger.info(f"First co-registered product: {product}")
            sct_logger.info(f"Second co-registered product: {product_2}")
        else:
            sct_logger.info(f"Interferogram product: {product}")
        sct_logger.info(f"Output folder is: {output_directory}")
        sct_logger.info(f"Graphs generation {'enabled' if graphs else 'disabled'}")

        common.display_title("Interferometric Analysis")

        analysis_config = (
            SCTInterferometricAnalysisConfig.from_toml(config.toml_path)
            if config.toml_path is not None
            else SCTInterferometricAnalysisConfig()
        )
        interf_coherence_analysis_implementation(
            product=product,
            product_2=product_2,
            output_directory=output_directory,
            config=analysis_config,
            graphs=graphs,
            dump_config=config.save_config_copy,
        )


@common.log_elapsed_time("Interferometric Analysis")
@common.graceful_exit("Interferometric Analysis")
def interf_coherence_analysis_implementation(
    product: Path,
    product_2: Path | None,
    config: SCTInterferometricAnalysisConfig,
    output_directory: Path,
    graphs: bool,
    dump_config: bool,
) -> None:
    """Implement of the interferometric analysis command."""
    from sct_interferometric_analysis.main import full_interferometric_analysis

    full_interferometric_analysis(
        product=product,
        product_2=product_2,
        config=config,
        output_directory=output_directory,
        graphs=graphs,
    )
