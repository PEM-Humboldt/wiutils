"""
Test cases for the wiutils.extraction.get_scientific_name function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.extraction import get_scientific_name


@pytest.fixture(scope="module")
def images():
    return pd.DataFrame(
        {
            "genus": ["Dasyprocta", np.nan, "No CV Result", "Unknown", "Odocoileus"],
            "species": ["fuliginosa", np.nan, "No CV Result", "Unknown", np.nan],
        }
    )


def test_discard_genus(images):
    result = get_scientific_name(images, keep_genus=False)
    expected = pd.Series(["Dasyprocta fuliginosa", np.nan, np.nan, np.nan, np.nan])
    pd.testing.assert_series_equal(result, expected)


def test_keep_genus(images):
    result = get_scientific_name(images, keep_genus=True)
    expected = pd.Series(["Dasyprocta fuliginosa", np.nan, np.nan, np.nan, "Odocoileus"])
    pd.testing.assert_series_equal(result, expected)


def test_add_qualifier(images):
    result = get_scientific_name(images, keep_genus=True, add_qualifier=True)
    expected = pd.Series(
        ["Dasyprocta fuliginosa", np.nan, np.nan, np.nan, "Odocoileus sp."]
    )
    pd.testing.assert_series_equal(result, expected)


def test_add_qualifier_no_effect(images):
    result = get_scientific_name(images, keep_genus=False, add_qualifier=True)
    expected = pd.Series(["Dasyprocta fuliginosa", np.nan, np.nan, np.nan, np.nan])
    pd.testing.assert_series_equal(result, expected)
