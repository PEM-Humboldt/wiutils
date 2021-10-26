"""
Test cases for the wiutils.transformers.compute_detection_by_deployment function.
"""
import pandas as pd
import pytest

from wiutils.transformers import compute_detection_by_deployment


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
                "002"
            ],
            "scientific_name": [
                "Zentrygon linearis",
                "Zentrygon linearis",
                "Galictis vittata",
                "Galictis vittata",
                "Zentrygon linearis",
                "Eira barbara"
            ]
        }
    )


@pytest.fixture(scope="module")
def column_names():
    return {"site_col": "deployment_id", "species_col": "scientific_name"}


def test_compute_abundance(images, column_names):
    result = compute_detection_by_deployment(images, **column_names)
    expected = pd.DataFrame(
        {
            "scientific_name": [
                "Eira barbara",
                "Eira barbara",
                "Galictis vittata",
                "Galictis vittata",
                "Zentrygon linearis",
                "Zentrygon linearis"
            ],
            "deployment_id": [
                "001",
                "002",
                "001",
                "002",
                "001",
                "002"
            ],
            "value": [0, 1, 2, 0, 2, 1]
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_compute_presence(images, column_names):
    result = compute_detection_by_deployment(
        images, compute_abundance=False, **column_names
    )
    expected = pd.DataFrame(
        {
            "scientific_name": [
                "Eira barbara",
                "Eira barbara",
                "Galictis vittata",
                "Galictis vittata",
                "Zentrygon linearis",
                "Zentrygon linearis"
            ],
            "deployment_id": [
                "001",
                "002",
                "001",
                "002",
                "001",
                "002"
            ],
            "value": [0, 1, 1, 0, 1, 1]
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_pivot(images, column_names):
    result = compute_detection_by_deployment(images, pivot=True, **column_names)
    expected = pd.DataFrame(
        {
            "scientific_name": [
                "Eira barbara",
                "Galictis vittata",
                "Zentrygon linearis"
            ],
            "001": [0, 2, 2],
            "002": [1, 0, 1]
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_intact_input(images, column_names):
    images_original = images.copy()
    compute_detection_by_deployment(images, **column_names)
    pd.testing.assert_frame_equal(images_original, images)
