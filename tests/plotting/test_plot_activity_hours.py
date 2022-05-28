"""
Test cases for the wiutils.plotting.plot_activity_hours function.
"""
import matplotlib.axes
import matplotlib.pyplot
import numpy as np
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
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
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
            "number_of_objects": [1, 1, 1, 3, 1, 1, 1, 1, 1, 2],
        }
    )


def test_hist(images, mocker):
    mocker.patch("seaborn.histplot")
    plot_activity_hours(images, "Bradypus", kind="hist")
    expected = pd.DataFrame(
        {
            "taxon": [
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
            ],
            "hour": [8.22, 8.25, 15.27, 15.37, 15.37, 15.37, 15.25, 21.20, 21.23],
        }
    )
    args, kwargs = seaborn.histplot.call_args
    pd.testing.assert_frame_equal(kwargs["data"], expected, atol=1e-2)


def test_hist_polar(images, mocker):
    mocker.patch("matplotlib.pyplot.subplot")
    mocker.patch("matplotlib.pyplot.thetagrids")
    ax = matplotlib.pyplot.subplot()
    mocker.patch.object(ax, "bar")
    plot_activity_hours(images, "Bradypus", kind="hist", polar=True)
    args, kwargs = ax.bar.call_args
    expected_x = np.arange(24) * (2 * np.pi / 24)
    np.testing.assert_array_equal(args[0], expected_x)
    expected_y = np.histogram(
        [8.22, 8.25, 15.27, 15.37, 15.37, 15.37, 15.25, 21.2, 21.23], bins=np.arange(25)
    )[0]
    np.testing.assert_array_equal(args[1], expected_y)


def test_hist_polar_kwargs(images, mocker):
    mocker.patch("matplotlib.pyplot.subplot")
    mocker.patch("matplotlib.pyplot.thetagrids")
    ax = matplotlib.pyplot.subplot()
    mocker.patch.object(ax, "bar")
    plot_activity_hours(
        images, "Bradypus", kind="hist", polar=True, polar_kws={"fill": False}
    )
    args, kwargs = ax.bar.call_args
    assert kwargs["fill"] is False


def test_kde(images, mocker):
    mocker.patch("seaborn.kdeplot")
    plot_activity_hours(images, "Tremarctos ornatus", kind="kde")
    expected = pd.DataFrame(
        {
            "taxon": [
                "Tremarctos ornatus",
                "Tremarctos ornatus",
                "Tremarctos ornatus",
                "Tremarctos ornatus",
            ],
            "hour": [11.02, 9.03, 11.22, 11.22],
        }
    )
    args, kwargs = seaborn.kdeplot.call_args
    pd.testing.assert_frame_equal(kwargs["data"], expected, atol=1e-2)


def test_area_polar(images, mocker):
    mocker.patch("matplotlib.pyplot.subplot")
    mocker.patch("matplotlib.pyplot.thetagrids")
    ax = matplotlib.pyplot.subplot()
    mocker.patch.object(ax, "plot")
    plot_activity_hours(images, "Tremarctos ornatus", kind="area", polar=True)
    args, kwargs = ax.plot.call_args
    width = 2 * np.pi / 24
    expected_x = np.arange(24) * width + (width / 2)
    expected_x = np.append(expected_x, expected_x[0])
    np.testing.assert_array_equal(args[0], expected_x)
    expected_y = np.histogram([11.02, 9.03, 11.22, 11.22], bins=np.arange(25))[0]
    expected_y = np.append(expected_y, expected_y[0])
    np.testing.assert_array_equal(args[1], expected_y)


def test_multiple_names(images, mocker):
    mocker.patch("seaborn.histplot")
    plot_activity_hours(images, ["Bradypus", "Tremarctos ornatus"], kind="hist")
    expected = pd.DataFrame(
        {
            "taxon": [
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Bradypus",
                "Tremarctos ornatus",
                "Tremarctos ornatus",
                "Tremarctos ornatus",
                "Tremarctos ornatus",
            ],
            "hour": [
                8.22,
                8.25,
                15.27,
                15.37,
                15.37,
                15.37,
                15.25,
                21.20,
                21.23,
                11.02,
                9.03,
                11.22,
                11.22,
            ],
        }
    )
    args, kwargs = seaborn.histplot.call_args
    pd.testing.assert_frame_equal(kwargs["data"], expected, atol=1e-2)


def test_intact_input(images, mocker):
    mocker.patch("seaborn.histplot")
    images_original = images.copy()
    plot_activity_hours(images, "Tremarctos ornatus", kind="hist")
    pd.testing.assert_frame_equal(images_original, images)


def test_invalid_kind_area(images):
    with pytest.raises(ValueError):
        plot_activity_hours(images, "Bradypus", kind="area")


def test_invalid_kind_other(images):
    with pytest.raises(ValueError):
        plot_activity_hours(images, "Bradypus", kind="bar")


def test_invalid_kind_polar_kde(images):
    with pytest.raises(ValueError):
        plot_activity_hours(images, "Bradypus", kind="kde", polar=True)


def test_invalid_kind_polar_other(images):
    with pytest.raises(ValueError):
        plot_activity_hours(images, "Bradypus", kind="bar", polar=True)


def test_invalid_species(images):
    with pytest.raises(ValueError):
        plot_activity_hours(images, "Panthera onca", kind="hist")
