"""
Test cases for the wiutils.reading.read_projects function.
"""
import pathlib

import pandas
import pytest

from wiutils.reading import read_projects


def test_shape(bundle_path):
    projects = read_projects(bundle_path)
    assert projects.shape == (1, 27)


def test_other_path(mocker):
    mocker.patch("pandas.read_csv")
    read_projects("path/to/bundle")
    pandas.read_csv.assert_called_once_with(pathlib.Path("path/to/bundle/projects.csv"))


def test_invalid_path(invalid_path):
    with pytest.raises(ValueError):
        read_projects(invalid_path)
