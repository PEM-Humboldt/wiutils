"""
Functions to filter WI images based on different conditions.
"""
import numpy as np
import pandas as pd

from . import _labels
from ._helpers import _convert_to_datetime, _get_taxonomy_columns


def remove_duplicates(
    images: pd.DataFrame,
    species_col: str = "scientific_name",
    interval: int = 30,
    unit: str = "minutes",
    reset_index: bool = True,
) -> pd.DataFrame:
    """
    Removes duplicate records (images) from a same species in the same
    site given a time interval.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.

    species_col : str
        Label of the scientific name column in the images DataFrame.
    interval : int
        Time interval (for a specific time unit).
    unit : str
        Time unit. Possible values are:

            - 'weeks'
            - 'days'
            - 'hours'
            - 'minutes'
            - 'seconds'
    reset_index : bool
        Whether to reset the index of the resulting DataFrame. If True,
        the index will be numeric from 0 to the length of the result.

    Returns
    -------
    DataFrame
        Copy of images with removed duplicates.

    """
    if unit not in ("weeks", "days", "hours", "minutes", "seconds"):
        raise ValueError(
            "unit must be one of ['weeks', 'days', 'hours', 'minutes', 'seconds']"
        )

    df = images.copy()
    df = _convert_to_datetime(df, _labels.date)

    df = df.sort_values([_labels.site, species_col, _labels.date])
    delta = df.groupby([_labels.site, species_col])[_labels.date].diff()
    mask = (delta >= pd.Timedelta(**{unit: interval})) | (delta.isna())

    images_reference = images.dropna(subset=[species_col])
    images_reference = images_reference.sort_values(
        [_labels.site, species_col, _labels.date]
    )
    df = images_reference[mask]
    df = df.append(images[images[species_col].isna()])
    df = df.sort_index()

    if reset_index:
        df = df.reset_index(drop=True)

    return df


def remove_inconsistent_dates(
    images: pd.DataFrame, deployments: pd.DataFrame, reset_index: bool = True
) -> pd.DataFrame:
    """
    Removes images where the timestamp is outside the date range of the
    corresponding camera.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.
    deployments : pd.DataFrame
        DataFrame with the project's deployments.
    reset_index : bool
        Whether to reset the index of the resulting DataFrame. If True,
        the index will be numeric from 0 to the length of the result.

    Returns
    -------
    DataFrame
        Images DataFrame with removed inconsistent images.

    """
    df = images.copy()
    deployments = deployments.copy()

    df = _convert_to_datetime(df, _labels.date)
    deployments = _convert_to_datetime(deployments, [_labels.start, _labels.end])

    df[_labels.date] = pd.to_datetime(df[_labels.date].dt.date)
    df = pd.merge(
        df,
        deployments[[_labels.site, _labels.start, _labels.end]],
        on=_labels.site,
        how="left",
    )
    df["__is_between"] = df[_labels.date].between(df[_labels.start], df[_labels.end])
    df = images[df["__is_between"]]

    if reset_index:
        df = df.reset_index(drop=True)

    return df


def remove_unidentified(
    images: pd.DataFrame, rank: str = "genus", reset_index: bool = True
) -> pd.DataFrame:
    """
    Removes unidentified (up to a specific taxonomic rank) images.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.
    rank : str
        Taxonomic rank for which images that do not have an identification
        will be removed. Possible values are:

            - 'epithet'
            - 'genus'
            - 'family'
            - 'order'
            - 'class'
        For example, if rank is 'family', all images where the family
        (and therefore the inferior ranks - genus and epithet -) were
        not identified will be removed.
    reset_index : bool
        Whether to reset the index of the resulting DataFrame. If True,
        the index will be numeric from 0 to the length of the result.

    Returns
    -------
    DataFrame
        Images DataFrame with removed unidentified images.

    """
    df = images.copy()

    taxonomy_columns = _get_taxonomy_columns(rank)
    exclude = ["No CV Result", "Unknown"]
    df[taxonomy_columns] = df[taxonomy_columns].replace(exclude, np.nan)
    df = df.dropna(subset=taxonomy_columns, how="all")

    if reset_index:
        df = df.reset_index(drop=True)

    return df
