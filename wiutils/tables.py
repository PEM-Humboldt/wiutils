"""
Functions to create new tables or modify existing ones from WI data.
"""
from typing import Union

import numpy as np
import pandas as pd


def _compute_q_diversity_index(p: Union[list, tuple, np.ndarray], q: int) -> float:
    """
    Computes the corresponding diversity index (from the Hill numbers of
    order q or effective number of species) for a given value of q.

    Parameters
    ----------
    p : list, tuple or array
        Proportional abundance values for each species.
    q : int
        Value of q to compute the diversity index for.

    Returns
    -------
    float
        Diversity index for a given value of q.

    """
    if q == 1:
        return np.exp(-np.sum(p * np.log(p)))
    else:
        return np.sum(p ** q) ** (1 / (1 - q))


def add_scientific_name():
    pass


def compute_abundance_by_deployment():
    pass


def compute_detection_history(
    images: pd.DataFrame,
    deployments: pd.DataFrame,
    date_col: str = "timestamp",
    site_col: str = "deployment_id",
    species_col: str = "scientific_name",
    start_col: str = "start_date",
    end_col: str = "end_date",
    compute_abundance: bool = True,
    interval: int = 1,
    unit: str = "days",
    pivot: bool = False
) -> pd.DataFrame:
    """

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
    species_col : str
        Label of the scientific name column in the images DataFrame.
    start_col : str
        Label of the start date in the deployments DataFrame.
    end_col : str
        Label of the end date in the deployments DataFrame.
    compute_abundance : bool
        Whether to compute the abundance for each interval. If False,
        returns presence/absence for the intervals.
    interval : int
        Time interval (for a specific time unit) to group observations
        into.
    unit : str
        Time unit. Possible values are:
            * 'weeks'
            * 'days'
            * 'hours'
            * 'minutes'
    pivot : bool
        Whether to pivot (reshape from long to wide format) the resulting
        DataFrame.

    Returns
    -------

    """
    freq = pd.Timedelta(**{unit: interval})
    groupers = [
        pd.Grouper(key=species_col),
        pd.Grouper(key=site_col),
        pd.Grouper(key=date_col, freq=freq)
    ]
    result = images.groupby(groupers).size()

    # TODO explain why we need to reindex (hint: fill all the dates)
    species = images[species_col].unique()
    sites = images[site_col].unique()
    dates = pd.date_range(
        deployments[start_col].min(), deployments[end_col].max(), freq=freq
    )
    idx = pd.MultiIndex.from_product(
        [species, sites, dates], names=[species_col, site_col, date_col]
    )
    result = result.reindex(idx, fill_value=0)
    result.name = "value"
    result = result.reset_index()

    if not compute_abundance:
        presence = result["value"] > 0
        result.loc[presence, "value"] = 1

    result = pd.merge(
        result, deployments[[site_col, start_col, end_col]], on=site_col, how="outer"
    )
    inside_range = result[date_col].between(result[start_col], result[end_col])
    result.loc[~inside_range, "value"] = pd.NA
    result = result.drop(columns=[start_col, end_col])

    if pivot:
        result = result.pivot(
            index=[species_col, site_col], columns=date_col, values="value"
        )
        result = result.reset_index()

    return result


def compute_hill_numbers(
    images: pd.DataFrame,
    q_values: Union[int, list, tuple, np.ndarray],
    site_col: str = "deployment_id",
    species_col: str = "scientific_name",
    pivot: bool = False,
) -> pd.DataFrame:
    """
    Computes the Hill numbers of order q (also called effective number of
    species) by site for some given values of q.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.
    site_col : str
        Label of the site column in the images DataFrame.
    species_col : str
        Label of the scientific name column in the images DataFrame.
    q_values : int, list, tuple or array
        Value(s) of q to compute Hill numbers for.
    pivot : bool
        Whether to pivot (reshape from long to wide format) the resulting
        DataFrame.

    Returns
    -------
    DataFrame
        Computed Hill numbers by deployment.

    """
    if isinstance(q_values, int):
        q_values = [q_values]

    result = pd.DataFrame(columns=["site", "q", "D"])

    abundance = images.groupby([site_col, species_col]).size()
    relative_abundance = abundance / abundance.groupby(level=0).sum()
    for site, group in relative_abundance.groupby(level=0):
        for q in q_values:
            row = {
                "site": site,
                "q": q,
                "D": _compute_q_diversity_index(group.to_numpy(), q)
            }
            result = result.append(row, ignore_index=True)

    if pivot:
        result = result.pivot(index=site_col, columns="q", values="D")

    return result


def remove_duplicates(
    images: pd.DataFrame,
    date_col: str = "timestamp",
    site_col: str = "deployment_id",
    species_col: str = "scientific_name",
    interval: int = 30,
    unit: str = "minutes",
) -> pd.DataFrame:
    """
    Removes duplicate records (images) from a same species in the same
    site given a time interval.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.
    date_col : str
        Label of the date column in the images DataFrame.
    site_col : str
        Label of the site column in the images DataFrame.
    species_col : str
        Label of the scientific name column in the images DataFrame.
    interval : int
        Time interval (for a specific time unit).
    unit : str
        Time unit. Possible values are:
            * 'weeks'
            * 'days'
            * 'hours'
            * 'minutes'
            * 'seconds'

    Returns
    -------
    DataFrame
        Copy of images with removed duplicates.

    """
    images = images.copy()

    images = images.sort_values([site_col, species_col, date_col])
    delta = images.groupby([site_col, species_col])[date_col].diff()
    mask = (delta >= pd.Timedelta(**{unit: interval})) | (delta.isna())

    return images[mask]


def remove_unidentified(df: pd.DataFrame) -> pd.DataFrame:
    pass
