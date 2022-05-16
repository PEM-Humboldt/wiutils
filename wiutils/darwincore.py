"""
Functions to create Darwin Core tables from a Wildlife Insights project.
"""
import numpy as np
import pandas as pd

from . import _dwc, _labels, _utils
from .extraction import get_lowest_taxon
from .filtering import _remove_wrapper


def create_dwc_events(
    deployments: pd.DataFrame,
    remove_empty_optionals: bool = False,
    language: str = "en",
) -> pd.DataFrame:
    """
    Creates an events Darwin Core compliant table from Wildlife Insights
    deployments information.

    Parameters
    ----------
    deployments : DataFrame
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
    images : DataFrame
        DataFrame with the project's images.
    deployments : DataFrame
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
    images = _utils.taxonomy.replace_unidentified(images)
    images[_labels.images.name] = images[_labels.images.name].replace("Blank", np.nan)
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
    result = result.rename(columns=_dwc.mapping.records)

    result.loc[result["class"].notna(), "kingdom"] = "Animalia"
    result.loc[result["class"].notna(), "phylum"] = "Chordata"

    taxa, ranks = get_lowest_taxon(images, return_rank=True)
    result["scientificName"] = taxa
    result["taxonRank"] = ranks

    epithets = images[_labels.images.epithet].str.split(" ", expand=True)
    result["specificEpithet"] = epithets[0]
    if 1 in epithets.columns:
        result["infraspecificEpithet"] = epithets[1]
    else:
        result["infraspecificEpithet"] = np.nan

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
