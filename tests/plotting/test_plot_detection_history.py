"""
Test cases for the wiutils.plotting.plot_detection_history function.
"""
import numpy as np
import pandas as pd
import pytest
import seaborn

from wiutils.plotting import plot_detection_history


@pytest.fixture()
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
                "001",
                "002",
                "002",
                "002",
            ],
            "scientific_name": [
                "Alouatta seniculus",
                "Alouatta seniculus",
                "Alouatta seniculus",
                "Alouatta seniculus",
                "Alouatta seniculus",
                "Tapirus terrestris",
                "Tapirus terrestris",
                "Tapirus terrestris",
                "Alouatta seniculus",
                "Alouatta seniculus",
                "Alouatta seniculus",
            ],
            "timestamp": [
                "2020-11-27 06:45:57",
                "2020-11-29 09:24:32",
                "2020-12-04 14:41:52",
                "2020-12-05 16:17:41",
                "2020-12-06 08:51:01",
                "2020-11-25 09:58:12",
                "2020-12-01 10:11:25",
                "2020-12-05 17:21:33",
                "2020-11-30 09:42:29",
                "2020-12-03 11:14:32",
                "2020-12-11 07:53:07",
            ],
        }
    )


@pytest.fixture()
def deployments():
    return pd.DataFrame(
        {
            "deployment_id": ["001", "002"],
            "start_date": ["2020-11-24", "2020-11-27"],
            "end_date": ["2020-12-07", "2020-12-14"],
        }
    )


def test_no_mask(images, deployments, mocker):
    mocker.patch("seaborn.heatmap")
    plot_detection_history(
        images,
        deployments,
        name="Alouatta seniculus",
        species_col="scientific_name",
        mask=False,
        compute_detection_history_kws=dict(days=7),
    )
    expected = pd.DataFrame(
        {
            "2020-11-24": [2.0, 1.0],
            "2020-12-01": [3.0, 1.0],
            "2020-12-08": [0, 1.0],
        },
        index=pd.Index(["001", "002"], name="deployment_id"),
    )
    args, kwargs = seaborn.heatmap.call_args
    pd.testing.assert_frame_equal(kwargs["data"], expected)


def test_mask(images, deployments, mocker):
    mocker.patch("seaborn.heatmap")
    plot_detection_history(
        images,
        deployments,
        name="Tapirus terrestris",
        species_col="scientific_name",
        mask=True,
        compute_detection_history_kws=dict(days=7, compute_abundance=True),
    )
    expected = pd.DataFrame(
        {
            "2020-11-24": [1.0, 0.0],
            "2020-12-01": [2.0, 0.0],
            "2020-12-08": [np.nan, 0.0],
        },
        index=pd.Index(["001", "002"], name="deployment_id"),
    )
    args, kwargs = seaborn.heatmap.call_args
    pd.testing.assert_frame_equal(kwargs["data"], expected)


def test_intact_input(images, deployments, mocker):
    mocker.patch("seaborn.heatmap")
    images_original = images.copy()
    deployments_original = deployments.copy()
    plot_detection_history(
        images, deployments, name="Alouatta seniculus", species_col="scientific_name"
    )
    pd.testing.assert_frame_equal(images_original, images)
    pd.testing.assert_frame_equal(deployments_original, deployments)


def test_invalid_species(images, deployments):
    with pytest.raises(ValueError):
        plot_detection_history(images, deployments, "Panthera onca")
