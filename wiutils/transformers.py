"""
Functions to create new tables or modify existing ones from WI data.
"""
from typing import Union

import numpy as np
import pandas as pd

from ._helpers import _convert_to_datetime, _get_taxonomy_columns
from .filters import remove_duplicates, remove_unidentified


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


def compute_detection_by_deployment(
    images: pd.DataFrame,
    site_col: str = "deployment_id",
    species_col: str = "scientific_name",
    compute_abundance: bool = True,
    pivot: bool = False,
):
    """
    Computes the detection (in terms of abundance or presence) of each
    species by deployment.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.
    site_col : str
        Label of the site column in the images DataFrame.
    species_col : str
        Label of the scientific name column in the images DataFrame.
    compute_abundance : bool
        Whether to compute the abundance for each deployment. If False,
        returns presence/absence for the deployments.
    pivot : bool
        Whether to pivot (reshape from long to wide format) the resulting
        DataFrame.

    Returns
    -------
    DataFrame
        DataFrame with the detection of each species by deployment.

    """
    result = images.groupby([species_col, site_col]).size()

    species = images[species_col].unique()
    sites = images[site_col].unique()
    idx = pd.MultiIndex.from_product([species, sites], names=[species_col, site_col])
    result = result.reindex(idx, fill_value=0)
    result.name = "value"
    result = result.reset_index()

    if not compute_abundance:
        has_observations = result["value"] > 0
        result.loc[has_observations, "value"] = 1

    result = result.sort_values([species_col, site_col], ignore_index=True)

    if pivot:
        result = result.pivot(index=species_col, columns=site_col, values="value")
        result = result.rename_axis(None, axis=1).reset_index()

    return result


def compute_deployment_count_summary(
    images: pd.DataFrame,
    site_col: str = "deployment_id",
    species_col: str = "scientific_name",
    remove_unidentified_kws: dict = None,
    remove_duplicates_kws: dict = None,
) -> pd.DataFrame:
    """
    Computes a summary of images, records and species count by deployment.
    
    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.
    site_col : str
        Label of the site column in the images DataFrame.
    species_col : str
        Label of the scientific name column in the images DataFrame.
    remove_unidentified_kws : dict
        Keyword arguments for the wiutils.remove_unidentified function.
    remove_duplicates_kws : dict
        Keyword arguments for the wiutils.remove_duplicates function.

    Returns
    -------
    DataFrame
        Summary of images, records and species count by deployment.

    """
    df = images.copy()

    if remove_unidentified_kws is None:
        remove_unidentified_kws = {}
    if remove_duplicates_kws is None:
        remove_duplicates_kws = {}

    result = pd.DataFrame(index=sorted(df[site_col].unique()))
    result = result.join(df.groupby(site_col).size().rename("total_images"))
    df = remove_unidentified(df, **remove_unidentified_kws)
    result = result.join(df.groupby(site_col).size().rename("identified_images"))
    df = remove_duplicates(df, **remove_duplicates_kws)
    result = result.join(df.groupby(site_col).size().rename("independent_records"))
    result = result.join(df.groupby(site_col)[species_col].nunique().rename("species"))

    result.index.name = site_col
    result = result.reset_index()

    return result


