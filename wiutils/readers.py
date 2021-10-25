"""
Functions to read information from WI projects.
"""
import pathlib
from typing import Union

import pandas as pd


def read_project(folder: Union[str, pathlib.Path]) -> tuple:
    """
    Reads images and deployments tables for a specific Wildlife Insights
    project bundle.

    Parameters
    ----------
    folder : str or Path
        Absolute or relative path of the project bundle.

    Returns
    -------
    tuple
        tuple with the images and the deployments DataFrames.

    """
    if isinstance(folder, str):
        folder = pathlib.Path(folder)

    images = pd.read_csv(folder.joinpath("images.csv"), parse_dates=["timestamp"])
    deployments = pd.read_csv(
        folder.joinpath("deployments.csv"), parse_dates=["start_date", "end_date"]
    )

    return images, deployments
