"""
Test cases for the wiutils.transformers.compute_hill_numbers function.
"""
import pandas as pd
import pytest

from wiutils.transformers import compute_hill_numbers


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
            "scientific_name": [
                "Momotus momota",
                "Momotus momota",
                "Momotus momota",
                "Momotus momota",
                "Eira barbara",
                "Eira barbara",
                "Cuniculus paca",
                "Didelphis marsupialis",
                "Didelphis marsupialis",
                "Momotus momota",
                "Eira barbara",
                "Leopardus pardalis",
            ],
        }
    )


def test_result_long_single(images):
    result = compute_hill_numbers(images, 0, pivot=False, species_col="scientific_name")
    expected = pd.DataFrame(
        {"deployment_id": ["001", "002"], "q": [0, 0], "D": [3.0, 4.0]}
    )
    pd.testing.assert_frame_equal(result, expected, check_exact=False)


def test_result_long_multiple(images):
    result = compute_hill_numbers(
        images, [0, 1, 2], pivot=False, species_col="scientific_name"
    )
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "001", "001", "002", "002", "002"],
            "q": [0, 1, 2, 0, 1, 2],
            "D": [3.0, 2.600490006, 2.333333333, 4.0, 3.789291416, 3.571428571],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_exact=False)


def test_result_wide_single(images):
    result = compute_hill_numbers(images, 1, pivot=True, species_col="scientific_name")
    expected = pd.DataFrame(
        {"deployment_id": ["001", "002"], "1": [2.600490006, 3.789291416]}
    )
    pd.testing.assert_frame_equal(result, expected, check_exact=False)


def test_result_wide_multiple(images):
    result = compute_hill_numbers(
        images, [0, 1, 2], pivot=True, species_col="scientific_name"
    )
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "0": [3.0, 4.0],
            "1": [2.600490006, 3.789291416],
            "2": [2.333333333, 3.571428571],
        }
    )
    pd.testing.assert_frame_equal(result, expected, check_exact=False)


def test_intact_input(images):
    images_original = images.copy()
    compute_hill_numbers(images, [0, 1, 2], species_col="scientific_name")
    pd.testing.assert_frame_equal(images_original, images)
