# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Testing SCT Elevation Notch Analysis testing utilities."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from netCDF4 import Dataset
from sct.testing.utilities.common import ReferenceOutput, TestOutput

from sct_notch_analysis.testing import validate_notch_results

LINES = 100
SAMPLES = 50


def _create_notch_netcdf(path: Path, groups: dict) -> None:
    """Create a NetCDF file with the given group structure."""
    ds = Dataset(path, "w", format="NETCDF4")
    for group_name, subgroups in groups.items():
        grp = ds.createGroup(group_name)
        for sg_name, sg_data in subgroups.items():
            sg = grp.createGroup(sg_name)
            sg.azimuth_blocks_num = sg_data.get("azimuth_blocks_num", 1)
            sg.lines_per_block = sg_data.get("lines_per_block", LINES)
            sg.samples_per_block = sg_data.get("samples_per_block", SAMPLES)
            sg.createDimension("lines", LINES)
            sg.createDimension("samples", SAMPLES)
            for var_name, var_info in sg_data.get("variables", {}).items():
                v = sg.createVariable(var_name, "f8", ("lines", "samples"))
                v[:] = var_info["values"]
                if "units" in var_info:
                    v.units = var_info["units"]
    ds.close()


def _make_outputs(tmp_path: Path, ref_data: dict, cur_data: dict) -> tuple[ReferenceOutput, TestOutput]:
    """Create ReferenceOutput and TestOutput from data dicts."""
    ref_file = tmp_path / "ref.nc"
    cur_file = tmp_path / "cur.nc"
    _create_notch_netcdf(ref_file, ref_data)
    _create_notch_netcdf(cur_file, cur_data)
    return ReferenceOutput(netcdf_reference=ref_file), TestOutput(netcdf_results=cur_file)


class TestValidateNotchResults:
    """Tests for validate_notch_results."""

    def test_matching_results(self, tmp_path: Path) -> None:
        """Identical files should pass validation."""
        data = np.ones((LINES, SAMPLES), dtype=np.float64)
        ref_data = {
            "group1": {
                "subgroup1": {
                    "azimuth_blocks_num": 2,
                    "variables": {
                        "power": {"values": data, "units": "dB"},
                        "phase": {"values": np.zeros((LINES, SAMPLES))},
                    },
                },
            },
        }
        ref, cur = _make_outputs(tmp_path, ref_data, ref_data)
        validate_notch_results(cur, ref)

    def test_value_mismatch(self, tmp_path: Path) -> None:
        """Values differing beyond tolerance should raise AssertionError."""
        base = np.ones((LINES, SAMPLES), dtype=np.float64)
        ref_data = {
            "G": {"S": {"variables": {"power": {"values": base, "units": "dB"}}}},
        }
        cur_data = {
            "G": {"S": {"variables": {"power": {"values": base + 0.1, "units": "dB"}}}},
        }
        ref, cur = _make_outputs(tmp_path, ref_data, cur_data)
        with pytest.raises(AssertionError):
            validate_notch_results(cur, ref)

    def test_values_within_tolerance(self, tmp_path: Path) -> None:
        """Values within tolerance should pass."""
        base = np.ones((LINES, SAMPLES), dtype=np.float64)
        ref_data = {
            "G": {"S": {"variables": {"power": {"values": base, "units": "dB"}}}},
        }
        cur_data = {
            "G": {"S": {"variables": {"power": {"values": base + 1e-6, "units": "dB"}}}},
        }
        ref, cur = _make_outputs(tmp_path, ref_data, cur_data)
        validate_notch_results(cur, ref)

    def test_different_groups(self, tmp_path: Path) -> None:
        """Different group keys should raise AssertionError."""
        data = np.ones((LINES, SAMPLES), dtype=np.float64)
        ref_data = {
            "group1": {"subgroup1": {"variables": {"power": {"values": data}}}},
        }
        cur_data = {
            "group1": {"subgroup1": {"variables": {"power": {"values": data}}}},
            "group2": {"subgroup1": {"variables": {"power": {"values": data}}}},
        }
        ref, cur = _make_outputs(tmp_path, ref_data, cur_data)
        with pytest.raises(AssertionError):
            validate_notch_results(cur, ref)

    def test_different_variables(self, tmp_path: Path) -> None:
        """Different variable keys should raise AssertionError."""
        base = np.ones((LINES, SAMPLES), dtype=np.float64)
        ref_data = {
            "G": {"S": {"variables": {"power": {"values": base}, "phase": {"values": base}}}},
        }
        cur_data = {
            "G": {"S": {"variables": {"power": {"values": base}}}},
        }
        ref, cur = _make_outputs(tmp_path, ref_data, cur_data)
        with pytest.raises(AssertionError):
            validate_notch_results(cur, ref)

    def test_different_azimuth_blocks(self, tmp_path: Path) -> None:
        """Different azimuth_blocks_num should raise AssertionError."""
        base = np.ones((LINES, SAMPLES), dtype=np.float64)
        ref_data = {
            "G": {"S": {"azimuth_blocks_num": 2, "variables": {"power": {"values": base}}}},
        }
        cur_data = {
            "G": {"S": {"azimuth_blocks_num": 5, "variables": {"power": {"values": base}}}},
        }
        ref, cur = _make_outputs(tmp_path, ref_data, cur_data)
        with pytest.raises(AssertionError):
            validate_notch_results(cur, ref)
