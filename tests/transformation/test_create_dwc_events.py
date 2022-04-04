"""
Test cases for the wiutils.transformation.create_dwc_events function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.transformation import create_dwc_events


@pytest.fixture(scope="function")
def deployments():
    return pd.DataFrame(
        {
            "placename": ["90210", "90210", "90210"],
            "deployment_id": ["001", "002", "003"],
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
            "feature_type": [np.nan, np.nan, np.nan],
            "event_name": [np.nan, np.nan, np.nan],
        }
    )


def test_defaults(deployments):
    result = create_dwc_events(deployments)
    expected = pd.DataFrame(
        {
            "eventID": ["001", "002", "003"],
            "parentEventID": ["90210", "90210", "90210"],
            "institutionCode": [np.nan, np.nan, np.nan],
            "sampleSizeValue": [1, 1, 1],
            "sampleSizeUnit": ["trap-nights", "trap-nights", "trap-nights"],
            "samplingProtocol": ["camera-trap", "camera-trap", "camera-trap"],
            "samplingEffort": ["37 trap-nights", "30 trap-nights", "36 trap-nights"],
            "eventDate": [
                "2020-11-10/2020-12-17",
                "2020-11-13/2020-12-13",
                "2020-11-08/2020-12-14",
            ],
            "eventRemarks": [np.nan, np.nan, np.nan],
            "continent": [np.nan, np.nan, np.nan],
            "country": [np.nan, np.nan, np.nan],
            "countryCode": [np.nan, np.nan, np.nan],
            "stateProvince": [np.nan, np.nan, np.nan],
            "county": [np.nan, np.nan, np.nan],
            "locality": [np.nan, np.nan, np.nan],
            "minimumElevationInMeters": [np.nan, np.nan, np.nan],
            "maximumElevationInMeters": [np.nan, np.nan, np.nan],
            "locationRemarks": [np.nan, np.nan, np.nan],
            "decimalLatitude": [3.71647, 3.82742, 3.90128],
            "decimalLongitude": [-71.79161, -71.52733, -71.81543],
            "geodeticDatum": ["EPSG:4326", "EPSG:4326", "EPSG:4326"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_remove_empty_optionals(deployments):
    result = create_dwc_events(deployments, remove_empty_optionals=True)
    expected = pd.DataFrame(
        {
            "eventID": ["001", "002", "003"],
            "parentEventID": ["90210", "90210", "90210"],
            "institutionCode": [np.nan, np.nan, np.nan],
            "sampleSizeValue": [1, 1, 1],
            "sampleSizeUnit": ["trap-nights", "trap-nights", "trap-nights"],
            "samplingProtocol": ["camera-trap", "camera-trap", "camera-trap"],
            "samplingEffort": ["37 trap-nights", "30 trap-nights", "36 trap-nights"],
            "eventDate": [
                "2020-11-10/2020-12-17",
                "2020-11-13/2020-12-13",
                "2020-11-08/2020-12-14",
            ],
            "continent": [np.nan, np.nan, np.nan],
            "country": [np.nan, np.nan, np.nan],
            "countryCode": [np.nan, np.nan, np.nan],
            "stateProvince": [np.nan, np.nan, np.nan],
            "county": [np.nan, np.nan, np.nan],
            "locality": [np.nan, np.nan, np.nan],
            "minimumElevationInMeters": [np.nan, np.nan, np.nan],
            "maximumElevationInMeters": [np.nan, np.nan, np.nan],
            "decimalLatitude": [3.71647, 3.82742, 3.90128],
            "decimalLongitude": [-71.79161, -71.52733, -71.81543],
            "geodeticDatum": ["EPSG:4326", "EPSG:4326", "EPSG:4326"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_language_es(deployments):
    result = create_dwc_events(deployments, language="es")
    expected = pd.DataFrame(
        {
            "eventID": ["001", "002", "003"],
            "parentEventID": ["90210", "90210", "90210"],
            "institutionCode": [np.nan, np.nan, np.nan],
            "sampleSizeValue": [1, 1, 1],
            "sampleSizeUnit": ["trampas-noche", "trampas-noche", "trampas-noche"],
            "samplingProtocol": ["fototrampeo", "fototrampeo", "fototrampeo"],
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
            "eventRemarks": [np.nan, np.nan, np.nan],
            "continent": [np.nan, np.nan, np.nan],
            "country": [np.nan, np.nan, np.nan],
            "countryCode": [np.nan, np.nan, np.nan],
            "stateProvince": [np.nan, np.nan, np.nan],
            "county": [np.nan, np.nan, np.nan],
            "locality": [np.nan, np.nan, np.nan],
            "minimumElevationInMeters": [np.nan, np.nan, np.nan],
            "maximumElevationInMeters": [np.nan, np.nan, np.nan],
            "locationRemarks": [np.nan, np.nan, np.nan],
            "decimalLatitude": [3.71647, 3.82742, 3.90128],
            "decimalLongitude": [-71.79161, -71.52733, -71.81543],
            "geodeticDatum": ["EPSG:4326", "EPSG:4326", "EPSG:4326"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_intact_input(deployments):
    deployments_original = deployments.copy()
    create_dwc_events(deployments)
    pd.testing.assert_frame_equal(deployments_original, deployments)
