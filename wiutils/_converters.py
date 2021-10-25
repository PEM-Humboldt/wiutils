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
