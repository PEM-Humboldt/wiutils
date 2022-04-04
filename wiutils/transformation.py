"""
Functions to create new tables or modify existing ones from WI data.
"""
from typing import Union

import numpy as np
import pandas as pd

from . import _dwc, _labels, _utils
from .extraction import get_scientific_name as _get_scientific_name
from .filtering import _remove_wrapper


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


def compute_deployment_count_summary(
    images: pd.DataFrame,
    species_col: str = "scientific_name",
    add_records_by_class: bool = False,
    add_species_by_class: bool = False,
    remove_unidentified_kws: dict = None,
    remove_duplicates_kws: dict = None,
    remove_domestic: bool = False,
    remove_domestic_kws: dict = None,
) -> pd.DataFrame:
    """
    Computes a summary of images, records and species count by deployment.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.
    species_col : str
        Label of the scientific name column in the images DataFrame.
    add_records_by_class : bool
        Whether to add number of independent records discriminated by
        taxonomic class.
    add_species_by_class : bool
        Whether to add number of species discriminated by taxonomic class.
    remove_unidentified_kws : dict
        Keyword arguments for the wiutils.remove_unidentified function.
    remove_duplicates_kws : dict
        Keyword arguments for the wiutils.remove_duplicates function.
    remove_domestic : bool
        Whether to remove domestic species. Wrapper for the
        wiutils.remove_domestic function.
    remove_domestic_kws : dict
        Keyword arguments for the wiutils.remove_domestic function.

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

    if remove_domestic:
        if remove_domestic_kws is None:
            remove_domestic_kws = {}
        df = _remove_wrapper(df, domestic=True, domestic_kws=remove_domestic_kws)

    result = pd.DataFrame(index=sorted(df[_labels.site].unique()))
    result = result.join(df.groupby(_labels.site).size().rename("total_images"))
    df = _remove_wrapper(df, unidentified=True, unidentified_kws=remove_unidentified_kws)
    result = result.join(df.groupby(_labels.site).size().rename("identified_images"))
    df = _remove_wrapper(df, duplicates=True, duplicates_kws=remove_duplicates_kws)

    result = result.join(df.groupby(_labels.site).size().rename("records"))
    if add_records_by_class:
        classes = df[_labels.class_].dropna().unique()
        for class_ in classes:
            subset = df[df[_labels.class_] == class_]
            result = result.join(
                subset.groupby(_labels.site).size().rename(f"records_{class_.lower()}")
            )

    result = result.join(
        df.groupby(_labels.site)[species_col].nunique().rename("species")
    )
    if add_species_by_class:
        classes = df[_labels.class_].dropna().unique()
        for class_ in classes:
            subset = df[df[_labels.class_] == class_]
            result = result.join(
                subset.groupby(_labels.site)[species_col]
                .nunique()
                .rename(f"species_{class_.lower()}")
            )

    result.index.name = _labels.site
    result = result.reset_index()
    result.iloc[:, 1:] = result.iloc[:, 1:].fillna(0).astype(int)

    return result


def compute_detection_by_deployment(
    images: pd.DataFrame,
    species_col: str = "scientific_name",
    compute_abundance: bool = True,
    remove_unidentified: bool = False,
    remove_unidentified_kws: dict = None,
    remove_duplicates: bool = False,
    remove_duplicates_kws: dict = None,
    remove_domestic: bool = False,
    remove_domestic_kws: dict = None,
    pivot: bool = False,
):
    """
    Computes the detection (in terms of abundance or presence) of each
    species by deployment.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.
    species_col : str
        Label of the scientific name column in the images DataFrame.
    compute_abundance : bool
        Whether to compute the abundance for each deployment. If False,
        returns presence/absence for the deployments.
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
    pivot : bool
        Whether to pivot (reshape from long to wide format) the resulting
        DataFrame.

    Returns
    -------
    DataFrame
        DataFrame with the detection of each species by deployment.

    """
    df = images.copy()
    df = _remove_wrapper(
        df,
        remove_unidentified,
        remove_unidentified_kws,
        remove_duplicates,
        remove_duplicates_kws,
        remove_domestic,
        remove_domestic_kws,
    )

    result = df.groupby([species_col, _labels.site]).size()

    species = df[species_col].unique()
    sites = df[_labels.site].unique()
    idx = pd.MultiIndex.from_product([species, sites], names=[species_col, _labels.site])
    result = result.reindex(idx, fill_value=0)
    result.name = "value"
    result = result.reset_index()

    if not compute_abundance:
        has_observations = result["value"] > 0
        result.loc[has_observations, "value"] = 1

    result = result.sort_values([species_col, _labels.site], ignore_index=True)

    if pivot:
        result = result.pivot(index=species_col, columns=_labels.site, values="value")
        result = result.rename_axis(None, axis=1).reset_index()

    return result


def compute_detection_history(
    images: pd.DataFrame,
    deployments: pd.DataFrame,
    species_col: str = "scientific_name",
    date_range: str = "deployments",
    days: int = 1,
    compute_abundance: bool = True,
    remove_unidentified: bool = False,
    remove_unidentified_kws: dict = None,
    remove_duplicates: bool = False,
    remove_duplicates_kws: dict = None,
    remove_domestic: bool = False,
    remove_domestic_kws: dict = None,
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
    species_col : str
        Label of the scientific name column in the images DataFrame.
    date_range : str
        Table to compute the date range from. Possible values are:

            - 'deployments'
            - 'images'
    days : int
        Days interval to group observations into.
    compute_abundance : bool
        Whether to compute the abundance for each interval. If False,
        returns presence/absence for the intervals.
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

    df[_labels.date] = pd.to_datetime(df[_labels.date])
    df[_labels.date] = pd.to_datetime(df[_labels.date].dt.date)
    deployments[_labels.start] = pd.to_datetime(deployments[_labels.start])
    deployments[_labels.end] = pd.to_datetime(deployments[_labels.end])
    if date_range == "deployments":
        start = deployments[_labels.start].min()
        end = deployments[_labels.end].max()
    elif date_range == "images":
        start = df[_labels.date].min()
        end = df[_labels.date].max()
    else:
        raise ValueError("date_range must be one of ['deployments', 'images'].")

    df = _remove_wrapper(
        df,
        remove_unidentified,
        remove_unidentified_kws,
        remove_duplicates,
        remove_duplicates_kws,
        remove_domestic,
        remove_domestic_kws,
    )

    freq = pd.Timedelta(days=days)
    groupers = [
        pd.Grouper(key=species_col),
        pd.Grouper(key=_labels.site),
        pd.Grouper(key=_labels.date, freq=freq, origin=start),
    ]
    result = df.groupby(groupers).size()

    # A new index with all the combinations of species, sites and dates
    # is created to reindex the result and to assign zeros where there
    # were no observations.
    species = df[species_col].unique()
    sites = df[_labels.site].unique()
    dates = pd.date_range(start, end, freq=freq)
    idx = pd.MultiIndex.from_product(
        [species, sites, dates], names=[species_col, _labels.site, _labels.date]
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
        result,
        deployments[[_labels.site, _labels.start, _labels.end]],
        on=_labels.site,
        how="left",
    )
    group_start = result[_labels.date]
    group_end = result[_labels.date] + pd.Timedelta(days=days - 1)
    inside_range_left = group_start.between(result[_labels.start], result[_labels.end])
    inside_range_right = group_end.between(result[_labels.start], result[_labels.end])
    inside_range = inside_range_left | inside_range_right
    result.loc[~inside_range, "value"] = np.nan
    result = result.drop(columns=[_labels.start, _labels.end])

    result = result.sort_values(
        [species_col, _labels.site, _labels.date], ignore_index=True
    )

    if pivot:
        result[_labels.date] = result[_labels.date].astype(str)
        result = result.pivot(
            index=[species_col, _labels.site], columns=_labels.date, values="value"
        )
        result = result.rename_axis(None, axis=1).reset_index()

    return result


def compute_general_count(
    images: pd.DataFrame,
    species_col: str = "scientific_name",
    add_taxonomy: bool = True,
    rank: str = "class",
    remove_unidentified: bool = False,
    remove_unidentified_kws: dict = None,
    remove_duplicates: bool = False,
    remove_duplicates_kws: dict = None,
    remove_domestic: bool = False,
    remove_domestic_kws: dict = None,
):
    """
    Computes the general abundance and number of deployments for each
    species.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.
    species_col : str
        Label of the scientific name column in the images DataFrame.
    add_taxonomy : bool
        Whether to add the superior taxonomy of the species to the result.
    rank : str
        Upper taxonomic rank to extract classification for. Possible
        values are:

            - 'epithet'
            - 'genus'
            - 'family'
            - 'order'
            - 'class'
        For example, if rank is 'family', the result will have the
        corresponding family (and therefore the inferior ranks - genus
        and epithet -) were not identified will be removed.
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

    Returns
    -------
    DataFrame
        DataFrame with abundance and number of deployments by species.

    """
    df = images.copy()
    df = _remove_wrapper(
        df,
        remove_unidentified,
        remove_unidentified_kws,
        remove_duplicates,
        remove_duplicates_kws,
        remove_domestic,
        remove_domestic_kws,
    )

    result = df.groupby(species_col).agg({species_col: "size", _labels.site: "nunique"})
    result = result.rename(columns={species_col: "images", _labels.site: "deployments"})
    result = result.reset_index()

    if add_taxonomy:
        taxonomy_columns = _utils.taxonomy.get_taxonomy_columns(rank)
        taxonomy = df[[species_col, *taxonomy_columns]].drop_duplicates(species_col)
        result = pd.merge(result, taxonomy, on=species_col, how="left")

    return result


def compute_hill_numbers(
    images: pd.DataFrame,
    q_values: Union[int, list, tuple, np.ndarray],
    species_col: str = "scientific_name",
    remove_unidentified: bool = False,
    remove_unidentified_kws: dict = None,
    remove_duplicates: bool = False,
    remove_duplicates_kws: dict = None,
    remove_domestic: bool = False,
    remove_domestic_kws: dict = None,
    pivot: bool = False,
) -> pd.DataFrame:
    """
    Computes the Hill numbers of order q (also called effective number of
    species) by site for some given values of q.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.
    species_col : str
        Label of the scientific name column in the images DataFrame.
    q_values : int, list, tuple or array
        Value(s) of q to compute Hill numbers for.
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
    pivot : bool
        Whether to pivot (reshape from long to wide format) the resulting
        DataFrame.

    Returns
    -------
    DataFrame
        Computed Hill numbers by deployment.

    """
    df = images.copy()
    df = _remove_wrapper(
        df,
        remove_unidentified,
        remove_unidentified_kws,
        remove_duplicates,
        remove_duplicates_kws,
        remove_domestic,
        remove_domestic_kws,
    )

    if isinstance(q_values, int):
        q_values = [q_values]

    result = []

    abundance = df.groupby([_labels.site, species_col]).size()
    relative_abundance = abundance / abundance.groupby(level=0).sum()
    for site, group in relative_abundance.groupby(level=0):
        for q in q_values:
            row = {
                _labels.site: site,
                "q": q,
                "D": _compute_q_diversity_index(group.to_numpy(), q),
            }
            result.append(row)

    result = pd.DataFrame(result)

    if pivot:
        result["q"] = result["q"].astype(str)
        result = result.pivot(index=_labels.site, columns="q", values="D")
        result = result.rename_axis(None, axis=1).reset_index()

    return result


def create_dwc_events(
    deployments: pd.DataFrame, remove_empty_optionals: bool = False, language: str = "en"
) -> pd.DataFrame:
    """
    Creates an events Darwin Core compliant table from Wildlife Insights
    deployments information.

    Parameters
    ----------
    deployments : pd.DataFrame
        DataFrame with the project's deployments.
    remove_empty_optionals : bool
        Whether to remove empty optional columns.
    language : str
        Language of the result's values. Possible values are:

            - 'en' for english
            - 'es' for spanish
        Keep in mind that regardless of the value, column names will be
        kept in english to comply with the Darwin Core standard.

    Returns
    -------
    DataFrame
        Darwin Core standard compliant events table.

    """
    result = deployments.copy()

    result = result.rename(columns=_dwc.mapping.events)

    start_date = pd.to_datetime(result["start_date"])
    end_date = pd.to_datetime(result["end_date"])
    result["eventDate"] = (
        start_date.dt.strftime("%Y-%m-%d") + "/" + end_date.dt.strftime("%Y-%m-%d")
    )
    delta = end_date - start_date
    result["samplingEffort"] = delta.dt.days.astype(str) + " trap-nights"

    for column, value in _dwc.constants.events.items():
        result[column] = value

    if remove_empty_optionals:
        is_empty = result.isna().all()
        is_optional = result.columns.isin(_dwc.optional.events)
        subset = result.columns[~(is_empty & is_optional)]
        result = result[subset]

    if language == "en":
        pass
    elif language == "es":
        result = _utils.language.translate(result, language)
    else:
        raise ValueError("language must be one of ['en', 'es'].")

    result = _utils.data.rearrange(result, _dwc.order.events)

    return result


def create_dwc_records(
    images: pd.DataFrame,
    deployments: pd.DataFrame,
    remove_empty_optionals: bool = False,
    language: str = "en",
    remove_unidentified: bool = False,
    remove_unidentified_kws: dict = None,
    remove_duplicates: bool = False,
    remove_duplicates_kws: dict = None,
    remove_domestic: bool = False,
    remove_domestic_kws: dict = None,
) -> pd.DataFrame:
    """
    Creates a records Darwin Core compliant table from Wildlife Insights
    images and deployments information.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.
    deployments : pd.DataFrame
        DataFrame with the project's deployments.
    remove_empty_optionals : bool
        Whether to remove empty optional columns.
    language : str
        Language of the result's values. Possible values are:

            - 'en' for english
            - 'es' for spanish
        Keep in mind that regardless of the value, column names will be
        kept in english to comply with the Darwin Core standard.
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

    Returns
    -------
    DataFrame
        Darwin Core standard compliant records table.

    """
    df = images.copy()
    df["scientific_name"] = _get_scientific_name(df, keep_genus=True, add_qualifier=True)
    df = _remove_wrapper(
        df,
        remove_unidentified,
        remove_unidentified_kws,
        remove_duplicates,
        remove_duplicates_kws,
        remove_domestic,
        remove_domestic_kws,
    )

    result = pd.merge(df, deployments, on="deployment_id", how="left")

    remove_values = ["Blank", "No CV Result", "Unknown"]
    result = result.replace(remove_values, np.nan)

    result.loc[result["class"].notna(), "kingdom"] = "Animalia"
    result.loc[result["class"].notna(), "phylum"] = "Chordata"
    epithets = result["species"].str.split(" ", expand=True)
    result["specificEpithet"] = epithets[0]
    if 1 in epithets.columns:
        result["infraspecificEpithet"] = epithets[1]
    else:
        result["infraspecificEpithet"] = np.nan
    result["taxonRank"] = _utils.taxonomy.compute_taxonomic_rank(result)

    result["eventDate"] = pd.to_datetime(result["timestamp"]).dt.strftime("%Y-%m-%d")
    result["eventTime"] = pd.to_datetime(result["timestamp"]).dt.strftime("%H:%M:%S")

    result = result.rename(columns=_dwc.mapping.records)

    mask = (result["organismQuantity"] >= 1) & (result["taxonRank"].notna())
    result.loc[~mask, "organismQuantity"] = np.nan
    result.loc[mask, "organismQuantityType"] = "individuals"

    for column, value in _dwc.constants.records.items():
        result[column] = value

    if remove_empty_optionals:
        is_empty = result.isna().all()
        is_optional = result.columns.isin(_dwc.optional.records)
        subset = result.columns[~(is_empty & is_optional)]
        result = result[subset]

    if language == "en":
        pass
    elif language == "es":
        result = _utils.language.translate(result, language)
    else:
        raise ValueError("language must be one of ['en', 'es'].")

    result = _utils.data.rearrange(result, _dwc.order.records)

    return result
