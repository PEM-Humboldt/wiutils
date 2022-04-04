"""
Test cases for the wiutils.plotting.plot_deployment_dates function.
"""
import pandas as pd
import pytest
import seaborn

from wiutils.plotting import plot_deployment_dates


@pytest.fixture()
def images():
    return pd.DataFrame(
        {
            "deployment_id": [
                "001",
                "002",
                "002",
                "002",
                "003",
                "003",
                "001",
                "001",
                "003",
            ],
            "timestamp": [
                "2020-10-19 06:05:21",
                "2020-10-03 16:32:04",
                "2020-11-30 04:31:23",
                "2020-11-29 06:29:53",
                "2020-10-03 12:16:21",
                "2020-11-23 15:03:09",
                "2020-11-20 21:24:00",
                "2020-10-16 20:54:42",
                "2020-11-22 23:11:33",
            ],
        }
    )


@pytest.fixture()
def deployments():
    return pd.DataFrame(
        {
            "deployment_id": ["001", "002", "003"],
            "start_date": ["2020-10-15", "2020-10-02", "2020-11-01"],
            "end_date": ["2020-11-21", "2020-12-02", "2020-11-24"],
        }
    )


def test_images(images, mocker):
    mocker.patch("seaborn.relplot")
    plot_deployment_dates(images=images, source="images")
    expected = pd.DataFrame(
        {
            "deployment_id": ["002", "003", "001", "001", "003", "002"],
            "source": ["images", "images", "images", "images", "images", "images"],
            "variable": [
                "start_date",
                "start_date",
                "start_date",
                "end_date",
                "end_date",
                "end_date",
            ],
            "date": pd.to_datetime(
                [
                    "2020-10-03",
                    "2020-10-03",
                    "2020-10-16",
                    "2020-11-20",
                    "2020-11-23",
                    "2020-11-30",
                ]
            ),
        }
    )
    args, kwargs = seaborn.relplot.call_args
    pd.testing.assert_frame_equal(kwargs["data"], expected)


def test_deployments(deployments, mocker):
    mocker.patch("seaborn.relplot")
    plot_deployment_dates(deployments=deployments, source="deployments")
    expected = pd.DataFrame(
        {
            "deployment_id": ["002", "001", "003", "001", "003", "002"],
            "source": [
                "deployments",
                "deployments",
                "deployments",
                "deployments",
                "deployments",
                "deployments",
            ],
            "variable": [
                "start_date",
                "start_date",
                "start_date",
                "end_date",
                "end_date",
                "end_date",
            ],
            "date": pd.to_datetime(
                [
                    "2020-10-02",
                    "2020-10-15",
                    "2020-11-01",
                    "2020-11-21",
                    "2020-11-24",
                    "2020-12-02",
                ]
            ),
        }
    )
    args, kwargs = seaborn.relplot.call_args
    pd.testing.assert_frame_equal(kwargs["data"], expected)


def test_both(images, deployments, mocker):
    mocker.patch("seaborn.relplot")
    plot_deployment_dates(images=images, deployments=deployments, source="both")
    expected = pd.DataFrame(
        {
            "deployment_id": [
                "002",
                "002",
                "003",
                "001",
                "001",
                "003",
                "001",
                "001",
                "003",
                "003",
                "002",
                "002",
            ],
            "source": [
                "deployments",
                "images",
                "images",
                "deployments",
                "images",
                "deployments",
                "images",
                "deployments",
                "images",
                "deployments",
                "images",
                "deployments",
            ],
            "variable": [
                "start_date",
                "start_date",
                "start_date",
                "start_date",
                "start_date",
                "start_date",
                "end_date",
                "end_date",
                "end_date",
                "end_date",
                "end_date",
                "end_date",
            ],
            "date": pd.to_datetime([
                "2020-10-02",
                "2020-10-03",
                "2020-10-03",
                "2020-10-15",
                "2020-10-16",
                "2020-11-01",
                "2020-11-20",
                "2020-11-21",
                "2020-11-23",
                "2020-11-24",
                "2020-11-30",
                "2020-12-02",
            ]),
        }
    )
    args, kwargs = seaborn.relplot.call_args
    pd.testing.assert_frame_equal(kwargs["data"], expected)


def test_intact_input(images, deployments, mocker):
    mocker.patch("seaborn.relplot")
    images_original = images.copy()
    deployments_original = deployments.copy()
    plot_deployment_dates(images=images, deployments=deployments, source="both")
    pd.testing.assert_frame_equal(images_original, images)
    pd.testing.assert_frame_equal(deployments_original, deployments)


def test_invalid_source(images, deployments, mocker):
    mocker.patch("seaborn.relplot")
    with pytest.raises(ValueError):
        plot_deployment_dates(images=images, deployments=deployments, source="records")


def test_no_images(deployments, mocker):
    mocker.patch("seaborn.relplot")
    with pytest.raises(ValueError):
        plot_deployment_dates(deployments=deployments, source="both")


def test_no_deployments(images, mocker):
    mocker.patch("seaborn.relplot")
    with pytest.raises(ValueError):
        plot_deployment_dates(images=images, source="both")
