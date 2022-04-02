"""
Functions to plot information from the images and deployments tables.
"""
from typing import Union

import matplotlib
import pandas as pd
import seaborn as sns

from . import _labels
from .filtering import _remove_wrapper
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
    Plots the activity hours of one or multiple species by grouping all
    observations into a 24-hour range.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    names : list, str or Series
        List of names to plot activity hours for.
    species_col : str
        Label of the scientific name column in the images DataFrame.
    remove_duplicates : bool
        Whether to remove duplicates. Wrapper for the
        wiutils.remove_duplicates function.
    remove_duplicates_kws : dict
        Keyword arguments for the wiutils.remove_duplicates function.
    kind : str
        Type of plot. Values can be:

        - 'hist' for histogram.
        - 'kde' for kernel density estimate plot.
    hist_kws : dict
        Keyword arguments passed to the seaborn.histplot() function. Only
        has effect if kind is 'hist'.
    kde_kws : dict
        Keyword arguments passed to the seaborn.kde() function. Only
        has effect if kind is 'kde'.

    Returns
    -------
    Axes
        Plot axes.

    """
    if isinstance(names, str):
        names = [names]

    if hist_kws is None:
        hist_kws = {}
    if kde_kws is None:
        kde_kws = {}

    images = images.copy()

    if remove_duplicates:
        images = _remove_wrapper(
            images, duplicates=True, duplicates_kws=remove_duplicates_kws
        )

    images = images.loc[images[species_col].isin(names), :].reset_index(drop=True)
    images[_labels.date] = pd.to_datetime(images[_labels.date])
    images["hour"] = images[_labels.date].dt.round("H").dt.hour
    images = images.drop(columns=_labels.date)

    if kind == "hist":
        ax = sns.histplot(
            data=images,
            x="hour",
            hue=species_col,
            binwidth=1,
            binrange=(-0.5, 23.5),
            discrete=False,
            **hist_kws,
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
    Plots detection history matrix for a given species.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    deployments : DataFrame
        DataFrame with the project's deployments.
    name : str
        Scientific name of the species to plot the detection history for.
    species_col : str
        Label of the scientific name column in the images DataFrame.
    mask : bool
        Whether to mask cells where cameras were not functioning. If True,
        those cells won't be displayed. Otherwise, they will be displayed
        as zero.
    compute_detection_history_kws : dict
        Keyword arguments for the wiutils.compute_detection_history()
        function.
    heatmap_kws : dict
        Keyword arguments for the seaborn.heatmap() function.

    Returns
    -------
    Axes
        Plot axes.

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


def plot_deployment_dates(
    images: pd.DataFrame = None,
    deployments: pd.DataFrame = None,
    source="both",
    remove_unidentified: bool = False,
    remove_unidentified_kws: dict = None,
    remove_duplicates: bool = False,
    remove_duplicates_kws: dict = None,
    remove_domestic: bool = False,
    remove_domestic_kws: dict = None,
    **kwargs,
) -> matplotlib.axes.Axes:
    """
    Plots deployment date ranges.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    deployments : DataFrame
        DataFrame with the project's deployments.
    source : bool
        Source to plot date ranges from: Values can be:

            - 'images' to plot date ranges from images (i.e. first image
            to last image taken).
            - 'deployments' to plot date ranges from deployments
            information (i.e. start date and end date).
            - 'both' to plot both sources in two different subplots.
    remove_unidentified : bool
        Whether to remove unidentified images. Wrapper for the
        wiutils.remove_unidentified function.
    remove_unidentified_kws : dict
        Keyword arguments for the wiutils.remove_unidentified function.
    remove_duplicates : bool
        Whether to remove duplicates. Wrapper for the
        wiutils.remove_duplicates function.
    remove_duplicates_kws : dict
        Keyword arguments for the wiutils.remove_duplicates function.
    remove_domestic : bool
        Whether to remove domestic species. Wrapper for the
        wiutils.remove_domestic function.
    remove_domestic_kws : dict
        Keyword arguments for the wiutils.remove_domestic function.
    kwargs

    Returns
    -------
    Axes
        Plot axes.

    """
    df = pd.DataFrame()

    if source == "images" or source == "both":
        if images is None:
            raise ValueError("images DataFrame must be provided.")
        images = images.copy()
        images = _remove_wrapper(
            images,
            remove_unidentified,
            remove_unidentified_kws,
            remove_duplicates,
            remove_duplicates_kws,
            remove_domestic,
            remove_domestic_kws,
        )
        images[_labels.date] = pd.to_datetime(images[_labels.date])
        dates = images.groupby(_labels.site)[_labels.date].agg(
            start_date="min", end_date="max"
        )
        dates["source"] = "images"
        df = pd.concat([df, dates.reset_index()], ignore_index=True)
    elif source == "deployments" or source == "both":
        if deployments is None:
            raise ValueError("deployments DataFrame must be provided.")
        deployments = deployments.copy()
        deployments[_labels.start] = pd.to_datetime(deployments[_labels.start])
        deployments[_labels.end] = pd.to_datetime(deployments[_labels.end])
        dates = deployments.loc[:, [_labels.site, _labels.start, _labels.end]]
        dates["source"] = "deployments"
        df = pd.concat([df, dates], ignore_index=True)
    else:
        raise ValueError("source must be one of ['images', 'deployments', 'both']")

    df = pd.melt(
        df, id_vars=[_labels.site, "source"], value_vars=[_labels.start, _labels.end]
    )
    df = df.rename(columns={"value": "date"})
    df = df.sort_values("date")

    g = sns.relplot(
        data=df,
        x="date",
        y=_labels.site,
        row="source",
        kind="line",
        units=_labels.site,
        estimator=None,
        **kwargs,
    )

    return g.axes
