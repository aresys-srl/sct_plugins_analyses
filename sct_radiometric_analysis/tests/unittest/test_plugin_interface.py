# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing SCT Radiometric Analysis plugin interface."""

from __future__ import annotations

from typing import Callable

import pytest
from sct.core.base import AnalysisHandler, AnalysisTestingHandler
from sct.plugins.loader import import_analysis_plugins
from sct.plugins.protocols import AnalysisPluginProtocol

from sct_radiometric_analysis.config import SCTRadiometricAnalysisConfig
from sct_radiometric_analysis.interface import ANALYSES_NAMES, ANALYSIS_BASE_NAME, RadiometricAnalysisPlugin


@pytest.fixture
def plugin():
    plugins = import_analysis_plugins()
    candidates = [p for p in plugins if p is RadiometricAnalysisPlugin]
    assert len(candidates) >= 1
    return candidates[0]


class TestPluginProtocolCompliance:
    """Test Plugin Protocol Compliance"""

    def test_installed_plugin(self, plugin) -> None:
        """Testing correct plugin installation"""
        assert plugin is RadiometricAnalysisPlugin
        assert plugin.__name__ == "RadiometricAnalysisPlugin"

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
        assert sorted(ANALYSIS_BASE_NAME + "-" + a for a in ANALYSES_NAMES) == sorted(handlers.keys())
        for h in handlers.values():
            assert isinstance(h, AnalysisHandler)

    def test_handler_structure(self, plugin) -> None:
        """Testing handler structure: config, cli, testing"""
        handlers = plugin.get_handlers()

        for handler in handlers.values():
            assert handler.config is SCTRadiometricAnalysisConfig
            assert isinstance(handler.cli, Callable)
            assert handler.testing is None or isinstance(handler.testing, AnalysisTestingHandler)
            if handler.testing is not None:
                assert callable(handler.testing.api_runner)
                assert callable(handler.testing.cli_runner)
                assert callable(handler.testing.validator)
            assert handler.cli_group_name is None or isinstance(handler.cli_group_name, str)
