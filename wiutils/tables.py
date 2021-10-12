"""
Functions to create new tables from WI data.
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


def compute_hill_numbers(
    df: pd.DataFrame,
    q_values: Union[int, list, tuple, np.ndarray],
    site_col: str = "deployment_id",
    species_col: str = "species",
    pivot: bool = False,
) -> pd.DataFrame:
    """
    Computes the Hill numbers of order q (also called effective number of
    species) by site for some given values of q.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with records.
    site_col : str
        Label of the site column.
    species_col : str
        Label of the scientific name column.
    q_values : int, list, tuple or array
        Value(s) of q to compute Hill numbers for.
    pivot : bool
        Whether to pivot (reshape from long to wide format) the resulting
        DataFrame.

    Returns
    -------
    DataFrame
        Computed Hill numbers by site.

    """
    df = df.copy()

    if isinstance(q_values, int):
        q_values = [q_values]

    result = pd.DataFrame(columns=["site", "q", "D"])

    abundance = df.groupby([site_col, species_col]).size()
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
    df: pd.DataFrame,
    date_col: str = "timestamp",
    site_col: str = "deployment_id",
    species_col: str = "species",
    interval: int = 30,
    unit: str = "m",
) -> pd.DataFrame:
    """
    Removes duplicate records (images) from a same species in the same
    site given a time interval.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with records.
    date_col : str
        Label of the date column.
    site_col : str
        Label of the site column.
    species_col : str
        Label of the scientific name column.
    interval : int
        Time interval (for a specific time unit).
    unit : str
        Time unit. Refer to pandas.Timedelta documentation for a list of
        possible values:
        https://pandas.pydata.org/docs/reference/api/pandas.Timedelta.html

    Returns
    -------
    DataFrame
        Copy of df with removed duplicates.

    """
    df = df.copy()

    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values([site_col, species_col, date_col])
    delta = df.groupby([site_col, species_col])[date_col].diff()
    mask = (delta >= pd.Timedelta(interval, unit=unit)) | (delta.isna())

    return df[mask]
