"""
Test cases for the wiutils.filters.remove_unidentified function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.filters import remove_unidentified


@pytest.fixture(scope="function")
def images():
    return pd.DataFrame(
        {
            "class": [
                "Aves",
                "Mammalia",
                "Mammalia",
                "Aves",
                "Unknown",
                "Mammalia",
                "No CV Result",
                np.nan,
            ],
            "order": [
                "Piciformes",
                "Rodentia",
                "Carnivora",
                np.nan,
                "Unknown",
                "Pilosa",
                "No CV Result",
                np.nan,
            ],
            "family": [
                "Picidae",
                np.nan,
                "Felidae",
                np.nan,
                "Unknown",
                "Myrmecophagidae",
                "No CV Result",
                np.nan,
            ],
            "genus": [
                np.nan,
                np.nan,
                "Puma",
                np.nan,
                "Unknown",
                "Myrmecophaga",
                "No CV Result",
                np.nan,
            ],
            "species": [
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                "Unknown",
                "tridactyla",
                "No CV Result",
                np.nan,
            ],
        }
    )


def test_rank_class(images):
    result = remove_unidentified(images, rank="class", reset_index=True)
    expected = pd.DataFrame(
        {
            "class": ["Aves", "Mammalia", "Mammalia", "Aves", "Mammalia"],
            "order": ["Piciformes", "Rodentia", "Carnivora", np.nan, "Pilosa"],
            "family": ["Picidae", np.nan, "Felidae", np.nan, "Myrmecophagidae"],
            "genus": [np.nan, np.nan, "Puma", np.nan, "Myrmecophaga"],
            "species": [np.nan, np.nan, np.nan, np.nan, "tridactyla"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_rank_order(images):
    result = remove_unidentified(images, rank="order", reset_index=True)
    expected = pd.DataFrame(
        {
            "class": ["Aves", "Mammalia", "Mammalia", "Mammalia"],
            "order": ["Piciformes", "Rodentia", "Carnivora", "Pilosa"],
            "family": ["Picidae", np.nan, "Felidae", "Myrmecophagidae"],
            "genus": [np.nan, np.nan, "Puma", "Myrmecophaga"],
            "species": [np.nan, np.nan, np.nan, "tridactyla"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_rank_family(images):
    result = remove_unidentified(images, rank="family", reset_index=True)
    expected = pd.DataFrame(
        {
            "class": ["Aves", "Mammalia", "Mammalia"],
            "order": ["Piciformes", "Carnivora", "Pilosa"],
            "family": ["Picidae", "Felidae", "Myrmecophagidae"],
            "genus": [np.nan, "Puma", "Myrmecophaga"],
            "species": [np.nan, np.nan, "tridactyla"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_rank_genus(images):
    result = remove_unidentified(images, rank="genus", reset_index=True)
    expected = pd.DataFrame(
        {
            "class": ["Mammalia", "Mammalia"],
            "order": ["Carnivora", "Pilosa"],
            "family": ["Felidae", "Myrmecophagidae"],
            "genus": ["Puma", "Myrmecophaga"],
            "species": [np.nan, "tridactyla"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_rank_epithet(images):
    result = remove_unidentified(images, rank="epithet", reset_index=True)
    expected = pd.DataFrame(
        {
            "class": ["Mammalia"],
            "order": ["Pilosa"],
            "family": ["Myrmecophagidae"],
            "genus": ["Myrmecophaga"],
            "species": ["tridactyla"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_keep_index(images):
    result = remove_unidentified(images, rank="order", reset_index=False)
    expected_index = pd.Index([0, 1, 2, 5], dtype="int64")
    pd.testing.assert_index_equal(result.index, expected_index)


def test_intact_input(images):
    images_original = images.copy()
    remove_unidentified(images, rank="order")
    pd.testing.assert_frame_equal(images_original, images)
