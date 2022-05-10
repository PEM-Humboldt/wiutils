"""
Test cases for the wiutils.transformation.compute_detection_history function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.summarizing import compute_detection_history


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
                "001",
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
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
            ],
            "order": [
                "Carnivora",
                "Carnivora",
                "Carnivora",
                "Carnivora",
                "Carnivora",
                "Carnivora",
                "Carnivora",
                "Carnivora",
                "Carnivora",
                "Carnivora",
                "Carnivora",
            ],
            "family": [
                "Felidae",
                "Felidae",
                "Felidae",
                "Felidae",
                "Felidae",
                "Felidae",
                "Felidae",
                "Felidae",
                "Felidae",
                "Felidae",
                "Felidae",
            ],
            "genus": [
                "Panthera",
                "Panthera",
                "Panthera",
                "Panthera",
                "Panthera",
                "Leopardus",
                "Leopardus",
                "Leopardus",
                "Panthera",
                "Panthera",
                "Panthera",
            ],
            "species": [
                "onca",
                "onca",
                "onca",
                "onca",
                "onca",
                "pardalis",
                "pardalis",
                "pardalis",
                "onca",
                "onca",
                "onca",
            ],
            "timestamp": [
                "2020-11-27 06:45:57",
                "2020-11-29 09:24:32",
                "2020-12-04 14:41:52",
                "2020-12-05 16:17:41",
                "2020-12-06 08:51:01",
                "2020-11-25 09:58:12",
                "2020-12-01 10:11:25",
                "2020-12-05 17:21:33",
                "2020-11-30 09:42:29",
                "2020-12-03 11:14:32",
                "2020-12-11 07:53:07",
            ],
        }
    )


@pytest.fixture(scope="function")
def deployments():
    return pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "start_date": ["2020-11-24", "2020-11-27"],
            "end_date": ["2020-12-07", "2020-12-14"],
        }
    )


def test_compute_abundance(images, deployments):
    result = compute_detection_history(images, deployments, days=7)
    expected = pd.DataFrame(
        {
            "taxon": [
                "Leopardus pardalis",
                "Leopardus pardalis",
                "Leopardus pardalis",
                "Leopardus pardalis",
                "Leopardus pardalis",
                "Leopardus pardalis",
                "Panthera onca",
                "Panthera onca",
                "Panthera onca",
                "Panthera onca",
                "Panthera onca",
                "Panthera onca",
            ],
            "deployment_id": [
                "001",
                "001",
                "001",
                "002",
                "002",
                "002",
                "001",
                "001",
                "001",
                "002",
                "002",
                "002",
            ],
            "timestamp": pd.to_datetime(
                [
                    "2020-11-24",
                    "2020-12-01",
                    "2020-12-08",
                    "2020-11-24",
                    "2020-12-01",
                    "2020-12-08",
                    "2020-11-24",
                    "2020-12-01",
                    "2020-12-08",
                    "2020-11-24",
                    "2020-12-01",
                    "2020-12-08",
                ]
            ),
            "value": [1, 2, np.nan, 0, 0, 0, 2, 3, np.nan, 1, 1, 1],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_compute_presence(images, deployments):
    result = compute_detection_history(
        images, deployments, days=14, compute_abundance=False
    )
    expected = pd.DataFrame(
        {
            "taxon": [
                "Leopardus pardalis",
                "Leopardus pardalis",
                "Leopardus pardalis",
                "Leopardus pardalis",
                "Panthera onca",
                "Panthera onca",
                "Panthera onca",
                "Panthera onca",
            ],
            "deployment_id": ["001", "001", "002", "002", "001", "001", "002", "002"],
            "timestamp": pd.to_datetime(
                [
                    "2020-11-24",
                    "2020-12-08",
                    "2020-11-24",
                    "2020-12-08",
                    "2020-11-24",
                    "2020-12-08",
                    "2020-11-24",
                    "2020-12-08",
                ]
            ),
            "value": [1, np.nan, 0, 0, 1, np.nan, 1, 1],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_date_range_images(images, deployments):
    result = compute_detection_history(images, deployments, date_range="images", days=15)
    expected = pd.DataFrame(
        {
            "taxon": [
                "Leopardus pardalis",
                "Leopardus pardalis",
                "Leopardus pardalis",
                "Leopardus pardalis",
                "Panthera onca",
                "Panthera onca",
                "Panthera onca",
                "Panthera onca",
            ],
            "deployment_id": ["001", "001", "002", "002", "001", "001", "002", "002"],
            "timestamp": pd.to_datetime(
                [
                    "2020-11-25",
                    "2020-12-10",
                    "2020-11-25",
                    "2020-12-10",
                    "2020-11-25",
                    "2020-12-10",
                    "2020-11-25",
                    "2020-12-10",
                ]
            ),
            "value": [3, np.nan, 0, 0, 5, np.nan, 2, 1],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_pivot(images, deployments):
    result = compute_detection_history(
        images, deployments, date_range="images", days=15, pivot=True
    )
    expected = pd.DataFrame(
        {
            "taxon": [
                "Leopardus pardalis",
                "Leopardus pardalis",
                "Panthera onca",
                "Panthera onca",
            ],
            "deployment_id": ["001", "002", "001", "002"],
            "2020-11-25": [3.0, 0.0, 5.0, 2.0],
            "2020-12-10": [np.nan, 0, np.nan, 1],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_intact_input(images, deployments):
    images_original = images.copy()
    deployments_original = deployments.copy()
    compute_detection_history(images, deployments, days=7)
    pd.testing.assert_frame_equal(images_original, images)
    pd.testing.assert_frame_equal(deployments_original, deployments)
