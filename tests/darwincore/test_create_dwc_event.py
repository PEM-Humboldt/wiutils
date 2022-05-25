"""
Test cases for the wiutils.darwincore.create_dwc_event function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.darwincore import create_dwc_event


@pytest.fixture(scope="function")
def deployments():
    return pd.DataFrame(
        {
            "project_id": ["vkeh6gs", "vkeh6gs", "vkeh6gs"],
            "deployment_id": ["001", "002", "003"],
            "placename": ["90210", "90210", "10001"],
            "longitude": [-71.79161, -71.52733, -71.81543],
            "latitude": [3.71647, 3.82742, 3.90128],
            "start_date": [
                "2020-11-10 00:00:00",
                "2020-11-13 00:00:00",
                "2020-11-08 00:00:00",
            ],
            "end_date": [
                "2020-12-17 00:00:00",
                "2020-12-13 00:00:00",
                "2020-12-14 00:00:00",
            ],
            "feature_type": ["Other", "Trail hiking", "Road dirt"],
            "event_description": [np.nan, np.nan, "Some description"],
        }
    )


@pytest.fixture(scope="function")
def projects():
    return pd.DataFrame({"project_id": ["vkeh6gs"], "country_code": ["COL"]})


def test_language_en(deployments, projects):
    result = create_dwc_event(deployments, projects)
    expected = pd.DataFrame(
        {
            "eventID": ["001", "002", "003"],
            "parentEventID": ["90210", "90210", "10001"],
            "samplingProtocol": ["camera trap", "camera trap", "camera trap"],
            "sampleSizeValue": [1, 1, 1],
            "sampleSizeUnit": ["camera", "camera", "camera"],
            "samplingEffort": ["37 trap-nights", "30 trap-nights", "36 trap-nights"],
            "eventDate": [
                "2020-11-10/2020-12-17",
                "2020-11-13/2020-12-13",
                "2020-11-08/2020-12-14",
            ],
            "eventRemarks": [np.nan, np.nan, "Some description"],
            "countryCode": ["CO", "CO", "CO"],
            "locationRemarks": ["Other", "Trail hiking", "Road dirt"],
            "decimalLatitude": [3.71647, 3.82742, 3.90128],
            "decimalLongitude": [-71.79161, -71.52733, -71.81543],
            "geodeticDatum": ["WGS84", "WGS84", "WGS84"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_language_es(deployments, projects):
    result = create_dwc_event(deployments, projects, language="es")
    expected = pd.DataFrame(
        {
            "eventID": ["001", "002", "003"],
            "parentEventID": ["90210", "90210", "10001"],
            "samplingProtocol": ["fototrampeo", "fototrampeo", "fototrampeo"],
            "sampleSizeValue": [1, 1, 1],
            "sampleSizeUnit": ["cámara", "cámara", "cámara"],
            "samplingEffort": [
                "37 trampas-noche",
                "30 trampas-noche",
                "36 trampas-noche",
            ],
            "eventDate": [
                "2020-11-10/2020-12-17",
                "2020-11-13/2020-12-13",
                "2020-11-08/2020-12-14",
            ],
            "eventRemarks": [np.nan, np.nan, "Some description"],
            "countryCode": ["CO", "CO", "CO"],
            "locationRemarks": ["Otro", "Sendero", "Camino de tierra"],
            "decimalLatitude": [3.71647, 3.82742, 3.90128],
            "decimalLongitude": [-71.79161, -71.52733, -71.81543],
            "geodeticDatum": ["WGS84", "WGS84", "WGS84"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_intact_input(deployments, projects):
    deployments_original = deployments.copy()
    projects_original = projects.copy()
    create_dwc_event(deployments, projects)
    pd.testing.assert_frame_equal(deployments_original, deployments)
    pd.testing.assert_frame_equal(projects_original, projects)
