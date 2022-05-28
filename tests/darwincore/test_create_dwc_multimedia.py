"""
Test cases for the wiutils.darwincore.create_dwc_multimedia function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.darwincore import create_dwc_multimedia


@pytest.fixture(scope="function")
def images():
    return pd.DataFrame(
        {
            "deployment_id": ["001", "001", "002"],
            "image_id": ["abc123", "def456", "hij789"],
            "location": [
                "gs://bucket/deployment/001/abc123.jpg",
                "gs://bucket/deployment/001/def456.jpg",
                "gs://bucket/deployment/002/hij789.jpg",
            ],
            "identified_by": ["Jane Doe", "Jane Doe", np.nan],
            "timestamp": [
                "2014-11-23 04:42:34",
                "2014-11-23 04:42:34",
                "2014-11-28 13:26:34",
            ],
            "class": ["Mammalia", "Mammalia", np.nan],
            "order": ["Carnivora", "Carnivora", np.nan],
            "family": ["Felidae", "Felidae", np.nan],
            "genus": ["Panthera", "Panthera", np.nan],
            "species": ["onca", "onca", np.nan],
            "license": ["CC-BY-NC", "CC-BY-NC", "CC-BY-NC"],
        }
    )


@pytest.fixture(scope="function")
def deployments():
    return pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "recorded_by": ["John Doe", "John Doe"],
        }
    )


def test_defaults(images, deployments):
    gcs_base_url = "https://console.cloud.google.com/storage/browser/"
    result = create_dwc_multimedia(images, deployments)
    expected = pd.DataFrame(
        {
            "eventID": ["001", "001", "002"],
            "type": ["Image", "Image", "Image"],
            "format": ["image/jpeg", "image/jpeg", "image/jpeg"],
            "identifier": ["abc123", "def456", "hij789"],
            "references": [
                gcs_base_url + "bucket/deployment/001/abc123.jpg",
                gcs_base_url + "bucket/deployment/001/def456.jpg",
                gcs_base_url + "bucket/deployment/002/hij789.jpg",
            ],
            "title": ["Panthera onca", "Panthera onca", "Blank or unidentified"],
            "created": [
                "2014-11-23 04:42:34",
                "2014-11-23 04:42:34",
                "2014-11-28 13:26:34",
            ],
            "creator": ["John Doe", "John Doe", "John Doe"],
            "contributor": ["Jane Doe", "Jane Doe", np.nan],
            "publisher": [
                "Wildlife Insights",
                "Wildlife Insights",
                "Wildlife Insights",
            ],
            "license": ["CC-BY-NC", "CC-BY-NC", "CC-BY-NC"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_intact_input(images, deployments):
    images_original = images.copy()
    deployments_original = deployments.copy()
    create_dwc_multimedia(images, deployments)
    pd.testing.assert_frame_equal(images_original, images)
    pd.testing.assert_frame_equal(deployments_original, deployments)
