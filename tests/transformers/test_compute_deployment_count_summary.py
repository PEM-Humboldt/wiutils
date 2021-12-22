"""
Test cases for the wiutils.transformers.compute_deployment_count_summary function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.transformers import compute_deployment_count_summary


@pytest.fixture(scope="function")
def images():
    return pd.DataFrame(
        {
            "deployment_id": ["001", "001", "001", "002", "002", "002", "002", "002"],
            "class": [
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Aves",
                "No CV Result",
                "Mammalia",
                "Aves",
                "Aves",
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
            ],
            "scientific_name": [
                "Leopardus pardalis",
                "Leopardus pardalis",
                np.nan,
                "Bubulcus ibis",
                np.nan,
                "Saimiri sciureus",
                "Cyanocorax violaceus",
                np.nan,
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
            ],
        }
    )


def test_defaults(images):
    result = compute_deployment_count_summary(images)
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 5],
            "identified_images": [2, 4],
            "records": [2, 4],
            "species": [1, 3],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_add_records_by_class(images):
    result = compute_deployment_count_summary(images, add_records_by_class=True)
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 5],
            "identified_images": [2, 4],
            "records": [2, 4],
            "records_mammalia": [2, 1],
            "records_aves": [0, 3],
            "species": [1, 3],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_add_species_by_class(images):
    result = compute_deployment_count_summary(images, add_species_by_class=True)
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 5],
            "identified_images": [2, 4],
            "records": [2, 4],
            "species": [1, 3],
            "species_mammalia": [1, 1],
            "species_aves": [0, 2]
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_remove_unidentified_kws(images):
    result = compute_deployment_count_summary(
        images, remove_unidentified_kws={"rank": "epithet"}
    )
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 5],
            "identified_images": [2, 3],
            "records": [2, 3],
            "species": [1, 3],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_remove_duplicates_kws(images):
    result = compute_deployment_count_summary(
        images, remove_duplicates_kws={"interval": 60, "unit": "minutes"}
    )
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 5],
            "identified_images": [2, 4],
            "records": [1, 4],
            "species": [1, 3],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_intact_input(images):
    images_original = images.copy()
    compute_deployment_count_summary(images)
    pd.testing.assert_frame_equal(images_original, images)
