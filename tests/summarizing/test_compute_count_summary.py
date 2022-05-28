"""
Test cases for the wiutils.summarizing.compute_count_summary function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.summarizing import compute_count_summary


@pytest.fixture(scope="function")
def images():
    return pd.DataFrame(
        {
            "deployment_id": [
                "001",
                "001",
                "001",
                "002",
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
                "Aves",
                "No CV Result",
                "Mammalia",
                "Aves",
                "Aves",
                "Mammalia",
            ],
            "order": [
                "Carnivora",
                "Carnivora",
                "Rodentia",
                "Pelecaniformes",
                "No CV Result",
                "Primates",
                "Passeriformes",
                "Passeriformes",
                "Carnivora",
            ],
            "family": [
                "Felidae",
                "Felidae",
                np.nan,
                "Ardeidae",
                "No CV Result",
                "Cebidae",
                "Corvidae",
                "Tyrannidae",
                "Felidae",
            ],
            "genus": [
                "Leopardus",
                "Leopardus",
                np.nan,
                "Bubulcus",
                "No CV Result",
                "Saimiri",
                "Cyanocorax",
                "Elaenia",
                "Leopardus",
            ],
            "species": [
                "pardalis",
                "pardalis",
                np.nan,
                "ibis",
                "No CV Result",
                "sciureus",
                "violaceus",
                np.nan,
                "pardalis",
            ],
            "timestamp": [
                "2020-11-24 00:06:26",
                "2020-11-24 00:54:12",
                "2020-12-20 22:16:10",
                "2020-12-18 16:48:04",
                "2020-12-23 07:26:33",
                "2020-12-24 08:09:32",
                "2020-12-24 09:15:01",
                "2020-12-24 13:48:12",
                "2020-12-21 03:12:21",
            ],
        }
    )


@pytest.fixture(scope="function")
def deployments():
    return pd.DataFrame({"deployment_id": ["001", "002"], "placename": ["AAA", "AAA"]})


def test_groupby_deployment(images):
    result = compute_count_summary(images, groupby="deployment")
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 6],
            "identified_images": [2, 5],
            "records": [2, 5],
            "taxa": [1, 5],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_groupby_location(images, deployments):
    result = compute_count_summary(images, deployments, groupby="location")
    expected = pd.DataFrame(
        {
            "placename": ["AAA"],
            "total_images": [9],
            "identified_images": [7],
            "records": [7],
            "taxa": [5],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_add_records_by_class_deployment(images):
    result = compute_count_summary(
        images, groupby="deployment", add_records_by_class=True
    )
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 6],
            "identified_images": [2, 5],
            "records": [2, 5],
            "records_mammalia": [2, 2],
            "records_aves": [0, 3],
            "taxa": [1, 5],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_add_records_by_class_location(images, deployments):
    result = compute_count_summary(
        images, deployments, groupby="location", add_records_by_class=True
    )
    expected = pd.DataFrame(
        {
            "placename": ["AAA"],
            "total_images": [9],
            "identified_images": [7],
            "records": [7],
            "records_mammalia": [4],
            "records_aves": [3],
            "taxa": [5],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_add_species_by_class_deployment(images):
    result = compute_count_summary(
        images, groupby="deployment", add_species_by_class=True
    )
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 6],
            "identified_images": [2, 5],
            "records": [2, 5],
            "taxa": [1, 5],
            "taxa_mammalia": [1, 2],
            "taxa_aves": [0, 3],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_add_species_by_class_location(images, deployments):
    result = compute_count_summary(
        images, deployments, groupby="location", add_species_by_class=True
    )
    expected = pd.DataFrame(
        {
            "placename": ["AAA"],
            "total_images": [9],
            "identified_images": [7],
            "records": [7],
            "taxa": [5],
            "taxa_mammalia": [2],
            "taxa_aves": [3],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_remove_unidentified_kws(images):
    result = compute_count_summary(images, remove_unidentified_kws={"rank": "species"})
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 6],
            "identified_images": [2, 4],
            "records": [2, 4],
            "taxa": [1, 4],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_remove_duplicates_kws(images):
    result = compute_count_summary(
        images, remove_duplicates_kws={"interval": 60, "unit": "minutes"}
    )
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 6],
            "identified_images": [2, 5],
            "records": [1, 5],
            "taxa": [1, 5],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_intact_input(images):
    images_original = images.copy()
    compute_count_summary(images)
    pd.testing.assert_frame_equal(images_original, images)