def compute_detection_history(
    images: pd.DataFrame,
    deployments: pd.DataFrame,
    date_col: str = "timestamp",
    site_col: str = "deployment_id",
    species_col: str = "scientific_name",
    start_col: str = "start_date",
    end_col: str = "end_date",
    date_range: str = "deployments",
    days: int = 1,
    compute_abundance: bool = True,
    pivot: bool = False,
) -> pd.DataFrame:
    """
    Computes the detection history (in terms of abundance or presence) by
    species and deployment, grouping observations into specific days-long
    intervals.

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
    date_range : str
        Table to compute the date range from. Possible values are:

            - 'deployments'
            - 'images'
    days : int
        Days interval to group observations into.
    compute_abundance : bool
        Whether to compute the abundance for each interval. If False,
        returns presence/absence for the intervals.
    pivot : bool
        Whether to pivot (reshape from long to wide format) the resulting
        DataFrame.

    Returns
    -------
    DataFrame
        Detection history.

    """
    df = images.copy()
    deployments = deployments.copy()

    df = _convert_to_datetime(df, date_col)
    df[date_col] = pd.to_datetime(df[date_col].dt.date)
    if date_range == "deployments":
        deployments = _convert_to_datetime(deployments, [start_col, end_col])
        start = deployments[start_col].min()
        end = deployments[end_col].max()
    elif date_range == "images":
        start = df[date_col].min()
        end = df[date_col].max()
    else:
        raise ValueError("date_range must be one of ['deployments', 'images'].")

    freq = pd.Timedelta(days=days)
    groupers = [
        pd.Grouper(key=species_col),
        pd.Grouper(key=site_col),
        pd.Grouper(key=date_col, freq=freq, origin=start),
    ]
    result = df.groupby(groupers).size()

    # A new index with all the combinations of species, sites and dates
    # is created to reindex the result and to assign zeros where there
    # were no observations.
    species = df[species_col].unique()
    sites = df[site_col].unique()
    dates = pd.date_range(start, end, freq=freq)
    idx = pd.MultiIndex.from_product(
        [species, sites, dates], names=[species_col, site_col, date_col]
    )
    result = result.reindex(idx, fill_value=0)
    result.name = "value"
    result = result.reset_index()

    if not compute_abundance:
        has_observations = result["value"] > 0
        result.loc[has_observations, "value"] = 1

    # Groups (i.e. days intervals) where the corresponding camera was not
    # deployed at the time are assigned NaNs.
    result = pd.merge(
        result, deployments[[site_col, start_col, end_col]], on=site_col, how="left"
    )
    group_start = result[date_col]
    group_end = result[date_col] + pd.Timedelta(days=days-1)
    inside_range_left = group_start.between(result[start_col], result[end_col])
    inside_range_right = group_end.between(result[start_col], result[end_col])
    inside_range = inside_range_left | inside_range_right
    result.loc[~inside_range, "value"] = np.nan
    result = result.drop(columns=[start_col, end_col])

    result = result.sort_values([species_col, site_col, date_col], ignore_index=True)

    if pivot:
        result[date_col] = result[date_col].astype(str)
        result = result.pivot(
            index=[species_col, site_col], columns=date_col, values="value"
        )
        result = result.rename_axis(None, axis=1).reset_index()

    return result


def compute_general_count(
    images: pd.DataFrame,
    site_col: str = "deployment_id",
    species_col: str = "scientific_name",
    add_taxonomy: bool = True,
    rank: str = "class",
    class_col: str = "class",
    order_col: str = "order",
    family_col: str = "family",
    genus_col: str = "genus",
    epithet_col: str = "species"
):
    """
    Computes the general abundance and number of deployments for each
    species.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.
    site_col : str
        Label of the site column in the images DataFrame.
    species_col : str
        Label of the scientific name column in the images DataFrame.
    add_taxonomy : bool
        Whether to add the superior taxonomy of the species to the result.
    rank : str
        Upper taxonomic rank to extract classification for:

            - 'epithet'
            - 'genus'
            - 'family'
            - 'order'
            - 'class'
        For example, if rank is 'family', the result will have the
        corresponding family (and therefore the inferior ranks - genus
        and epithet -) were not identified will be removed.
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

    Returns
    -------
    DataFrame
        DataFrame with abundance and number of deployments by species.

    """
    result = images.groupby(species_col).agg({species_col: "size", site_col: "nunique"})
    result = result.rename(columns={species_col: "images", site_col: "deployments"})
    result = result.reset_index()

    if add_taxonomy:
        taxonomy_columns = _get_taxonomy_columns(
            rank, class_col, order_col, family_col, genus_col, epithet_col
        )
        taxonomy = images[[species_col, *taxonomy_columns]].drop_duplicates(species_col)
        result = pd.merge(result, taxonomy, on=species_col, how="left")

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

    result = pd.DataFrame(columns=[site_col, "q", "D"])

    abundance = images.groupby([site_col, species_col]).size()
    relative_abundance = abundance / abundance.groupby(level=0).sum()
    for site, group in relative_abundance.groupby(level=0):
        for q in q_values:
            row = {
                site_col: site,
                "q": q,
                "D": _compute_q_diversity_index(group.to_numpy(), q),
            }
            result = result.append(row, ignore_index=True)

    result["q"] = result["q"].astype(int)

    if pivot:
        result["q"] = result["q"].astype(str)
        result = result.pivot(index=site_col, columns="q", values="D")
        result = result.rename_axis(None, axis=1).reset_index()

    return result
