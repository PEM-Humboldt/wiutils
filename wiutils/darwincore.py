"""
Functions to create different core and extension tables following the
Darwin Core (DwC) standard from a Wildlife Insights data.
"""
import json
import pathlib

import numpy as np
import pandas as pd

from . import _dwc, _labels, _utils
from .extraction import get_lowest_taxon


def _translate(df: pd.DataFrame, language: str) -> pd.DataFrame:
    if language == "en":
        return df
    elif language in ("es",):
        words = _dwc.nls.es.words
    else:
        raise ValueError("language must be one of ['en', 'es'].")

    existing_columns = set(words.keys()) & set(df.columns)
    for column in existing_columns:
        df[column] = df[column].replace(words[column], regex=True)

    return df


def create_dwc_archive(
    cameras: pd.DataFrame,
    deployments: pd.DataFrame,
    images: pd.DataFrame,
    projects: pd.DataFrame,
    language: str = "en",
) -> tuple:
    """

    Parameters
    ----------
    cameras
    deployments
    images
    projects
    language

    Returns
    -------

    """
    event = create_dwc_event(deployments, projects, language)

    return (event,)


def create_dwc_event(
    deployments: pd.DataFrame,
    projects: pd.DataFrame,
    language: str = "en",
) -> pd.DataFrame:
    """

    Parameters
    ----------
    deployments
    projects
    language

    Returns
    -------

    """
    df = pd.merge(deployments, projects, on=_labels.deployments.project_id, how="left")
    df[_labels.deployments.start] = pd.to_datetime(df[_labels.deployments.start])
    df[_labels.deployments.end] = pd.to_datetime(df[_labels.deployments.end])

    core = df.rename(columns=_dwc.event.mapping)
    core = core[core.columns[core.columns.isin(_dwc.event.order)]]

    for term, value in _dwc.event.constants.items():
        core[term] = value

    delta = df[_labels.deployments.end] - df[_labels.deployments.start]
    core["samplingEffort"] = delta.dt.days.astype(str) + " trap-nights"

    core["eventDate"] = (
        df[_labels.deployments.start].dt.strftime("%Y-%m-%d")
        + "/"
        + df[_labels.deployments.end].dt.strftime("%Y-%m-%d")
    )

    with open(pathlib.Path(__file__).parent.joinpath("_dwc/countries.json")) as f:
        countries = pd.DataFrame(json.load(f))
        core["countryCode"] = core["countryCode"].map(
            countries.set_index("alpha-3")["alpha-2"]
        )

    core = _translate(core, language)
    core = core.reindex(columns=_dwc.event.order)

    return core


def create_dwc_measurement():
    pass


def create_dwc_multimedia():
    pass


def create_dwc_occurrence():
    pass


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

    result = deployments.rename(columns=_dwc.mapping.event)

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

    Returns
    -------
    DataFrame
        Darwin Core standard compliant records table.

    """
    images = images.copy()
    images = _utils.taxonomy.replace_unidentified(images)
    images[_labels.images.name] = images[_labels.images.name].replace("Blank", np.nan)

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
