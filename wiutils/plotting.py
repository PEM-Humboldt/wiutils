"""

"""
from typing import Union

import matplotlib
import pandas as pd
import seaborn as sns

from . import _labels
from .filtering import remove_duplicates as _remove_duplicates
from .transformation import compute_detection_history


def plot_activity_hours(
    images: pd.DataFrame,
    names: Union[list, str, pd.Series],
    species_col: str = "scientific_name",
    remove_duplicates: bool = False,
    remove_duplicates_kws: dict = None,
    kind: str = "kde",
    hist_kws: dict = None,
    kde_kws: dict = None,
) -> matplotlib.axes.Axes:
    """

    Parameters
    ----------
    images
    names
    species_col
    remove_duplicates
    remove_duplicates_kws
    kind
    hist_kws
    kde_kws

    Returns
    -------

    """
    if isinstance(names, str):
        names = [names]

    if remove_duplicates_kws is None:
        remove_duplicates_kws = {}
    if hist_kws is None:
        hist_kws = {}
    if kde_kws is None:
        kde_kws = {}

    images = images.copy()

    if remove_duplicates:
        images = _remove_duplicates(images, **remove_duplicates_kws)

    images = images[images[species_col].isin(names)]
    images[_labels.date] = pd.to_datetime(images[_labels.date])
    images["hour"] = images[_labels.date].dt.round("H").dt.hour

    if kind == "hist":
        ax = sns.histplot(
            data=images,
            x="hour",
            hue=species_col,
            binwidth=1,
            binrange=(-0.5, 23.5),
            discrete=False,
            **hist_kws
        )
    elif kind == "kde":
        ax = sns.kdeplot(data=images, x="hour", hue=species_col, **kde_kws)
    else:
        raise ValueError("kind must be one of ['hist', 'kde']")

    ax.set_xlim(-1, 24)
    ax.set_xticks(range(0, 24, 2), labels=[f"{h:02}:00" for h in range(0, 24, 2)])

    return ax


def plot_detection_history(
    images: pd.DataFrame,
    deployments: pd.DataFrame,
    name: str,
    species_col: str = "scientific_name",
    mask: bool = False,
    compute_detection_history_kws: dict = None,
    heatmap_kws: dict = None,
) -> matplotlib.axes.Axes:
    """

    Parameters
    ----------
    images
    deployments
    name
    species_col
    mask
    compute_detection_history_kws
    heatmap_kws

    Returns
    -------

    """
    if compute_detection_history_kws is None:
        compute_detection_history_kws = {}
    if heatmap_kws is None:
        heatmap_kws = {}

    result = compute_detection_history(
        images, deployments, species_col, pivot=True, **compute_detection_history_kws
    )
    result = result[result[species_col] == name]
    result = result.drop(columns=species_col)
    result = result.set_index(_labels.site)

    if not mask:
        result = result.fillna(0)

    ax = sns.heatmap(data=result, **heatmap_kws)

    return ax


def plot_site_dates(deployments: pd.DataFrame, **kwargs) -> matplotlib.axes.Axes:
    """

    Parameters
    ----------
    deployments

    Returns
    -------

    """
    deployments = deployments.copy()

    deployments[_labels.start] = pd.to_datetime(deployments[_labels.start])
    deployments[_labels.end] = pd.to_datetime(deployments[_labels.end])

    df = pd.melt(
        deployments, id_vars=_labels.site, value_vars=[_labels.start, _labels.end]
    )
    df = df.rename(columns={"value": "date"})
    df = df.sort_values("date")

    ax = sns.lineplot(
        data=df, x="date", y=_labels.site, units=_labels.site, estimator=None, **kwargs
    )

    return ax
