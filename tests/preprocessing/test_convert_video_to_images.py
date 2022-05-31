"""
Test cases for the wiutils.preprocessing.convert_video_to_images function.
"""
import cv2
import PIL.Image
import pytest

from wiutils.preprocessing import convert_video_to_images


def patch_image(mocker):
    mocker.patch("PIL.Image.fromarray")
    image = PIL.Image.fromarray()
    mocker.patch.object(image, "getexif", side_effect=[dict(), dict(), dict()])
    mocker.patch.object(image, "save")

    return image


def patch_video(mocker):
    mocker.patch("cv2.VideoCapture")
    mocker.patch("cv2.cvtColor")
    video = cv2.VideoCapture()
    mocker.patch.object(
        video,
        "read",
        side_effect=[
            (True, mocker.MagicMock()),
            (True, mocker.MagicMock()),
            (True, mocker.MagicMock()),
            (False, mocker.MagicMock()),  # Avoid infinite while loop.
        ],
    )
    # The first patch returns the number of frames and the next three
    # return the position in the video (in milliseconds).
    mocker.patch.object(video, "get", side_effect=[180, 0, 1000, 2000])


def test_timestamp(mocker):
    patch_video(mocker)
    image = patch_image(mocker)
    convert_video_to_images(
        "video.mp4", "folder", timestamp="2021-05-31 17:08:42", offset=1
    )
    call_args = image.save.call_args_list
    assert call_args[0][1]["exif"][36867] == "2021:05:31 17:08:42"
    assert call_args[1][1]["exif"][36867] == "2021:05:31 17:08:43"
    assert call_args[2][1]["exif"][36867] == "2021:05:31 17:08:44"


def test_automatic_timestamp(mocker):
    mocker.patch(
        "ffmpeg.probe",
        return_value={"format": {"tags": {"creation_time": "2021-05-31 15:24:01"}}},
    )
    patch_video(mocker)
    image = patch_image(mocker)
    convert_video_to_images("video.mp4", "folder", offset=1)
    call_args = image.save.call_args_list
    assert call_args[0][1]["exif"][36867] == "2021:05:31 15:24:01"
    assert call_args[1][1]["exif"][36867] == "2021:05:31 15:24:02"
    assert call_args[2][1]["exif"][36867] == "2021:05:31 15:24:03"


def test_no_creation_time(mocker):
    with pytest.raises(KeyError):
        mocker.patch("ffmpeg.probe", return_value=dict())
        convert_video_to_images("video.mp4", "folder")


def test_invalid_format():
    with pytest.raises(ValueError):
        convert_video_to_images("video.mp4", "folder", image_format="tif")
