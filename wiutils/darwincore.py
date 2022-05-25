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


def _gs_to_https(location: pd.Series) -> pd.Series:
    base_url = "https://console.cloud.google.com/storage/browser/"
    bucket = location.str.split("/").str[2]
    uri = location.str.split("/").str[4:].str.join("/")

    return base_url + bucket + "/" + uri


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
    cameras : DataFrame
        Dataframe with the bundle's cameras.
    deployments : DataFrame
        Dataframe with the bundle's deployments.
    images : DataFrame
        Dataframe with the bundle's cameras.
    projects : DataFrame
        Dataframe with the bundle's projects.
    language : str
        Language of the result's values. Possible values are:

            - 'en' for english
            - 'es' for spanish
        Keep in mind that regardless of the value, terms will be kept in
        english to comply with the Darwin Core standard.

    Returns
    -------
    DataFrame
        Darwin Core Event dataframe.
    DataFrame
        Darwin Core Measurement or Facts dataframe.
    DataFrame
        Darwin Core Simple Multimedia dataframe.

    """
    event = create_dwc_event(deployments, projects, language)
    measurement = create_dwc_measurement(cameras, deployments)
    multimedia = create_dwc_multimedia(images)

    return event, measurement, multimedia


def create_dwc_event(
    deployments: pd.DataFrame,
    projects: pd.DataFrame,
    language: str = "en",
) -> pd.DataFrame:
    """
    Creates a Darwin Core Event dataframe from deployments and projects
    information. See https://rs.gbif.org/core/dwc_event_2022-02-02.xml
    for more information about this core.

    Parameters
    ----------
    deployments : DataFrame
        Dataframe with the bundle's deployments.
    projects : DataFrame
        Dataframe with the bundle's projects.
    language : str
        Language of the result's values. Possible values are:

            - 'en' for english
            - 'es' for spanish
        Keep in mind that regardless of the value, terms will be kept in
        english to comply with the Darwin Core standard.

    Returns
    -------
    DataFrame
        Darwin Core Event dataframe.

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


def create_dwc_measurement(
    cameras: pd.DataFrame, deployments: pd.DataFrame, language: str = "en"
) -> pd.DataFrame:
    """
    Creates a Darwin Core Measurement or Facts dataframe from cameras and
    deployments information. See https://rs.gbif.org/extension/dwc/measurements_or_facts_2022-02-02.xml
    for more information about this extension.

    Parameters
    ----------
    cameras : DataFrame
        Dataframe with the bundle's cameras.
    deployments : DataFrame
        Dataframe with the bundle's deployments.
    language : str
        Language of the result's values. Possible values are:

            - 'en' for english
            - 'es' for spanish
        Keep in mind that regardless of the value, terms will be kept in
        english to comply with the Darwin Core standard.

    Returns
    -------
    DataFrame
        Darwin Core Measurement or Facts dataframe.

    """
    df = pd.merge(deployments, cameras, on=_labels.deployments.camera_id, how="left")

    extension = pd.DataFrame()
    for item in _dwc.measurement.mapping:
        temp = pd.DataFrame()
        temp["eventID"] = df.loc[:, _labels.deployments.deployment_id]
        temp["measurementType"] = item["type"]
        temp["measurementValue"] = df.loc[:, item["value"]]
        temp["measurementUnit"] = item["unit"]
        if item["remarks"]:
            temp["measurementRemarks"] = df.loc[:, item["remarks"]]
        else:
            temp["measurementRemarks"] = np.nan
        extension = pd.concat([extension, temp], ignore_index=True)

    extension = _translate(extension, language)
    extension = extension.dropna(subset=["measurementValue"]).reset_index(drop=True)

    return extension


def create_dwc_multimedia(images: pd.DataFrame, language: str = "en") -> pd.DataFrame:
    """
    Creates a Darwin Core Simple Multimedia dataframe from images
    information. See https://rs.gbif.org/extension/gbif/1.0/multimedia.xml
    for more information about this extension.

    Parameters
    ----------
    images : DataFrame
        Dataframe with the bundle's cameras.
    language : str
        Language of the result's values. Possible values are:

            - 'en' for english
            - 'es' for spanish
        Keep in mind that regardless of the value, terms will be kept in
        english to comply with the Darwin Core standard.

    Returns
    -------
    DataFrame
        Darwin Core Simple Multimedia dataframe.

    """
    extension = images.rename(columns=_dwc.multimedia.mapping)
    extension = extension[
        extension.columns[extension.columns.isin(_dwc.multimedia.order)]
    ]

    for term, value in _dwc.multimedia.constants.items():
        extension[term] = value

    extension["location"] = _gs_to_https(extension["location"])

    extension["title"] = get_lowest_taxon(images, return_rank=False).fillna(
        "Blank or unidentified"
    )

    extension = _translate(extension, language)
    extension = extension.reindex(columns=_dwc.multimedia.order)

    return extension


def create_dwc_occurrence():
    pass


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
