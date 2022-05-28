"""
Test cases for the wiutils.darwincore.create_dwc_measurement function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.darwincore import create_dwc_measurement


@pytest.fixture(scope="function")
def deployments():
    return pd.DataFrame(
        {
            "deployment_id": ["001", "002", "003"],
            "camera_id": ["cam001", "cam002", "cam003"],
            "bait_type": ["Meat", np.nan, "Other"],
            "bait_description": [np.nan, np.nan, "Insects"],
            "quiet_period": [np.nan, 5, 15],
        }
    )


@pytest.fixture(scope="function")
def cameras():
    return pd.DataFrame(
        {
            "camera_id": ["cam001", "cam002", "cam003"],
            "make": ["Bushnell", "Bushnell", "Bushnell"],
        }
    )


@pytest.fixture(scope="function")
def mapping():
    return [
        {
            "type": "camera make",
            "value": "make",
            "unit": np.nan,
            "remarks": None,
        },
        {
            "type": "bait type",
            "value": "bait_type",
            "unit": np.nan,
            "remarks": "bait_description",
        },
        {
            "type": "quiet period",
            "value": "quiet_period",
            "unit": "seconds",
            "remarks": None,
        },
    ]


def test_defaults(deployments, cameras, mocker, mapping):
    mocker.patch("wiutils._dwc.measurement.mapping", mapping)
    result = create_dwc_measurement(deployments, cameras)
    expected = pd.DataFrame(
        {
            "eventID": [
                "001",
                "002",
                "003",
                "001",
                "003",
                "002",
                "003",
            ],
            "measurementType": [
                "camera make",
                "camera make",
                "camera make",
                "bait type",
                "bait type",
                "quiet period",
                "quiet period",
            ],
            "measurementValue": [
                "Bushnell",
                "Bushnell",
                "Bushnell",
                "Meat",
                "Other",
                5,
                15,
            ],
            "measurementUnit": [
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                "seconds",
                "seconds",
            ],
            "measurementRemarks": [
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                "Insects",
                np.nan,
                np.nan,
            ],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_intact_input(deployments, cameras, mocker, mapping):
    mocker.patch("wiutils._dwc.measurement.mapping", mapping)
    deployments_original = deployments.copy()
    cameras_original = cameras.copy()
    create_dwc_measurement(deployments, cameras)
    pd.testing.assert_frame_equal(deployments_original, deployments)
    pd.testing.assert_frame_equal(cameras_original, cameras)
