"""

"""
import pandas as pd

from . import _labels
from .filtering import _remove_wrapper


def compute_date_ranges(
    images: pd.DataFrame = None,
    deployments: pd.DataFrame = None,
    source: str = "both",
    compute_delta: bool = False,
    pivot: bool = False,
    remove_unidentified: bool = False,
    remove_unidentified_kws: dict = None,
    remove_duplicates: bool = False,
    remove_duplicates_kws: dict = None,
    remove_domestic: bool = False,
    remove_domestic_kws: dict = None,
):
    """
    Computes deployment date ranges using information from either images,
    deployments or both.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    deployments : DataFrame
        DataFrame with the project's deployments.
    source : bool
        Source to plot date ranges from: Values can be:

            - 'images' to plot date ranges from images (i.e. first image
            to last image taken).
            - 'deployments' to plot date ranges from deployments
            information (i.e. start date and end date).
            - 'both' to plot both sources in two different subplots.
    compute_delta : bool
        Whether to compute the delta (in days) between the start and end
        dates.
    pivot : bool
        Whether to pivot (reshape from long to wide format) the resulting
        DataFrame.
    remove_unidentified : bool
        Whether to remove unidentified images. Wrapper for the
        wiutils.remove_unidentified function.
    remove_unidentified_kws : dict
        Keyword arguments for the wiutils.remove_unidentified function.
    remove_duplicates : bool
        Whether to remove duplicates. Wrapper for the
        wiutils.remove_duplicates function.
    remove_duplicates_kws : dict
        Keyword arguments for the wiutils.remove_duplicates function.
    remove_domestic : bool
        Whether to remove domestic species. Wrapper for the
        wiutils.remove_domestic function.
    remove_domestic_kws : dict
        Keyword arguments for the wiutils.remove_domestic function.

    Returns
    -------

    """
    df = pd.DataFrame()

    if source == "images" or source == "both":
        if images is None:
            raise ValueError("images DataFrame must be provided.")
        images = images.copy()
        images = _remove_wrapper(
            images,
            remove_unidentified,
            remove_unidentified_kws,
            remove_duplicates,
            remove_duplicates_kws,
            remove_domestic,
            remove_domestic_kws,
        )
        images[_labels.date] = pd.to_datetime(images[_labels.date])
        images[_labels.date] = pd.to_datetime(images[_labels.date].dt.date)
        dates = images.groupby(_labels.site)[_labels.date].agg(
            start_date="min", end_date="max"
        )
        dates["source"] = "images"
        df = pd.concat([df, dates.reset_index()], ignore_index=True)

    if source == "deployments" or source == "both":
        if deployments is None:
            raise ValueError("deployments DataFrame must be provided.")
        deployments = deployments.copy()
        deployments[_labels.start] = pd.to_datetime(deployments[_labels.start])
        deployments[_labels.end] = pd.to_datetime(deployments[_labels.end])
        dates = deployments.loc[:, [_labels.site, _labels.start, _labels.end]]
        dates["source"] = "deployments"
        df = pd.concat([df, dates], ignore_index=True)

    if source not in ("images", "deployments", "both"):
        raise ValueError("source must be one of ['images', 'deployments', 'both']")

    if compute_delta:
        delta = df["end_date"] - df["start_date"]
        df["delta"] = delta.dt.days

    if pivot:
        df = df.pivot(index="deployment_id", columns="source")

    return df
