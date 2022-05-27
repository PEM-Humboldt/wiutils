"""
Test cases for the wiutils.summarizing.create_dwc_occurrence function.
"""
import numpy as np
import pandas as pd
import pytest

from wiutils.darwincore import create_dwc_occurrence


@pytest.fixture(scope="function")
def images():
    return pd.DataFrame(
        {
            "project_id": ["AAA001", "AAA001", "AAA001", "AAA001", "AAA001"],
            "deployment_id": ["001", "001", "002", "002", "002"],
            "image_id": ["bc6534f0", "003cb8eb", "a19bbd16", "740e09f5", "e09axa3q"],
            "location": [
                "gs://bucket/deployment/001/bc6534f0.jpg",
                "gs://bucket/deployment/001/003cb8eb.jpg",
                "gs://bucket/deployment/002/a19bbd16.jpg",
                "gs://bucket/deployment/002/740e09f5.jpg",
                "gs://bucket/deployment/002/e09axa3q.jpg",
            ],
            "class": ["Mammalia", "Mammalia", np.nan, "Aves", "Mammalia"],
            "order": ["Carnivora", "Carnivora", np.nan, "Passeriformes", "Rodentia"],
            "family": ["Felidae", "Felidae", np.nan, "Tinamidae", "Cuniculidae"],
            "genus": ["Panthera", "Panthera", np.nan, np.nan, "Cuniculus"],
            "species": ["onca", "onca", np.nan, np.nan, "paca nelsoni"],
            "timestamp": [
                "2020-12-13 09:04:50",
                "2020-12-13 10:02:12",
                "2021-01-12 09:59:02",
                "2020-11-17 01:12:57",
                "2021-01-12 09:59:03",
            ],
            "number_of_objects": [1, 1, 0, 1, 2],
        }
    )


@pytest.fixture(scope="function")
def deployments():
    return pd.DataFrame(
        {
            "placename": ["90210", "90211"],
            "deployment_id": ["001", "002"],
            "project_id": ["AAA001", "AAA001"],
            "recorded_by": ["Joe Bloggs", "Joe Bricks"],
        }
    )


@pytest.fixture(scope="function")
def projects():
    return pd.DataFrame(
        {
            "project_id": ["AAA001"],
            "project_admin_organization": ["Instituto Humboldt"],
        }
    )


@pytest.fixture(scope="function")
def constants():
    return {
        "organismQuantityType": "individual(s)",
    }


@pytest.fixture(scope="function")
def mapping():
    return {
        "deployment_id": "eventID",
        "placename": "parentEventID",
        "recorded_by": "recordedBy",
        "number_of_objects": "organismQuantity",
        "project_admin_organization": "institutionCode",
        "family": "family",
        "genus": "genus",
    }


@pytest.fixture(scope="function")
def order():
    return [
        "eventID",
        "parentEventID",
        "eventDate",
        "eventTime",
        "recordedBy",
        "organismQuantity",
        "organismQuantityType",
        "associatedMedia",
        "institutionCode",
        "scientificName",
        "family",
        "genus",
        "specificEpithet",
        "infraspecificEpithet",
        "taxonRank",
    ]


def test_defaults(deployments, images, projects, mocker, constants, mapping, order):
    mocker.patch("wiutils._dwc.occurrence.constants", constants)
    mocker.patch("wiutils._dwc.occurrence.mapping", mapping)
    mocker.patch("wiutils._dwc.occurrence.order", order)
    gcs_base_url = "https://console.cloud.google.com/storage/browser/"
    result = create_dwc_occurrence(images, deployments, projects)
    expected = pd.DataFrame(
        {
            "eventID": ["001", "001", "002", "002"],
            "parentEventID": ["90210", "90210", "90211", "90211"],
            "eventDate": ["2020-12-13", "2020-12-13", "2020-11-17", "2021-01-12"],
            "eventTime": ["09:04:50", "10:02:12", "01:12:57", "09:59:03"],
            "recordedBy": ["Joe Bloggs", "Joe Bloggs", "Joe Bricks", "Joe Bricks"],
            "organismQuantity": [1, 1, 1, 2],
            "organismQuantityType": [
                "individual(s)",
                "individual(s)",
                "individual(s)",
                "individual(s)",
            ],
            "associatedMedia": [
                gcs_base_url + "bucket/deployment/001/bc6534f0.jpg",
                gcs_base_url + "bucket/deployment/001/003cb8eb.jpg",
                gcs_base_url + "bucket/deployment/002/740e09f5.jpg",
                gcs_base_url + "bucket/deployment/002/e09axa3q.jpg",
            ],
            "institutionCode": [
                "Instituto Humboldt",
                "Instituto Humboldt",
                "Instituto Humboldt",
                "Instituto Humboldt",
            ],
            "scientificName": [
                "Panthera onca",
                "Panthera onca",
                "Tinamidae",
                "Cuniculus paca nelsoni",
            ],
            "family": ["Felidae", "Felidae", "Tinamidae", "Cuniculidae"],
            "genus": ["Panthera", "Panthera", np.nan, "Cuniculus"],
            "specificEpithet": ["onca", "onca", np.nan, "paca"],
            "infraspecificEpithet": [np.nan, np.nan, np.nan, "nelsoni"],
            "taxonRank": ["species", "species", "family", "subspecies"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_remove_duplicate_kws(
    deployments, images, projects, mocker, constants, mapping, order
):
    mocker.patch("wiutils._dwc.occurrence.constants", constants)
    mocker.patch("wiutils._dwc.occurrence.mapping", mapping)
    mocker.patch("wiutils._dwc.occurrence.order", order)
    gcs_base_url = "https://console.cloud.google.com/storage/browser/"
    result = create_dwc_occurrence(
        images,
        deployments,
        projects,
        remove_duplicate_kws=dict(interval=60, unit="minutes"),
    )
    expected = pd.DataFrame(
        {
            "eventID": ["001", "002", "002"],
            "parentEventID": ["90210", "90211", "90211"],
            "eventDate": ["2020-12-13", "2020-11-17", "2021-01-12"],
            "eventTime": ["09:04:50", "01:12:57", "09:59:03"],
            "recordedBy": ["Joe Bloggs", "Joe Bricks", "Joe Bricks"],
            "organismQuantity": [1, 1, 2],
            "organismQuantityType": ["individual(s)", "individual(s)", "individual(s)"],
            "associatedMedia": [
                gcs_base_url
                + "bucket/deployment/001/bc6534f0.jpg"
                + "|"
                + gcs_base_url
                + "bucket/deployment/001/003cb8eb.jpg",
                gcs_base_url + "bucket/deployment/002/740e09f5.jpg",
                gcs_base_url + "bucket/deployment/002/e09axa3q.jpg",
            ],
            "institutionCode": [
                "Instituto Humboldt",
                "Instituto Humboldt",
                "Instituto Humboldt",
            ],
            "scientificName": ["Panthera onca", "Tinamidae", "Cuniculus paca nelsoni"],
            "family": ["Felidae", "Tinamidae", "Cuniculidae"],
            "genus": ["Panthera", np.nan, "Cuniculus"],
            "specificEpithet": ["onca", np.nan, "paca"],
            "infraspecificEpithet": [np.nan, np.nan, "nelsoni"],
            "taxonRank": ["species", "family", "subspecies"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_intact_input(images, deployments, projects):
    images_original = images.copy()
    deployments_original = deployments.copy()
    create_dwc_occurrence(images, deployments, projects)
    pd.testing.assert_frame_equal(images_original, images)
    pd.testing.assert_frame_equal(deployments_original, deployments)
