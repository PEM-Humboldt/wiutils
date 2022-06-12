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
            "number_of_objects": [1, 1, 2, 1, 1, 3, 1, 1, 1],
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
            "identified_images": [3, 5],
            "records": [4, 7],
            "taxa": [2, 5],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_groupby_location(images, deployments):
    result = compute_count_summary(images, deployments, groupby="location")
    expected = pd.DataFrame(
        {
            "placename": ["AAA"],
            "total_images": [9],
            "identified_images": [8],
            "records": [11],
            "taxa": [6],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_add_records_by_class_deployment(images):
    result = compute_count_summary(
        images, groupby="deployment", add_records_by_class=True
    )
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 6],
            "identified_images": [3, 5],
            "records": [4, 7],
            "records_mammalia": [4, 4],
            "records_aves": [0, 3],
            "taxa": [2, 5],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_add_records_by_class_location(images, deployments):
    result = compute_count_summary(
        images, deployments, groupby="location", add_records_by_class=True
    )
    expected = pd.DataFrame(
        {
            "placename": ["AAA"],
            "total_images": [9],
            "identified_images": [8],
            "records": [11],
            "records_mammalia": [8],
            "records_aves": [3],
            "taxa": [6],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_add_taxa_by_class_deployment(images):
    result = compute_count_summary(images, groupby="deployment", add_taxa_by_class=True)
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 6],
            "identified_images": [3, 5],
            "records": [4, 7],
            "taxa": [2, 5],
            "taxa_mammalia": [2, 2],
            "taxa_aves": [0, 3],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_add_taxa_by_class_location(images, deployments):
    result = compute_count_summary(
        images, deployments, groupby="location", add_taxa_by_class=True
    )
    expected = pd.DataFrame(
        {
            "placename": ["AAA"],
            "total_images": [9],
            "identified_images": [8],
            "records": [11],
            "taxa": [6],
            "taxa_mammalia": [3],
            "taxa_aves": [3],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_remove_unidentified_kws(images):
    result = compute_count_summary(images, remove_unidentified_kws={"rank": "species"})
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 6],
            "identified_images": [2, 4],
            "records": [2, 6],
            "taxa": [1, 4],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_remove_duplicates_kws(images):
    result = compute_count_summary(
        images, remove_duplicates_kws={"interval": 60, "unit": "minutes"}
    )
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "total_images": [3, 6],
            "identified_images": [3, 5],
            "records": [3, 7],
            "taxa": [2, 5],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


def test_invalid_groupby(images, deployments):
    with pytest.raises(ValueError):
        compute_count_summary(images, deployments, groupby="placename")


def test_no_deployments(images):
    with pytest.raises(ValueError):
        compute_count_summary(images, groupby="location")


def test_intact_input(images, deployments):
    images_original = images.copy()
    deployments_original = deployments.copy()
    compute_count_summary(images)
    pd.testing.assert_frame_equal(images_original, images)
    pd.testing.assert_frame_equal(deployments_original, deployments)
