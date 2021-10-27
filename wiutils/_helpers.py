"""
Functions to convert data types.
"""
from typing import Union

import pandas as pd


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


def _get_taxonomy_columns(
    rank: str,
    class_col: str = "class",
    order_col: str = "order",
    family_col: str = "family",
    genus_col: str = "genus",
    epithet_col: str = "species"
):
    """

    Parameters
    ----------
    rank
    class_col
    order_col
    family_col
    genus_col
    epithet_col

    Returns
    -------

    """
    if rank == "epithet":
        taxonomy_columns = [epithet_col]
    elif rank == "genus":
        taxonomy_columns = [genus_col, epithet_col]
    elif rank == "family":
        taxonomy_columns = [family_col, genus_col, epithet_col]
    elif rank == "order":
        taxonomy_columns = [order_col, family_col, genus_col, epithet_col]
    elif rank == "class":
        taxonomy_columns = [class_col, order_col, family_col, genus_col, epithet_col]
    else:
        raise ValueError(
            "min_rank must be one of: ['epithet', 'genus', 'family', 'order', 'class']."
        )

    return taxonomy_columns
