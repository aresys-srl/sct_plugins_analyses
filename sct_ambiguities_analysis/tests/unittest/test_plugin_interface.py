# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing SCT Target Ambiguity Ratio Analysis plugin interface."""

from __future__ import annotations

from typing import Callable

import pytest
from sct.core.base import AnalysisHandler
from sct.plugins.loader import import_analysis_plugins
from sct.plugins.protocols import AnalysisPluginProtocol

from sct_ambiguities_analysis.config import SCTTargetAmbiguityRatioConfig
from sct_ambiguities_analysis.interface import ANALYSIS_NAME, TargetAmbiguityRatioAnalysisPlugin


@pytest.fixture
def plugin():
    plugins = import_analysis_plugins()
    candidates = [p for p in plugins if p is TargetAmbiguityRatioAnalysisPlugin]
    assert len(candidates) >= 1
    return candidates[0]


class TestPluginProtocolCompliance:
    """Test Plugin Protocol Compliance"""

    def test_installed_plugin(self, plugin) -> None:
        """Testing correct plugin installation"""
        assert plugin is TargetAmbiguityRatioAnalysisPlugin
        assert plugin.__name__ == "TargetAmbiguityRatioAnalysisPlugin"

    def test_protocol_compliance(self, plugin) -> None:
        """Testing analysis plugin protocol compliance"""
        assert isinstance(plugin, AnalysisPluginProtocol)

    def test_version_field(self, plugin) -> None:
        """Testing version field presence and type"""
        assert isinstance(plugin.version, str)
        assert len(plugin.version) > 0

    def test_short_help_field(self, plugin) -> None:
        """Testing short_help field presence and type"""
        assert isinstance(plugin.short_help, str)
        assert len(plugin.short_help) > 0

    def test_get_cli(self, plugin) -> None:
        """Testing CLI retriever protocol compliance"""
        cli = plugin.get_cli()
        assert isinstance(cli, Callable)

    def test_get_handlers(self, plugin) -> None:
        """Testing handlers retriever protocol compliance"""
        handlers = plugin.get_handlers()
        assert isinstance(handlers, dict)
        assert ANALYSIS_NAME in handlers
        handler = handlers[ANALYSIS_NAME]
        assert isinstance(handler, AnalysisHandler)

    def test_handler_structure(self, plugin) -> None:
        """Testing handler structure: config, cli, testing"""
        handler = plugin.get_handlers()[ANALYSIS_NAME]

        assert handler.config is SCTTargetAmbiguityRatioConfig

        assert isinstance(handler.cli, Callable)

        assert handler.testing is None

        assert handler.cli_group_name is None or isinstance(handler.cli_group_name, str)
