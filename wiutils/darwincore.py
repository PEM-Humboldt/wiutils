"""
Functions to create Darwin Core tables from a Wildlife Insights project.
"""
import pandas as pd
import numpy as np

from . import _dwc, _utils
from .extraction import get_scientific_name
from .filtering import _remove_wrapper


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
    deployments = deployments.copy()

    result = deployments.rename(columns=_dwc.mapping.events)

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
    images = images.copy()
    images["scientific_name"] = get_scientific_name(
        images, keep_genus=False, add_qualifier=False
    )
    images = _remove_wrapper(
        images,
        remove_unidentified,
        remove_unidentified_kws,
        remove_duplicates,
        remove_duplicates_kws,
        remove_domestic,
        remove_domestic_kws,
    )

    result = pd.merge(images, deployments, on="deployment_id", how="left")
    result = result.rename(
        columns={**_dwc.mapping.records, "scientific_name": "scientificName"}
    )

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

    # The Darwin Core standard specifies that the scientificName term
    # should be the name in the lowest level taxonomic rank that can be
    # determined. Thus, this taxon is retrieved by indexing the respective
    # ranks for those images where an identification different from
    # species was made.
    mask = (result["scientificName"].isna()) & (result["taxonRank"].notna())
    sorted_columns = np.argsort(result.columns)
    column_indices = np.searchsorted(
        result.columns[sorted_columns], result.loc[mask, "taxonRank"]
    )
    indices = sorted_columns[column_indices]
    result.loc[mask, "scientificName"] = result.loc[mask].values[
        np.arange(mask.sum()), indices
    ]

    result["eventDate"] = pd.to_datetime(result["timestamp"]).dt.strftime("%Y-%m-%d")
    result["eventTime"] = pd.to_datetime(result["timestamp"]).dt.strftime("%H:%M:%S")

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
