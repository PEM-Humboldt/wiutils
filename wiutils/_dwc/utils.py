"""
Helper functions used when creating DwC tables.
"""
from collections import OrderedDict
from typing import Union

import numpy as np
import pandas as pd

from . import nls


def compute_taxonomic_rank(df: pd.DataFrame) -> pd.Series:
    """
    Computes the taxonomic rank of the most specific identification for
    each image.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with records.

    Returns
    -------
    pd.Series
        Series with the corresponding taxonomic ranks.

    """
    rank_map = OrderedDict(
        {
            "kingdom": "kingdom",
            "phylum": "phylum",
            "class": "class",
            "order": "order",
            "family": "family",
            "genus": "genus",
            "species": "specificEpithet",
            "subspecies": "infraspecificEpithet",
        }
    )

    ranks = pd.Series(np.nan, index=df.index)

    for rank, column in reversed(rank_map.items()):
        if column in df:
            has_rank = ranks.notna()
            has_identification = df[column].notna()
            ranks.loc[(~has_rank & has_identification)] = rank

    return ranks


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


def translate(df: pd.DataFrame, language: str) -> pd.DataFrame:
    """
    Replaces values in a DataFrame for their translation in a specific
    language taking a predefined dictionary.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to translate values in.
    language : str
        Language to translate values. Possible values are:

            - 'es'

    Returns
    -------
    DataFrame
        DataFrame with translated values.

    """
    df = df.copy()

    if language == "es":
        words = nls.es.words
    else:
        raise ValueError("language must be one of ['es'].")

    existing_columns = set(words.keys()) & set(df.columns)
    for column in existing_columns:
        df[column] = df[column].replace(words[column], regex=True)

    return df
