"""
Functions to filter WI images based on different conditions.
"""
import numpy as np
import pandas as pd

from ._helpers import _convert_to_datetime, _get_taxonomy_columns


def remove_duplicates(
    images: pd.DataFrame,
    site_col: str = "deployment_id",
    species_col: str = "scientific_name",
    date_col: str = "timestamp",
    interval: int = 30,
    unit: str = "minutes",
    reset_index: bool = True
) -> pd.DataFrame:
    """
    Removes duplicate records (images) from a same species in the same
    site given a time interval.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.

    site_col : str
        Label of the site column in the images DataFrame.
    species_col : str
        Label of the scientific name column in the images DataFrame.
    date_col : str
        Label of the date column in the images DataFrame.
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
    df = _convert_to_datetime(df, date_col)

    df = df.sort_values([site_col, species_col, date_col])
    delta = df.groupby([site_col, species_col])[date_col].diff()
    mask = (delta >= pd.Timedelta(**{unit: interval})) | (delta.isna())

    images_reference = images.dropna(subset=[species_col])
    images_reference = images_reference.sort_values([site_col, species_col, date_col])
    df = images_reference[mask]
    df = df.append(images[images[species_col].isna()])
    df = df.sort_index()

    if reset_index:
        df = df.reset_index(drop=True)

    return df


def remove_inconsistent_dates(
    images: pd.DataFrame,
    deployments: pd.DataFrame,
    date_col: str = "timestamp",
    site_col: str = "deployment_id",
    start_col: str = "start_date",
    end_col: str = "end_date",
    reset_index: bool = True
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
    date_col : str
        Label of the date column in the images DataFrame.
    site_col : str
        Label of the site column in the images DataFrame.
    start_col : str
        Label of the start date in the deployments DataFrame.
    end_col : str
        Label of the end date in the deployments DataFrame.
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

    df = _convert_to_datetime(df, date_col)
    deployments = _convert_to_datetime(deployments, [start_col, end_col])

    df[date_col] = pd.to_datetime(df[date_col].dt.date)
    df = pd.merge(
        df, deployments[[site_col, start_col, end_col]], on=site_col, how="left"
    )
    df["__is_between"] = df[date_col].between(df[start_col], df[end_col])
    df = images[df["__is_between"]]

    if reset_index:
        df = df.reset_index(drop=True)

    return df


def remove_unidentified(
    images: pd.DataFrame,
    rank: str = "genus",
    class_col: str = "class",
    order_col: str = "order",
    family_col: str = "family",
    genus_col: str = "genus",
    epithet_col: str = "species",
    reset_index: bool = True,
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
    class_col : str
        Label of the class column in the images DataFrame.
    order_col : str
        Label of the order column in the images DataFrame.
    family_col : str
        Label of the family column in the images DataFrame.
    genus_col : str
        Label of the genus column in the images DataFrame.
    epithet_col : str
        Label of the epithet column in the images DataFrame.
    reset_index : bool
        Whether to reset the index of the resulting DataFrame. If True,
        the index will be numeric from 0 to the length of the result.

    Returns
    -------
    DataFrame
        Images DataFrame with removed unidentified images.

    """
    df = images.copy()

    taxonomy_columns = _get_taxonomy_columns(
        rank, class_col, order_col, family_col, genus_col, epithet_col
    )
    exclude = ["No CV Result", "Unknown"]
    df[taxonomy_columns] = df[taxonomy_columns].replace(exclude, np.nan)
    df = df.dropna(subset=taxonomy_columns, how="all")

    if reset_index:
        df = df.reset_index(drop=True)

    return df
