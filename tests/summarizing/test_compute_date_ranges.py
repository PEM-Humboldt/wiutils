"""
Test cases for the wiutils.verification.compute_date_ranges function.
"""
import pandas as pd
import pytest

from wiutils.verification import compute_date_ranges


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
                "2021-02-19 06:05:21",
                "2021-02-03 16:32:04",
                "2021-03-30 04:31:23",
                "2021-03-29 06:29:53",
                "2021-02-03 12:16:21",
                "2021-03-23 15:03:09",
                "2021-03-20 21:24:00",
                "2021-02-16 20:54:42",
                "2021-03-22 23:11:33",
            ],
        }
    )


@pytest.fixture()
def deployments():
    return pd.DataFrame(
        {
            "deployment_id": ["001", "002", "003"],
            "start_date": ["2021-02-13", "2021-02-01", "2021-03-01"],
            "end_date": ["2021-03-23", "2021-04-03", "2021-03-27"],
        }
    )


def test_images(images):
    result = compute_date_ranges(images=images, source="images")
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002", "003"],
            "start_date": pd.to_datetime(
                [
                    "2021-02-16",
                    "2021-02-03",
                    "2021-02-03",
                ]
            ),
            "end_date": pd.to_datetime(
                [
                    "2021-03-20",
                    "2021-03-30",
                    "2021-03-23",
                ]
            ),
            "source": ["images", "images", "images"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_deployments(deployments):
    result = compute_date_ranges(deployments=deployments, source="deployments")
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002", "003"],
            "start_date": pd.to_datetime(
                [
                    "2021-02-13",
                    "2021-02-01",
                    "2021-03-01",
                ]
            ),
            "end_date": pd.to_datetime(
                [
                    "2021-03-23",
                    "2021-04-03",
                    "2021-03-27",
                ]
            ),
            "source": ["deployments", "deployments", "deployments"],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_both(images, deployments):
    result = compute_date_ranges(images=images, deployments=deployments, source="both")
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002", "003", "001", "002", "003"],
            "start_date": pd.to_datetime(
                [
                    "2021-02-16",
                    "2021-02-03",
                    "2021-02-03",
                    "2021-02-13",
                    "2021-02-01",
                    "2021-03-01",
                ]
            ),
            "end_date": pd.to_datetime(
                [
                    "2021-03-20",
                    "2021-03-30",
                    "2021-03-23",
                    "2021-03-23",
                    "2021-04-03",
                    "2021-03-27",
                ]
            ),
            "source": [
                "images",
                "images",
                "images",
                "deployments",
                "deployments",
                "deployments",
            ],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_compute_delta(images):
    result = compute_date_ranges(images=images, source="images", compute_delta=True)
    expected = pd.DataFrame(
        {
            "deployment_id": ["001", "002", "003"],
            "start_date": pd.to_datetime(
                [
                    "2021-02-16",
                    "2021-02-03",
                    "2021-02-03",
                ]
            ),
            "end_date": pd.to_datetime(
                [
                    "2021-03-20",
                    "2021-03-30",
                    "2021-03-23",
                ]
            ),
            "source": ["images", "images", "images"],
            "delta": [32, 55, 48],
        }
    )
    pd.testing.assert_frame_equal(result, expected)


def test_pivot(images, deployments):
    result = compute_date_ranges(
        images=images, deployments=deployments, source="both", pivot=True
    )
    expected = pd.DataFrame(
        {
            ("start_date", "deployments"): pd.to_datetime(
                ["2021-02-13", "2021-02-01", "2021-03-01"]
            ),
            ("start_date", "images"): pd.to_datetime(
                ["2021-02-16", "2021-02-03", "2021-02-03"]
            ),
            ("end_date", "deployments"): pd.to_datetime(
                ["2021-03-23", "2021-04-03", "2021-03-27"]
            ),
            ("end_date", "images"): pd.to_datetime(
                ["2021-03-20", "2021-03-30", "2021-03-23"]
            ),
        },
        index=pd.Index(["001", "002", "003"], name="deployment_id"),
    )
    pd.testing.assert_frame_equal(result, expected, check_names=False)


def test_intact_input(images, deployments):
    images_original = images.copy()
    deployments_original = deployments.copy()
    compute_date_ranges(images=images, deployments=deployments, source="both")
    pd.testing.assert_frame_equal(images_original, images)
    pd.testing.assert_frame_equal(deployments_original, deployments)


def test_invalid_source(images, deployments):
    with pytest.raises(ValueError):
        compute_date_ranges(images=images, deployments=deployments, source="records")


def test_no_images(deployments):
    with pytest.raises(ValueError):
        compute_date_ranges(deployments=deployments, source="both")


def test_no_deployments(images):
    with pytest.raises(ValueError):
        compute_date_ranges(images=images, source="both")
