"""
Functions to read information from WI projects.
"""
import pathlib
import shutil
import tempfile
from typing import Union

import pandas as pd


def read_project(path: Union[str, pathlib.Path]) -> tuple:
    """
    Reads images and deployments tables for a specific Wildlife Insights
    project bundle.

    Parameters
    ----------
    path : str or Path
        Absolute or relative path of the project bundle. Can be a folder
        with all the respective csv files inside or a zip file.

    Returns
    -------
    tuple
        tuple with the images and the deployments DataFrames.

    """
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)

    temp_folder = None
    if path.is_file():
        if not path.suffix == ".zip":
            raise ValueError("path must be either a folder or a .zip file.")
        temp_folder = tempfile.mkdtemp()
        shutil.unpack_archive(path, temp_folder)
        path = pathlib.Path(temp_folder).joinpath(path.stem)

    images = pd.read_csv(path.joinpath("images.csv"), parse_dates=["timestamp"])
    deployments = pd.read_csv(
        path.joinpath("deployments.csv"), parse_dates=["start_date", "end_date"]
    )

    if temp_folder:
        shutil.rmtree(temp_folder)

    return images, deployments
