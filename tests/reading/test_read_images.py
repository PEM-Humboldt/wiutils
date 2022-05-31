"""
Test cases for the wiutils.reading.read_images function.
"""
import pathlib

import pandas
import pytest

from wiutils.reading import read_images


def test_shape(bundle_path):
    images = read_images(bundle_path)
    assert images.shape == (5253, 26)


def test_other_path(mocker):
    mocker.patch("pandas.read_csv")
    read_images("path/to/bundle")
    pandas.read_csv.assert_called_once_with(
        pathlib.Path("path/to/bundle/images.csv"), parse_dates=["timestamp"]
    )


def test_date_dtypes(bundle_path):
    deployments = read_images(bundle_path)
    assert pandas.api.types.is_datetime64_any_dtype(deployments["timestamp"])


def test_invalid_path(invalid_path):
    with pytest.raises(ValueError):
        read_images(invalid_path)
