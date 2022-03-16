"""
Functions for extracting information from WI tables.
"""
import numpy as np
import pandas as pd

from . import _labels


def get_scientific_name(
    images: pd.DataFrame,
    keep_genus: bool = True,
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
    has_genus = ~images[_labels.genus].isin(exclude) & images[_labels.genus].notna()
    has_epithet = (
        ~images[_labels.epithet].isin(exclude) & images[_labels.epithet].notna()
    )

    mask = has_genus & has_epithet
    names.loc[mask] = (
        images.loc[mask, _labels.genus] + " " + images.loc[mask, _labels.epithet]
    )

    if keep_genus:
        mask = has_genus & ~has_epithet
        names.loc[mask] = images.loc[mask, _labels.genus]
        if add_qualifier:
            names.loc[mask] += " sp."

    return names
