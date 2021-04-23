"""
Converts Wildlife Insights information to Darwin Core tables.
"""
import pandas as pd

from . import mapping
from . import order


def create_events(
    cameras: pd.DataFrame,
    deployments: pd.DataFrame,
    rearrange: bool = True
) -> pd.DataFrame:
    """
    Creates an events Darwin Core compliant table from Wildlife Insights
    cameras and deployments information.

    Parameters
    ----------
    cameras:     Wildlife Insights cameras table.
    deployments: Wildlife Insights deployments table.
    rearrange:   Whether to arrange columns using the corresponding
                 Darwin Core order.

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
    # TODO: add translation

    if rearrange:
        columns = set(order.event) & set(events.columns)
        events = events[sorted(columns, key=order.event.index)]

    return events


def create_records(
    images: pd.DataFrame,
    deployments: pd.DataFrame,
    rearrange: bool = True
) -> pd.DataFrame:
    """
    Creates a records Darwin Core compliant table from Wildlife Insights
    images and deployments information.

    Parameters
    ----------
    images:      Wildlife Insights cameras table.
    deployments: Wildlife Insights deployments table.
    rearrange:   Whether to arrange columns using the corresponding
                 Darwin Core order.

    Returns
    -------
    DataFrame with records following the Darwin Core standard.
    """
    images = images.drop(columns="project_id")
    info = pd.merge(images, deployments, on="camera_id", how="inner")
    records = info[mapping.record.keys()].rename(columns=mapping.record)

    # TODO: add specific fields
    # TODO: add measurements
    # TODO: add translation

    if rearrange:
        columns = set(order.event) & set(records.columns)
        records = records[sorted(columns, key=order.event.index)]

    return records
