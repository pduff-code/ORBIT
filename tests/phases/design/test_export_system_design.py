"""Tests for the `ExportSystemDesign` class."""

__author__ = "Rob Hammond"
__copyright__ = "Copyright 2019, National Renewable Energy Laboratory"
__maintainer__ = "Rob Hammond"
__email__ = "robert.hammond@nrel.gov"


import copy

import numpy as np
import pytest

from ORBIT.phases.design import ExportSystemDesign

config = {
    "site": {
        "depth": 20,
        "distance_to_interconnection": 3,
        "distance_to_landfall": 30,
    },
    "plant": {"num_turbines": 50},
    "turbine": {"turbine_rating": 7},
    "export_system_design": {
        "cables": "XLPE_300mm_33kV",
        "percent_redundant": 0.0,
        "percent_added_length": 0.01,
    },
}


def test_export_system_creation():
    export = ExportSystemDesign(config)
    export.run()

    assert export.num_cables
    assert export.length
    assert export.mass
    assert export.cable
    assert export.total_length
    assert export.total_mass


def test_number_cables():
    export = ExportSystemDesign(config)
    export.run()

    assert export.num_cables == 11


def test_cable_length():
    export = ExportSystemDesign(config)
    export.run()

    length = 0.02 + 3 + 30
    length += length * 0.01
    assert export.length == length


def test_cable_mass():
    export = ExportSystemDesign(config)
    export.run()

    length = 0.02 + 3 + 30
    length += length * 0.01
    mass = length * export.cable.linear_density
    assert export.mass == mass


def test_total_cable():
    export = ExportSystemDesign(config)
    export.run()

    length = 0.02 + 3 + 30
    length += length * 0.01
    mass = length * export.cable.linear_density
    assert export.total_mass == pytest.approx(mass * 11, abs=1e-10)
    assert export.total_length == pytest.approx(length * 11, abs=1e-10)


def test_cables_property():
    export = ExportSystemDesign(config)
    export.run()

    assert (
        export.sections_cables == export.cable.name
    ).sum() == export.num_cables


def test_cable_lengths_property():
    export = ExportSystemDesign(config)
    export.run()

    cable_len = export.length
    cable_name = export.cable.name
    assert (
        export.cable_lengths_by_type[cable_name] == export.length
    ).sum() == export.num_cables


def test_total_cable_len_property():
    export = ExportSystemDesign(config)
    export.run()

    cable_name = export.cable.name
    assert export.total_cable_length_by_type[cable_name] == pytest.approx(
        export.total_length, abs=1e-10
    )


def test_design_result():
    export = ExportSystemDesign(config)
    export.run()

    cable_name = export.cable.name
    cables = export.design_result["export_system"]["cables"]

    assert len(cables) == 1
    cable = cables[cable_name]
    assert cable["cable_sections"] == [(export.length, export.num_cables)]
    assert cable["linear_density"] == export.cable.linear_density