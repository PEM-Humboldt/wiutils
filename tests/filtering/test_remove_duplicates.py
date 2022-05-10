"""
Test cases for the wiutils.filtering.remove_duplicates function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.filtering import remove_duplicates


@pytest.fixture(scope="function")
def images():
    return pd.DataFrame(
        {
            "deployment_id": [
                "001",
                "001",
                "001",
                "001",
                "001",
                "001",
                "001",
                "002",
                "002",
                "002",
                "002",
                "002",
            ],
            "class": [
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Aves",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
            ],
            "order": [
                "Pilosa",
                "Pilosa",
                "Pilosa",
                "Pilosa",
                "Pilosa",
                "Pilosa",
                "Columbiformes",
                "Pilosa",
                "Pilosa",
                "Pilosa",
                "Pilosa",
                "Pilosa",
            ],
            "family": [
                "Myrmecophagidae",
                "Myrmecophagidae",
                "Myrmecophagidae",
                "Myrmecophagidae",
                "Myrmecophagidae",
                "Myrmecophagidae",
                "Columbidae",
                "Myrmecophagidae",
                "Myrmecophagidae",
                "Myrmecophagidae",
                "Myrmecophagidae",
                "Myrmecophagidae",
            ],
            "genus": [
                "Myrmecophaga",
                "Myrmecophaga",
                "Myrmecophaga",
                "Myrmecophaga",
                "Myrmecophaga",
                "Myrmecophaga",
                "Leptotila",
                "Myrmecophaga",
                "Myrmecophaga",
                "Myrmecophaga",
                np.nan,
                np.nan,
            ],
            "species": [
                "tridactyla",
                "tridactyla",
                "tridactyla",
                "tridactyla",
                "tridactyla",
                "tridactyla",
                "verreauxi",
                "tridactyla",
                "tridactyla",
                "tridactyla",
                np.nan,
                np.nan,
            ],
            "timestamp": [
                "2020-12-01 10:13:13",
                "2020-12-01 10:15:05",
                "2020-12-01 10:16:46",
                "2020-12-01 14:22:38",
                "2020-12-03 08:15:57",
                "2020-12-15 06:12:32",
                "2020-12-01 10:14:04",
                "2020-12-01 14:08:21",
                "2020-12-01 14:08:21",
                "2020-12-01 19:21:34",
                "2020-12-01 19:41:52",
                "2020-12-01 21:03:08",
            ],
        }
    )


def test_unit_seconds(images):
    result = remove_duplicates(images, interval=5, unit="seconds", reset_index=False)
    expected_index = pd.Index([0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11])
    pd.testing.assert_index_equal(result.index, expected_index)


def test_unit_minutes(images):
    result = remove_duplicates(images, interval=30, unit="minutes", reset_index=False)
    expected_index = pd.Index([0, 3, 4, 5, 6, 7, 9, 10, 11])
    pd.testing.assert_index_equal(result.index, expected_index)


def test_unit_hours(images):
    result = remove_duplicates(images, interval=5, unit="hours", reset_index=False)
    expected_index = pd.Index([0, 4, 5, 6, 7, 9, 10])
    pd.testing.assert_index_equal(result.index, expected_index)


def test_unit_days(images):
    result = remove_duplicates(images, interval=4, unit="days", reset_index=False)
    expected_index = pd.Index([0, 5, 6, 7, 10])
    pd.testing.assert_index_equal(result.index, expected_index)


def test_unit_weeks(images):
    result = remove_duplicates(images, interval=3, unit="weeks", reset_index=False)
    expected_index = pd.Index([0, 6, 7, 10])
    pd.testing.assert_index_equal(result.index, expected_index)


def test_reset_index(images):
    result = remove_duplicates(images, reset_index=True)
    expected_index = pd.Index([0, 1, 2, 3, 4, 5, 6, 7, 8])
    pd.testing.assert_index_equal(result.index, expected_index)


def test_intact_input(images):
    images_original = images.copy()
    remove_duplicates(images)
    pd.testing.assert_frame_equal(images_original, images)
