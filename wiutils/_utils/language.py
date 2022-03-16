"""
Language utilities.
"""
import pandas as pd

from .. import _nls


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
        words = _nls.es.words
    else:
        raise ValueError("language must be one of ['es'].")

    existing_columns = set(words.keys()) & set(df.columns)
    for column in existing_columns:
        df[column] = df[column].replace(words[column], regex=True)

    return df
