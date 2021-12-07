"""
Test cases for the wiutils.filters.remove_domestic function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.filters import remove_domestic


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
            ],
            "genus": [
                "Homo",
                "Bubulcus",
                "Dasyprocta",
                "Gallus",
                "Equus",
                "Anas",
                "Panthera",
                "Tremarctos",
                "Canis",
                "Bos",
                np.nan,
            ],
            "species": [
                "sapiens",
                "ibis",
                np.nan,
                "gallus",
                np.nan,
                "platyrhynchos domesticus",
                "onca",
                "ornatus",
                "familiaris",
                "taurus",
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
                "2020-12-01 21:01:43",
            ],
        }
    )


def test_defaults(images):
    result = remove_domestic(images)
    expected = pd.DataFrame(
        {
            "deployment_id": [
                "001",
                "001",
                "001",
                "002",
                "002",
            ],
            "genus": ["Bubulcus", "Dasyprocta", "Panthera", "Tremarctos", np.nan],
            "species": ["ibis", np.nan, "onca", "ornatus", np.nan],
            "timestamp": [
                "2020-12-01 10:15:05",
                "2020-12-01 10:16:46",
                "2020-12-01 10:14:04",
                "2020-12-01 14:08:21",
                "2020-12-01 21:01:43",
            ],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_keep_index(images):
    result = remove_domestic(images, reset_index=False)
    expected_index = pd.Index([1, 2, 6, 7, 10], dtype="int64")
    pd.testing.assert_index_equal(result.index, expected_index)


def test_intact_input(images):
    images_original = images.copy()
    remove_domestic(images)
    pd.testing.assert_frame_equal(images_original, images)
