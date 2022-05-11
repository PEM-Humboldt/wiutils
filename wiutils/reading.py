"""
Functions to read information from WI projects.
"""
import pathlib
import shutil
import tempfile
from typing import Union

import pandas as pd

from . import _labels


def load_demo(name) -> tuple:
    """
    Loads images and deployments from a demo dataset.

    Parameters
    ----------
    name : str
        Demo dataset name. Can be one of:

            - 'cajambre'
            - 'cristales'

    Returns
    -------
    DataFrame
        Demo images DataFrame
    DataFrame
        Demo deployments DataFrame

    """
    root = pathlib.Path(__file__).parents[0]
    if name == "cajambre":
        path = root.joinpath("data/cajambre.zip")
    elif name == "cristales":
        path = root.joinpath("data/cristales.zip")
    else:
        raise ValueError("name must be of one ['cajambre']")

    return read_project(path)


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
    DataFrame
        Project images DataFrame
    DataFrame
        Project deployments DataFrame

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

    images = pd.read_csv(path.joinpath("images.csv"), parse_dates=[_labels.images.date])
    deployments = pd.read_csv(
        path.joinpath("deployments.csv"),
        parse_dates=[_labels.deployments.start, _labels.deployments.end],
    )

    if temp_folder:
        shutil.rmtree(temp_folder)

    return images, deployments
