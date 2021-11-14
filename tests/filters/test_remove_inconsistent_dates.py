"""
Test cases for the wiutils.filters.remove_inconsistent_dates function.
"""
import pandas as pd
import pytest

from wiutils.filters import remove_inconsistent_dates


@pytest.fixture(scope="function")
def images():
    return pd.DataFrame(
        {
            "deployment_id": [
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
            "timestamp": [
                "2020-12-01 10:15:05",
                "2020-12-03 08:21:25",
                "2020-12-17 14:18:12",
                "2020-12-24 19:01:00",
                "2020-11-18 21:43:12",
                "2020-11-28 07:32:14",
                "2020-12-01 13:43:57",
                "2021-01-12 17:03:13",
                "2021-02-24 15:00:25",
            ],
        }
    )


@pytest.fixture(scope="function")
def deployments():
    return pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "start_date": ["2020-12-03", "2020-11-20"],
            "end_date": ["2021-01-18", "2021-01-12"],
        }
    )


def test_inconsistent_dates(images, deployments):
    result = remove_inconsistent_dates(images, deployments, reset_index=True)
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "001", "001", "002", "002", "002"],
            "timestamp": [
                "2020-12-03 08:21:25",
                "2020-12-17 14:18:12",
                "2020-12-24 19:01:00",
                "2020-11-28 07:32:14",
                "2020-12-01 13:43:57",
                "2021-01-12 17:03:13",
            ],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_keep_index(images, deployments):
    result = remove_inconsistent_dates(images, deployments, reset_index=False)
    expected_index = pd.Index([1, 2, 3, 5, 6, 7], dtype="int64")
    pd.testing.assert_index_equal(result.index, expected_index)


def test_intact_input(images, deployments):
    images_original = images.copy()
    deployments_original = deployments.copy()
    remove_inconsistent_dates(images, deployments)
    pd.testing.assert_frame_equal(images_original, images)
    pd.testing.assert_frame_equal(deployments_original, deployments)
