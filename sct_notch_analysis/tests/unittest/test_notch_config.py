# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing SCT Interferometric Analysis Configuration."""

from __future__ import annotations

from pathlib import Path

import pytest
from jsonschema.exceptions import ValidationError
from perseo_quality.elevation_notch_analysis.config import ElevationNotchConfig

from sct_notch_analysis.config import SCTElevationNotchAnalysisConfig

general_config_toml = """

[general]
save_log = true
save_config_copy = true

"""

elevation_notch_analysis_toml = """

[elevation_notch_analysis]
azimuth_block_size = 2500
range_pixel_margin = 100

"""


def _validate_notch_config(config: SCTElevationNotchAnalysisConfig) -> None:
    """Validating correct reading of elevation notch analysis configuration from file.

    Parameters
    ----------
    config : SCTElevationNotchAnalysisConfig
        sct elevation notch analysis configuration
    """

    assert isinstance(config, SCTElevationNotchAnalysisConfig)

    assert isinstance(config.base_config, ElevationNotchConfig)
    assert isinstance(config.base_config.azimuth_block_size, int)
    assert config.base_config.azimuth_block_size == 2500
    assert isinstance(config.base_config.range_pixel_margin, int)
    assert config.base_config.range_pixel_margin == 100


def test_full_elevation_notch_analysis_reading(tmp_path) -> None:
    """Test elevation_notch_analysis full configuration reading"""
    path_to_file = tmp_path.joinpath("test.toml")
    path_to_file.write_text(elevation_notch_analysis_toml)

    config = SCTElevationNotchAnalysisConfig.from_toml(path_to_file)

    assert isinstance(config, SCTElevationNotchAnalysisConfig)
    _validate_notch_config(config)


def test_reading_errors_0(tmp_path) -> None:
    """Test reading with errors"""
    partial_toml = """

    [elevation_notch_analysis]
    azimuth_block_size = "test"

    """
    with pytest.raises(ValidationError):
        path_to_file = tmp_path.joinpath("test.toml")
        path_to_file.write_text(partial_toml)

        SCTElevationNotchAnalysisConfig.from_toml(path_to_file)


def test_dump_read(tmp_path) -> None:
    """Test full configuration dump to toml and reading"""
    path_to_file = tmp_path.joinpath("test.toml")
    path_to_file.write_text(elevation_notch_analysis_toml)
    path_to_new_file = tmp_path.joinpath("dump.toml")

    # reading config
    config = SCTElevationNotchAnalysisConfig.from_toml(path_to_file)
    # dumping config
    config.to_toml(path_to_new_file)

    # compare config
    new_config = SCTElevationNotchAnalysisConfig.from_toml(path_to_new_file)

    assert new_config == config


def test_from_dict():
    config = SCTElevationNotchAnalysisConfig.from_dict({"azimuth_block_size": 2500, "range_pixel_margin": 100})
    assert isinstance(config, SCTElevationNotchAnalysisConfig)
    assert config.base_config.azimuth_block_size == 2500


def test_to_dict():
    config = SCTElevationNotchAnalysisConfig()
    d = config.to_dict()
    assert "elevation_notch_analysis" in d


def test_empty_config(tmp_path) -> None:
    """Test empty configuration"""
    with pytest.raises(ValidationError):
        path_to_file = tmp_path.joinpath("test.toml")
        path_to_file.write_text(general_config_toml)

        SCTElevationNotchAnalysisConfig.from_toml(path_to_file)


def test_default_config() -> None:
    """Test default configuration values"""
    config = SCTElevationNotchAnalysisConfig()
    assert isinstance(config, SCTElevationNotchAnalysisConfig)
    assert isinstance(config.base_config, ElevationNotchConfig)
    assert config.base_config.azimuth_block_size == 5000
    assert config.base_config.range_pixel_margin == 150


def test_validation_schema() -> None:
    """Test validation schema attribute"""
    schema = SCTElevationNotchAnalysisConfig.validation_schema
    assert isinstance(schema, Path)
    assert schema.exists()
    assert schema.name == "config_schema.json"


def test_config_group_name() -> None:
    """Test config_group_name attribute"""
    config = SCTElevationNotchAnalysisConfig()
    assert isinstance(config.config_group_name, str)
    assert len(config.config_group_name) > 0
    assert config.config_group_name == "elevation_notch_analysis"


def test_from_dict_empty() -> None:
    """Test from_dict with empty dict returns defaults"""
    config = SCTElevationNotchAnalysisConfig.from_dict({})
    assert isinstance(config, SCTElevationNotchAnalysisConfig)
    assert config.base_config.azimuth_block_size == 5000
    assert config.base_config.range_pixel_margin == 150


def test_from_dict_partial() -> None:
    """Test from_dict with partial dict fills missing from defaults"""
    config = SCTElevationNotchAnalysisConfig.from_dict({"azimuth_block_size": 3000})
    assert config.base_config.azimuth_block_size == 3000
    assert config.base_config.range_pixel_margin == 150


def test_to_dict_full() -> None:
    """Test to_dict returns full structured dict"""
    config = SCTElevationNotchAnalysisConfig.from_dict({"azimuth_block_size": 2500, "range_pixel_margin": 100})
    d = config.to_dict()
    assert "elevation_notch_analysis" in d
    inner = d["elevation_notch_analysis"]
    assert inner["azimuth_block_size"] == 2500
    assert inner["range_pixel_margin"] == 100


def test_config_equality() -> None:
    """Test equality of config instances"""
    c1 = SCTElevationNotchAnalysisConfig()
    c2 = SCTElevationNotchAnalysisConfig()
    assert c1 == c2
