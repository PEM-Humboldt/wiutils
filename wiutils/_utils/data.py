"""
Data utilities
"""
from typing import Union

import pandas as pd


def rearrange(df: pd.DataFrame, order: Union[list, tuple]) -> pd.DataFrame:
    """
    Rearranges DataFrame columns given a specific order.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to rearrange.
    order : list or tuple
        Ordered column labels.

    Returns
    -------
    DataFrame
        Rearranged DataFrame.

    """
    existing_columns = set(order) & set(df.columns)
    ordered_columns = sorted(existing_columns, key=order.index)

    return df[ordered_columns]
