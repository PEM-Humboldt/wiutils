"""
Test cases for the wiutils.plotting.plot_activity_hours function.
"""
import pandas as pd
import pytest
import seaborn

from wiutils.plotting import plot_activity_hours


@pytest.fixture()
def images():
    return pd.DataFrame(
        {
            "class": [
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
                "Mammalia",
            ],
            "order": [
                "Pilosa",
                "Pilosa",
                "Pilosa",
                "Pilosa",
                "Pilosa",
                "Pilosa",
                "Pilosa",
                "Carnivora",
                "Carnivora",
                "Carnivora",
            ],
            "family": [
                "Bradypodidae",
                "Bradypodidae",
                "Bradypodidae",
                "Bradypodidae",
                "Bradypodidae",
                "Bradypodidae",
                "Bradypodidae",
                "Ursidae",
                "Ursidae",
                "Ursidae",
            ],
            "genus": [
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Tremarctos",
                "Tremarctos",
                "Tremarctos",
            ],
            "species": [
                "variegatus",
                "variegatus",
                "variegatus",
                "variegatus",
                "variegatus",
                "variegatus",
                "variegatus",
                "ornatus",
                "ornatus",
                "ornatus",
            ],
            "timestamp": [
                "2020-11-16 08:13:13",
                "2020-11-16 08:15:05",
                "2020-11-18 15:16:46",
                "2020-11-19 15:22:38",
                "2020-11-21 15:15:57",
                "2020-11-21 21:12:32",
                "2020-11-29 21:14:04",
                "2020-11-30 11:01:58",
                "2020-12-05 09:02:41",
                "2020-12-11 11:13:09",
            ],
        }
    )


def test_hist(images, mocker):
    mocker.patch("seaborn.histplot")
    plot_activity_hours(images, "Bradypus variegatus", kind="hist")
    expected = pd.DataFrame(
        {
            "taxon": [
                "Bradypus variegatus",
                "Bradypus variegatus",
                "Bradypus variegatus",
                "Bradypus variegatus",
                "Bradypus variegatus",
                "Bradypus variegatus",
                "Bradypus variegatus",
            ],
            "hour": [8, 8, 15, 15, 15, 21, 21],
        }
    )
    args, kwargs = seaborn.histplot.call_args
    pd.testing.assert_frame_equal(kwargs["data"], expected)


def test_kde(images, mocker):
    mocker.patch("seaborn.kdeplot")
    plot_activity_hours(images, "Tremarctos ornatus", kind="kde")
    expected = pd.DataFrame(
        {
            "taxon": [
                "Tremarctos ornatus",
                "Tremarctos ornatus",
                "Tremarctos ornatus",
            ],
            "hour": [11, 9, 11],
        }
    )
    args, kwargs = seaborn.kdeplot.call_args
    pd.testing.assert_frame_equal(kwargs["data"], expected)


def test_multiple_names(images, mocker):
    mocker.patch("seaborn.histplot")
    plot_activity_hours(
        images, ["Bradypus variegatus", "Tremarctos ornatus"], kind="hist"
    )
    expected = pd.DataFrame(
        {
            "taxon": [
                "Bradypus variegatus",
                "Bradypus variegatus",
                "Bradypus variegatus",
                "Bradypus variegatus",
                "Bradypus variegatus",
                "Bradypus variegatus",
                "Bradypus variegatus",
                "Tremarctos ornatus",
                "Tremarctos ornatus",
                "Tremarctos ornatus",
            ],
            "hour": [8, 8, 15, 15, 15, 21, 21, 11, 9, 11],
        }
    )
    args, kwargs = seaborn.histplot.call_args
    pd.testing.assert_frame_equal(kwargs["data"], expected)


def test_intact_input(images, mocker):
    mocker.patch("seaborn.histplot")
    images_original = images.copy()
    plot_activity_hours(images, "Tremarctos ornatus", kind="hist")
    pd.testing.assert_frame_equal(images_original, images)


def test_invalid_kind(images):
    with pytest.raises(ValueError):
        plot_activity_hours(images, "Bradypus variegatus", kind="bar")


def test_invalid_species(images):
    with pytest.raises(ValueError):
        plot_activity_hours(images, "Panthera onca", kind="hist")
