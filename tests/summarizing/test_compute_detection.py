"""
Test cases for the wiutils.summarizing.compute_detection function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.summarizing import compute_detection


@pytest.fixture(scope="function")
def images():
    return pd.DataFrame(
        {
            "deployment_id": ["001", "001", "001", "001", "002", "002"],
            "class": [
                "Aves",
                "Aves",
                "Mammalia",
                "Mammalia",
                "Aves",
                "Mammalia",
            ],
            "order": [
                "Columbiformes",
                "Columbiformes",
                "Carnivora",
                "Carnivora",
                "Columbiformes",
                "Carnivora",
            ],
            "family": [
                "Columbidae",
                "Columbidae",
                "Mustelidae",
                "Mustelidae",
                "Columbidae",
                "Mustelidae",
            ],
            "genus": [
                "Zentrygon",
                "Zentrygon",
                "Galictis",
                "Galictis",
                "Zentrygon",
                "Eira",
            ],
            "species": [
                "linearis",
                "linearis",
                "vittata",
                "vittata",
                "linearis",
                np.nan,
            ],
            "number_of_objects": [1, 2, 5, 2, 1, 3],
        }
    )


@pytest.fixture(scope="function")
def deployments():
    return pd.DataFrame({"deployment_id": ["001", "002"], "placename": ["AAA", "AAA"]})


def test_compute_abundance_deployment(images):
    result = compute_detection(
        images,
        groupby="deployment",
        compute_abundance=True,
    )
    expected = pd.DataFrame(
        {
            "taxon": [
                "Eira",
                "Eira",
                "Galictis vittata",
                "Galictis vittata",
                "Zentrygon linearis",
                "Zentrygon linearis",
            ],
            "deployment_id": ["001", "002", "001", "002", "001", "002"],
            "value": [0, 3, 7, 0, 3, 1],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_compute_abundance_location(images, deployments):
    result = compute_detection(
        images,
        deployments,
        groupby="location",
        compute_abundance=True,
    )
    expected = pd.DataFrame(
        {
            "taxon": [
                "Eira",
                "Galictis vittata",
                "Zentrygon linearis",
            ],
            "placename": ["AAA", "AAA", "AAA"],
            "value": [3, 7, 4],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_compute_presence_deployment(images):
    result = compute_detection(
        images,
        groupby="deployment",
        compute_abundance=False,
    )
    expected = pd.DataFrame(
        {
            "taxon": [
                "Eira",
                "Eira",
                "Galictis vittata",
                "Galictis vittata",
                "Zentrygon linearis",
                "Zentrygon linearis",
            ],
            "deployment_id": ["001", "002", "001", "002", "001", "002"],
            "value": [0, 1, 1, 0, 1, 1],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_compute_presence_location(images, deployments):
    result = compute_detection(
        images,
        deployments,
        groupby="location",
        compute_abundance=False,
    )
    expected = pd.DataFrame(
        {
            "taxon": [
                "Eira",
                "Galictis vittata",
                "Zentrygon linearis",
            ],
            "placename": ["AAA", "AAA", "AAA"],
            "value": [1, 1, 1],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_pivot_deployment(images):
    result = compute_detection(
        images,
        groupby="deployment",
        pivot=True,
    )
    expected = pd.DataFrame(
        {
            "taxon": [
                "Eira",
                "Galictis vittata",
                "Zentrygon linearis",
            ],
            "001": [0, 7, 3],
            "002": [3, 0, 1],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_pivot_location(images, deployments):
    result = compute_detection(
        images,
        deployments,
        groupby="location",
        pivot=True,
    )
    expected = pd.DataFrame(
        {
            "taxon": [
                "Eira",
                "Galictis vittata",
                "Zentrygon linearis",
            ],
            "AAA": [3, 7, 4],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_invalid_groupby(images, deployments):
    with pytest.raises(ValueError):
        compute_detection(images, deployments, groupby="placename")


def test_no_deployments(images):
    with pytest.raises(ValueError):
        compute_detection(images, groupby="location")


def test_intact_input(images):
    images_original = images.copy()
    compute_detection(images)
    pd.testing.assert_frame_equal(images_original, images)
