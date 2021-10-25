"""
Test cases for the wiutils.tables.remove_duplicates function.
"""
import pandas as pd
import pytest

from wiutils.tables import remove_duplicates


@pytest.fixture(scope="module")
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
            ],
            "scientific_name": [
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Leptotila verreauxi",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
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
            ],
        }
    )


@pytest.fixture(scope="module")
def column_names():
    return {
        "site_col": "deployment_id",
        "species_col": "scientific_name",
        "date_col": "timestamp",
    }


def test_unit_seconds(images, column_names):
    result = remove_duplicates(images, interval=5, unit="seconds", **column_names)
    expected = pd.DataFrame(
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
            ],
            "scientific_name": [
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Leptotila verreauxi",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
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
                "2020-12-01 19:21:34",
            ],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_unit_minutes(images, column_names):
    result = remove_duplicates(images, interval=30, unit="minutes", **column_names)
    expected = pd.DataFrame(
        {
            "deployment_id": [
                "001",
                "001",
                "001",
                "001",
                "001",
                "002",
                "002",
            ],
            "scientific_name": [
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Leptotila verreauxi",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
            ],
            "timestamp": [
                "2020-12-01 10:13:13",
                "2020-12-01 14:22:38",
                "2020-12-03 08:15:57",
                "2020-12-15 06:12:32",
                "2020-12-01 10:14:04",
                "2020-12-01 14:08:21",
                "2020-12-01 19:21:34",
            ],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_unit_hours(images, column_names):
    result = remove_duplicates(images, interval=5, unit="hours", **column_names)
    expected = pd.DataFrame(
        {
            "deployment_id": [
                "001",
                "001",
                "001",
                "001",
                "002",
                "002",
            ],
            "scientific_name": [
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Leptotila verreauxi",
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
            ],
            "timestamp": [
                "2020-12-01 10:13:13",
                "2020-12-03 08:15:57",
                "2020-12-15 06:12:32",
                "2020-12-01 10:14:04",
                "2020-12-01 14:08:21",
                "2020-12-01 19:21:34",
            ],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_unit_days(images, column_names):
    result = remove_duplicates(images, interval=4, unit="days", **column_names)
    expected = pd.DataFrame(
        {
            "deployment_id": [
                "001",
                "001",
                "001",
                "002",
            ],
            "scientific_name": [
                "Myrmecophaga tridactyla",
                "Myrmecophaga tridactyla",
                "Leptotila verreauxi",
                "Myrmecophaga tridactyla",
            ],
            "timestamp": [
                "2020-12-01 10:13:13",
                "2020-12-15 06:12:32",
                "2020-12-01 10:14:04",
                "2020-12-01 14:08:21",
            ],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_unit_weeks(images, column_names):
    result = remove_duplicates(images, interval=3, unit="weeks", **column_names)
    expected = pd.DataFrame(
        {
            "deployment_id": [
                "001",
                "001",
                "002",
            ],
            "scientific_name": [
                "Myrmecophaga tridactyla",
                "Leptotila verreauxi",
                "Myrmecophaga tridactyla",
            ],
            "timestamp": [
                "2020-12-01 10:13:13",
                "2020-12-01 10:14:04",
                "2020-12-01 14:08:21",
            ],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_keep_index(images, column_names):
    result = remove_duplicates(images, reset_index=False, **column_names)
    expected_index = pd.Index([0, 3, 4, 5, 6, 7, 9], dtype="int64")
    pd.testing.assert_index_equal(result.index, expected_index)


def test_intact_input(images, column_names):
    remove_duplicates(images, reset_index=False, **column_names)
    pd.testing.assert_frame_equal(images, images)
