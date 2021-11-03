"""
Test cases for the wiutils.transformers.compute_general_count function.
"""
import pandas as pd
import pytest

from wiutils.transformers import compute_general_count


@pytest.fixture(scope="function")
def images():
    return pd.DataFrame(
        {
            "deployment_id": ["001", "001", "001", "002", "003"],
            "scientific_name": [
                "Panthera onca",
                "Eira barbara",
                "Eira barbara",
                "Eira barbara",
                "Canis lupus"
            ],
            "class": ["Mammalia", "Mammalia", "Mammalia", "Mammalia", "Mammalia"],
            "order": ["Carnivora", "Carnivora", "Carnivora", "Carnivora", "Carnivora"],
            "family": ["Felidae", "Mustelidae", "Mustelidae", "Mustelidae", "Canidae"],
            "genus": ["Panthera", "Eira", "Eira", "Eira", "Canis"],
            "species": ["onca", "barbara", "barbara", "barbara", "lupus"]
        }
    )


@pytest.fixture(scope="module")
def column_names():
    return {
        "site_col": "deployment_id",
        "species_col": "scientific_name",
        "class_col": "class",
        "order_col": "order",
        "family_col": "family",
        "genus_col": "genus",
        "epithet_col": "species"
    }


def test_rank_class(images, column_names):
    result = compute_general_count(
        images, add_taxonomy=True, rank="class", **column_names
    )
    expected = pd.DataFrame(
        {
            "scientific_name": ["Canis lupus", "Eira barbara", "Panthera onca"],
            "images": [1, 3, 1],
            "deployments": [1, 2, 1],
            "class": ["Mammalia", "Mammalia", "Mammalia"],
            "order": ["Carnivora", "Carnivora", "Carnivora"],
            "family": ["Canidae", "Mustelidae", "Felidae"],
            "genus": ["Canis", "Eira", "Panthera"],
            "species": ["lupus", "barbara", "onca"]
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_rank_family(images, column_names):
    result = compute_general_count(
        images, add_taxonomy=True, rank="family", **column_names
    )
    expected = pd.DataFrame(
        {
            "scientific_name": ["Canis lupus", "Eira barbara", "Panthera onca"],
            "images": [1, 3, 1],
            "deployments": [1, 2, 1],
            "family": ["Canidae", "Mustelidae", "Felidae"],
            "genus": ["Canis", "Eira", "Panthera"],
            "species": ["lupus", "barbara", "onca"]
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_rank_error(images, column_names):
    with pytest.raises(ValueError):
        compute_general_count(images, add_taxonomy=True, rank="kingdom", **column_names)


def test_no_taxonomy(images, column_names):
    result = compute_general_count(images, add_taxonomy=False, **column_names)
    expected = pd.DataFrame(
        {
            "scientific_name": ["Canis lupus", "Eira barbara", "Panthera onca"],
            "images": [1, 3, 1],
            "deployments": [1, 2, 1]
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_intact_input(images, column_names):
    images_original = images.copy()
    compute_general_count(images, add_taxonomy=False, **column_names)
    pd.testing.assert_frame_equal(images_original, images)
