"""
Test cases for the wiutils.summarizing.compute_detection function.
"""
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
                "",
                "",
                "Aves",
                "Mammalia",
            ],
            "order": [
                "Columbiformes",
                "Columbiformes",
                "",
                "",
                "Columbiformes",
                "Carnivora",
            ],
            "family": [
                "Columbidae",
                "Columbidae",
                "",
                "",
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
                "barbara",
            ],
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
                "Eira barbara",
                "Eira barbara",
                "Galictis vittata",
                "Galictis vittata",
                "Zentrygon linearis",
                "Zentrygon linearis",
            ],
            "deployment_id": ["001", "002", "001", "002", "001", "002"],
            "value": [0, 1, 2, 0, 2, 1],
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
                "Eira barbara",
                "Galictis vittata",
                "Zentrygon linearis",
            ],
            "placename": ["AAA", "AAA", "AAA"],
            "value": [1, 2, 3],
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
                "Eira barbara",
                "Eira barbara",
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
                "Eira barbara",
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
                "Eira barbara",
                "Galictis vittata",
                "Zentrygon linearis",
            ],
            "001": [0, 2, 2],
            "002": [1, 0, 1],
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
                "Eira barbara",
                "Galictis vittata",
                "Zentrygon linearis",
            ],
            "AAA": [1, 2, 3],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_intact_input(images):
    images_original = images.copy()
    compute_detection(images)
    pd.testing.assert_frame_equal(images_original, images)
