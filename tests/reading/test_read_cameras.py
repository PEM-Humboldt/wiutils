"""
Test cases for the wiutils.reading.read_cameras function.
"""
import pathlib

import pandas
import pytest

from wiutils.reading import read_cameras


def test_shape(bundle_path):
    cameras = read_cameras(bundle_path)
    assert cameras.shape == (18, 6)


def test_other_path(mocker):
    mocker.patch("pandas.read_csv")
    read_cameras("path/to/bundle")
    pandas.read_csv.assert_called_once_with(pathlib.Path("path/to/bundle/cameras.csv"))


def test_invalid_path(invalid_path):
    with pytest.raises(ValueError):
        read_cameras(invalid_path)
