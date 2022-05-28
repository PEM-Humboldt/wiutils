"""

"""
import pathlib

import pytest


@pytest.fixture(scope="module")
def bundle_path():
    return pathlib.Path(__file__).parents[2].joinpath("wiutils/data/cajambre.zip")


@pytest.fixture(scope="module")
def invalid_path():
    return pathlib.Path(__file__).parents[2].joinpath("wiutils/config/mplstyle")
