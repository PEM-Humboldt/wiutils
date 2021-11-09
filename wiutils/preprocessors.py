"""

"""
import pathlib
from typing import Union

import cv2
import ffmpeg
import pandas as pd
from PIL import Image, ExifTags


def _get_exif_code(tag: str) -> int:
    """
    Gets the exif code for a specific tag.

    Parameters
    ----------
    tag : str
        Tag name to get the exif code for.

    Returns
    -------
    int
        Exif code.

    """
    for key, value in ExifTags.TAGS.items():
        if value == tag:
            return key

    raise ValueError(f"{tag} is not a valid Exif tag.")


def convert_video_to_images(
    video_path: Union[str, pathlib.Path],
    output_path: Union[str, pathlib.Path],
    image_format: str = "jpeg",
    offset: int = None
) -> None:
    """
    Converts a video to images with an associated timestamp.

    Parameters
    ----------
    video_path : str or pathlib.Path
        Relative or absolute path of the video to convert.
    output_path : str or pathlib.Path
        Relative or absolute path of the folder to save the images to. If
        the folder does not exist, it will be created.
    image_format : str
        Image format of the output images. Possible values are:

            - 'jpeg'
            - 'png'
    offset : int
        Offset (in seconds) to convert frames to images. For example, if
        offset is 1, the output images will correspond to 1 second-separated
        frames of the video. If offset is None, all the frames in the video
        will be converted to images.

    Returns
    -------
    None

    """
    if not isinstance(video_path, pathlib.Path):
        video_path = pathlib.Path(video_path)
    if not isinstance(output_path, pathlib.Path):
        output_path = pathlib.Path(output_path)

    if image_format not in ("jpeg", "png"):
        raise ValueError("image_format must be one of ['jpeg', 'png'].")

    info = ffmpeg.probe(video_path.as_posix())
    try:
        timestamp = info["format"]["tags"]["creation_time"]
    except KeyError:
        raise Exception(f"{video_path.as_posix()} does not have a creation date.")
    timestamp = pd.Timestamp(timestamp)

    video = cv2.VideoCapture(video_path.as_posix())
    frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    width = len(str(int(frames)))
    datetime_code = _get_exif_code("DateTime")

    output_path.mkdir(parents=True, exist_ok=True)

    flag, arr = video.read()
    count = 1
    while flag:
        image = Image.fromarray(arr)
        exif = Image.Exif()
        exif[datetime_code] = timestamp.strftime("%Y:%m:%d %H:%M:%S")
        name = video_path.stem + "_" + str(count).zfill(width)
        image.save(output_path.joinpath(name), format=image_format)
        if offset:
            video.set(cv2.CAP_PROP_POS_MSEC, count * (offset * 1e3))
        flag, arr = video.read()
        timestamp += pd.Timedelta(milliseconds=video.get(cv2.CAP_PROP_POS_MSEC))
        count += 1
