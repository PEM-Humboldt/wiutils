"""
Converts Wildlife Insights information to Darwin Core transformers.
"""
import pandas as pd

from . import mapping
from . import nls
from . import optional
from . import order


def _rearrange(df: pd.DataFrame, order: list) -> pd.DataFrame:
    """
    Rearranges DataFrame columns given a specified order.

    Parameters
    ----------
    df:    DataFrame to rearrange.
    order: Ordered column labels.

    Returns
    -------
    Rearranged DataFrame.
    """
    df = df.copy()

    existing_columns = set(order) & set(df.columns)
    ordered_columns = sorted(existing_columns, key=order.index)

    return df[ordered_columns]


def _translate(df: pd.DataFrame, language: str) -> pd.DataFrame:
    """

    Parameters
    ----------
    df
    language

    Returns
    -------

    """
    df = df.copy()

    if language == "es":
        words = nls.es.words
    else:
        raise ValueError("The only accepted language is 'es'.")

    existing_columns = set(words.keys()) & set(df.columns)
    for column in existing_columns:
        df[column] = df[column].replace(words[column])

    return df


def create_events(
    cameras: pd.DataFrame,
    deployments: pd.DataFrame,
    remove_empty: bool = False,
    translate_to: str = None,
) -> pd.DataFrame:
    """
    Creates an events Darwin Core compliant table from Wildlife Insights
    cameras and deployments information.

    Parameters
    ----------
    cameras:      Wildlife Insights cameras table.
    deployments:  Wildlife Insights deployments table.
    remove_empty: Whether to remove empty optional columns.
    translate_to: Language to translate DataFrame strings to.

    Returns
    -------
    DataFrame with events following the Darwin Core standard.
    """
    cameras = cameras.drop(columns="project_id")
    info = pd.merge(deployments, cameras, on="camera_id", how="inner")
    events = info[mapping.event.keys()].rename(columns=mapping.event)

    start_date = pd.to_datetime(info["start_date"]).dt.strftime("%Y-%m-%d")
    end_date = pd.to_datetime(info["end_date"]).dt.strftime("%Y-%m-%d")
    events["eventDate"] = start_date.str.cat(end_date, sep="/")

    placenames = info["placename"].str.split(", ", expand=True)
    events[["locality", "stateProvince", "county"]] = placenames[[1, 2, 3]]

    # TODO: add specific fields
    # TODO: add measurements

    events = _rearrange(events, order.event)
    if remove_empty:
        events = events.dropna(how="all", axis=1, subset=optional.event)
    if translate_to:
        events = _translate(events, translate_to)

    return events


def create_records(
    images: pd.DataFrame,
    deployments: pd.DataFrame,
    remove_unidentified: bool = False,
    remove_empty: bool = False,
    translate_to: str = None
) -> pd.DataFrame:
    """
    Creates a records Darwin Core compliant table from Wildlife Insights
    images and deployments information.

    Parameters
    ----------
    deployments:         Wildlife Insights deployments table.
    images:              Wildlife Insights cameras table.
    remove_unidentified: Whether to remove unidentified images.
    remove_empty:        Whether to remove empty optional columns.
    translate_to:        Language to translate DataFrame strings to.

    Returns
    -------
    DataFrame with records following the Darwin Core standard.
    """
    images = images.drop(columns="project_id")
    info = pd.merge(images, deployments, on="deployment_id", how="inner")
    subset = ["class", "order", "family", "genus", "species", "common_name"]
    info[subset] = info[subset].replace(["No CV Result", "Unknown"], pd.NA)
    records = info[mapping.record.keys()].rename(columns=mapping.record)

    ranks = ["kingdom", "phylum", "class", "order", "family", "genus"]
    records["taxonRank"] = pd.NA
    records["kingdom"] = pd.NA
    records["phylum"] = pd.NA

    epithets = records["specificEpithet"].str.split(" ", expand=True)
    records["specificEpithet"] = epithets[0]
    species = records["genus"].str.cat(records["specificEpithet"], sep=" ")
    if 1 in epithets.columns:
        records["infraspecificEpithet"] = epithets[1]
        species = species.str.cat(records["infraspecificEpithet"], sep=" ")
        has_subspecies = records["infraspecificEpithet"].notna()
        records.loc[has_subspecies, "taxonRank"] = "subspecies"
    records["scientificName"] = species
    has_species = records["scientificName"].notna()
    records.loc[has_species, "taxonRank"] = "species"
    for rank in ranks:
        has_rank = records[rank].notna()
        mask = (~has_species & has_rank)
        records.loc[mask, "taxonRank"] = rank
        records.loc[mask, "taxonRank"] = records.loc[mask, rank]

    # TODO: add specific fields
    records["recordedBy"] = records["identifiedBy"]
    records["eventDate"] = pd.to_datetime(info["timestamp"]).dt.strftime("%Y-%m-%d")
    records["eventTime"] = pd.to_datetime(info["timestamp"]).dt.strftime("%H:%M:%S")

    # TODO: add measurements

    records = _rearrange(records, order.record)
    if remove_unidentified:
        records = records.dropna(subset="taxonRank")
    if remove_empty:
        records = records.dropna(how="all", axis=1, subset=optional.record)
    if translate_to:
        records = _translate(records, translate_to)

    return records
