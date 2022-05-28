"""
Test cases for the wiutils.reading.read_deployments function.
"""
import pathlib

import pandas
import pytest

from wiutils.reading import read_deployments


def test_shape(bundle_path):
    deployments = read_deployments(bundle_path)
    assert deployments.shape == (19, 27)


def test_other_path(mocker):
    mocker.patch("pandas.read_csv")
    read_deployments("path/to/bundle")
    pandas.read_csv.assert_called_once_with(
        pathlib.Path("path/to/bundle/deployments.csv"),
        parse_dates=["start_date", "end_date"],
    )


def test_date_dtypes(bundle_path):
    deployments = read_deployments(bundle_path)
    assert pandas.api.types.is_datetime64_any_dtype(deployments["start_date"])
    assert pandas.api.types.is_datetime64_any_dtype(deployments["end_date"])


def test_invalid_path(invalid_path):
    with pytest.raises(ValueError):
        read_deployments(invalid_path)
