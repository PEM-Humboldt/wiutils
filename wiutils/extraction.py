"""
Functions for extracting information from WI tables.
"""
from typing import Union

import numpy as np
import pandas as pd

from . import _labels, _utils


def get_lowest_taxon(
    images: pd.DataFrame, return_rank: bool = False
) -> Union[pd.Series, tuple]:
    """
    Gets the lowest identified taxa and ranks.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    return_rank : bool
        Whether to return the lowest identified ranks.

    Returns
    -------
    Series
        Lowest identified taxon for each image.

    Series
        Lowest identified rank for each image.

    """
    ranks = _utils.taxonomy.compute_taxonomic_rank(images)
    taxa = get_scientific_name(images, keep_genus=False, add_qualifier=False)

    mask = (taxa.isna()) & (ranks.notna())
    sorted_columns = np.argsort(images.columns)
    column_indices = np.searchsorted(images.columns[sorted_columns], ranks.loc[mask])
    indices = sorted_columns[column_indices]
    taxa.loc[mask] = images.loc[mask].values[np.arange(mask.sum()), indices]

    if return_rank:
        return taxa, ranks
    else:
        return taxa


def get_scientific_name(
    images: pd.DataFrame,
    keep_genus: bool = False,
    add_qualifier: bool = False,
) -> pd.Series:
    """
    Gets the scientific name of each image by concatenating their
    respective genus and specific epithet.

    Parameters
    ----------
    images : pd.DataFrame
        DataFrame with the project's images.
    keep_genus: bool
        Whether to keep the genus as the scientific name in images where
        only the genus was identified. If False, the scientific name for
        those cases will be emtpy.
    add_qualifier
        Whether to add an open nomenclature qualifier (sp.) to the
        scientific name of those cases where only the genus was
        identified. Only has effect if keep_genus is True.

    Returns
    -------
    Series
        Series with the corresponding scientific names.

    """
    names = pd.Series(np.nan, index=np.arange(len(images)), dtype=str)

    exclude = ["No CV Result", "Unknown"]
    has_genus = (
        ~images[_labels.images.genus].isin(exclude)
        & images[_labels.images.genus].notna()
    )
    has_epithet = (
        ~images[_labels.images.epithet].isin(exclude)
        & images[_labels.images.epithet].notna()
    )

    mask = has_genus & has_epithet
    names.loc[mask] = (
        images.loc[mask, _labels.images.genus]
        + " "
        + images.loc[mask, _labels.images.epithet]
    )

    if keep_genus:
        mask = has_genus & ~has_epithet
        names.loc[mask] = images.loc[mask, _labels.images.genus]
        if add_qualifier:
            names.loc[mask] += " sp."

    return names
