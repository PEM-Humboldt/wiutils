"""
Test cases for the wiutils.get_lowest_taxon function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.extraction import get_lowest_taxon


@pytest.fixture(scope="function")
def images():
    return pd.DataFrame(
        {
            "class": [
                "Mammalia",
                np.nan,
                "Aves",
                "No CV Result",
                "Mammalia",
                "Mammalia",
                "Mammalia",
            ],
            "order": [
                np.nan,
                np.nan,
                "Psittaciformes",
                "No CV Result",
                "Carnivora",
                "Rodentia",
                "Perissodactyla",
            ],
            "family": [
                np.nan,
                np.nan,
                "Psittacidae",
                "No CV Result",
                "Felidae",
                "No CV Result",
                "Tapiridae",
            ],
            "genus": [
                np.nan,
                np.nan,
                "Ara",
                "No CV Result",
                np.nan,
                "No CV Result",
                "Tapirus",
            ],
            "species": [
                np.nan,
                np.nan,
                "macao",
                "No CV Result",
                np.nan,
                "No CV Result",
                np.nan,
            ],
        }
    )


def test_taxa(images):
    result = get_lowest_taxon(images, return_rank=False)
    expected = pd.Series(
        ["Mammalia", np.nan, "Ara macao", np.nan, "Felidae", "Rodentia", "Tapirus"]
    )
    pd.testing.assert_series_equal(result, expected)


def test_ranks(images):
    _, result = get_lowest_taxon(images, return_rank=True)
    expected = pd.Series(
        ["class", np.nan, "species", np.nan, "family", "order", "genus"]
    )
    pd.testing.assert_series_equal(result, expected)


def test_intact_input(images):
    images_original = images.copy()
    get_lowest_taxon(images, return_rank=False)
    pd.testing.assert_frame_equal(images_original, images)
