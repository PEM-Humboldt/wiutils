"""
Test cases for the wiutils.summarizing.compute_hill_numbers function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.summarizing import compute_hill_numbers


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
                "002",
            ],
            "class": [
                "Aves",
                "Aves",
                "Aves",
                "Aves",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Aves",
                "Mammalia",
                "Mammalia",
            ],
            "order": [
                "Coraciiformes",
                "Coraciiformes",
                "Coraciiformes",
                "Coraciiformes",
                "Carnivora",
                "Carnivora",
                "Rodentia",
                "Didelphimorphia",
                "Didelphimorphia",
                "Coraciiformes",
                "Carnivora",
                "Carnivora",
            ],
            "family": [
                "Momotidae",
                "Momotidae",
                "Momotidae",
                "Momotidae",
                "Mustelidae",
                "Mustelidae",
                "Cuniculidae",
                "Didelphidae",
                "Didelphidae",
                "Momotidae",
                "Mustelidae",
                "Felidae",
            ],
            "genus": [
                "Momotus",
                "Momotus",
                "Momotus",
                "Momotus",
                "Eira",
                "Eira",
                np.nan,
                "Didelphis",
                "Didelphis",
                "Momotus",
                "Eira",
                "Leopardus",
            ],
            "species": [
                "momota",
                "momota",
                "momota",
                "momota",
                "barbara",
                "barbara",
                np.nan,
                "marsupialis",
                "marsupialis",
                "momota",
                "barbara",
                "pardalis",
            ],
            "number_of_objects": [2, 1, 1, 3, 1, 1, 6, 1, 1, 4, 1, 1],
        }
    )


@pytest.fixture(scope="function")
def deployments():
    return pd.DataFrame({"deployment_id": ["001", "002"], "placename": ["AAA", "AAA"]})


def test_result_long_location(images, deployments):
    result = compute_hill_numbers(
        images, deployments, groupby="location", q_values=[0, 1, 2], pivot=False
    )
    expected = pd.DataFrame(
        {
            "placename": ["AAA", "AAA", "AAA"],
            "q": [0, 1, 2],
            "D": [5.0, 3.735, 3.094],
        }
    )
    pd.testing.assert_frame_equal(result, expected, atol=1e-3)


def test_result_wide_location(images, deployments):
    result = compute_hill_numbers(
        images, deployments, groupby="location", q_values=[0, 1, 2], pivot=True
    )
    expected = pd.DataFrame(
        {
            "placename": ["AAA"],
            "0": [5.0],
            "1": [3.735],
            "2": [3.094],
        }
    )
    pd.testing.assert_frame_equal(result, expected, atol=1e-3)


def test_result_long_single(images):
    result = compute_hill_numbers(images, q_values=0, pivot=False)
    expected = pd.DataFrame(
        {"deployment_id": ["001", "002"], "q": [0, 0], "D": [3.0, 4.0]}
    )
    pd.testing.assert_frame_equal(result, expected)


def test_result_long_multiple(images):
    result = compute_hill_numbers(images, q_values=[0, 1, 2], pivot=False)
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "001", "001", "002", "002", "002"],
            "q": [0, 1, 2, 0, 1, 2],
            "D": [3.0, 2.693, 2.528, 4.000, 3.364, 2.909],
        }
    )
    pd.testing.assert_frame_equal(result, expected, atol=1e-3)


def test_result_wide_single(images):
    result = compute_hill_numbers(images, q_values=1, pivot=True)
    expected = pd.DataFrame({"deployment_id": ["001", "002"], "1": [2.693, 3.364]})
    pd.testing.assert_frame_equal(result, expected, atol=1e-3)


def test_result_wide_multiple(images):
    result = compute_hill_numbers(images, q_values=[0, 1, 2], pivot=True)
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "0": [3.0, 4.0],
            "1": [2.693, 3.364],
            "2": [2.528, 2.909],
        }
    )
    pd.testing.assert_frame_equal(result, expected, atol=1e-3)


def test_intact_input(images):
    images_original = images.copy()
    compute_hill_numbers(images, q_values=[0, 1, 2])
    pd.testing.assert_frame_equal(images_original, images)
