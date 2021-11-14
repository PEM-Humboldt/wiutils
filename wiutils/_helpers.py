"""
Functions to convert data types.
"""
from typing import Union

import pandas as pd

from . import _labels


def _convert_to_datetime(
    df: pd.DataFrame, columns: Union[list, str, tuple]
) -> pd.DataFrame:
    """
    Converts specific columns of a DataFrame to datetime dtype (if they
    are not datetime already).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to convert columns from.
    columns : list, str or tuple
        Column names to convert to datetime.

    Returns
    -------
    DataFrame
        DataFrame with converted columns.

    """
    if isinstance(columns, str):
        columns = [columns]

    for column in columns:
        if not pd.api.types.is_datetime64_any_dtype(df[column]):
            df[column] = pd.to_datetime(df[column])

    return df


def _get_taxonomy_columns(rank: str) -> list:
    """
    Gets a list of columns for a specific rank along with all the
    inferior taxonomic ranks.

    Parameters
    ----------
    rank : str
        Taxonomic rank.

    Returns
    -------
    list
        List with columns names for the taxonomic ranks.
    """
    if rank == "epithet":
        taxonomy_columns = [_labels.epithet]
    elif rank == "genus":
        taxonomy_columns = [_labels.genus, _labels.epithet]
    elif rank == "family":
        taxonomy_columns = [_labels.family, _labels.genus, _labels.epithet]
    elif rank == "order":
        taxonomy_columns = [
            _labels.order,
            _labels.family,
            _labels.genus,
            _labels.epithet,
        ]
    elif rank == "class":
        taxonomy_columns = [
            _labels.class_,
            _labels.order,
            _labels.family,
            _labels.genus,
            _labels.epithet,
        ]
    else:
        raise ValueError(
            "min_rank must be one of: ['epithet', 'genus', 'family', 'order', 'class']."
        )

    return taxonomy_columns
