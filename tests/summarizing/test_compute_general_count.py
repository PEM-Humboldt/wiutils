"""
Test cases for the wiutils.summarizing.compute_general_count function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.summarizing import compute_general_count


@pytest.fixture(scope="function")
def images():
    return pd.DataFrame(
        {
            "deployment_id": ["001", "001", "001", "002", "003"],
            "class": ["Mammalia", "Mammalia", "Mammalia", "Mammalia", "Mammalia"],
            "order": ["Carnivora", "Carnivora", "Carnivora", "Carnivora", "Carnivora"],
            "family": ["Felidae", "Mustelidae", "Mustelidae", "Mustelidae", "Canidae"],
            "genus": ["Panthera", "Eira", "Eira", "Eira", np.nan],
            "species": ["onca", "barbara", "barbara", "barbara", np.nan],
            "number_of_objects": [1, 1, 1, 1, 4],
        }
    )


@pytest.fixture(scope="function")
def deployments():
    return pd.DataFrame(
        {"deployment_id": ["001", "002", "003"], "placename": ["AAA", "AAA", "BBB"]}
    )


def test_deployment(images):
    result = compute_general_count(images, groupby="deployment")
    expected = pd.DataFrame(
        {
            "taxon": ["Canidae", "Eira barbara", "Panthera onca"],
            "records": [4, 3, 1],
            "deployments": [1, 2, 1],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_placename(images, deployments):
    result = compute_general_count(images, deployments, groupby="location")
    expected = pd.DataFrame(
        {
            "taxon": ["Canidae", "Eira barbara", "Panthera onca"],
            "records": [4, 3, 1],
            "locations": [1, 1, 1],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_rank_class(images):
    result = compute_general_count(
        images, groupby="deployment", add_taxonomy=True, rank="class"
    )
    expected = pd.DataFrame(
        {
            "taxon": ["Canidae", "Eira barbara", "Panthera onca"],
            "records": [4, 3, 1],
            "deployments": [1, 2, 1],
            "class": ["Mammalia", "Mammalia", "Mammalia"],
            "order": ["Carnivora", "Carnivora", "Carnivora"],
            "family": ["Canidae", "Mustelidae", "Felidae"],
            "genus": [np.nan, "Eira", "Panthera"],
            "species": [np.nan, "barbara", "onca"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_rank_family(images):
    result = compute_general_count(
        images, groupby="deployment", add_taxonomy=True, rank="family"
    )
    expected = pd.DataFrame(
        {
            "taxon": ["Canidae", "Eira barbara", "Panthera onca"],
            "records": [4, 3, 1],
            "deployments": [1, 2, 1],
            "family": ["Canidae", "Mustelidae", "Felidae"],
            "genus": [np.nan, "Eira", "Panthera"],
            "species": [np.nan, "barbara", "onca"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_rank_error(images):
    with pytest.raises(ValueError):
        compute_general_count(images, add_taxonomy=True, rank="kingdom")


def test_no_taxonomy(images):
    result = compute_general_count(images, add_taxonomy=False)
    expected = pd.DataFrame(
        {
            "taxon": ["Canidae", "Eira barbara", "Panthera onca"],
            "records": [4, 3, 1],
            "deployments": [1, 2, 1],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_intact_input(images):
    images_original = images.copy()
    compute_general_count(images, add_taxonomy=False)
    pd.testing.assert_frame_equal(images_original, images)
