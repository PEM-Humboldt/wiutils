"""
Taxonomy utilities.
"""
from collections import OrderedDict

import numpy as np
import pandas as pd

from .. import _labels


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


def get_taxonomy_columns(rank: str) -> list:
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
        taxonomy_columns = [_labels.images.epithet]
    elif rank == "genus":
        taxonomy_columns = [_labels.images.genus, _labels.images.epithet]
    elif rank == "family":
        taxonomy_columns = [
            _labels.images.family,
            _labels.images.genus,
            _labels.images.epithet,
        ]
    elif rank == "order":
        taxonomy_columns = [
            _labels.images.order,
            _labels.images.family,
            _labels.images.genus,
            _labels.images.epithet,
        ]
    elif rank == "class":
        taxonomy_columns = [
            _labels.images.class_,
            _labels.images.order,
            _labels.images.family,
            _labels.images.genus,
            _labels.images.epithet,
        ]
    else:
        raise ValueError(
            "min_rank must be one of: ['epithet', 'genus', 'family', 'order', 'class']."
        )

    return taxonomy_columns
