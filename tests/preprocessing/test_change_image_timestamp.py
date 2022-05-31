"""
Test cases for the wiutils.preprocessing.change_image_timestamp function.
"""
import pandas as pd
import PIL.Image

from wiutils.preprocessing import change_image_timestamp


def test_new_timestamp(mocker):
    mocker.patch("PIL.Image.open")
    image = PIL.Image.open("image.jpg")
    mocker.patch.object(image, "save")
    mocker.patch.object(image, "getexif", return_value=dict())
    change_image_timestamp(
        "image.jpg", "new_image.jpg", timestamp="2022-06-03 03:46:51"
    )
    args, kwargs = image.save.call_args
    assert kwargs["exif"][306] == "2022:06:03 03:46:51"  # Exif DateTime
    assert kwargs["exif"][36867] == "2022:06:03 03:46:51"  # Exif DateTimeOriginal


def test_positive_offset(mocker):
    mocker.patch("PIL.Image.open")
    image = PIL.Image.open("image.jpg")
    mocker.patch.object(image, "save")
    mocker.patch.object(image, "getexif", return_value={306: "2021:05:31 17:32:03"})
    change_image_timestamp("image.jpg", "new_image.jpg", offset=pd.DateOffset(days=10))
    args, kwargs = image.save.call_args
    assert kwargs["exif"][306] == "2021:06:10 17:32:03"  # Exif DateTime
    assert kwargs["exif"][36867] == "2021:06:10 17:32:03"  # Exif DateTimeOriginal


def test_negative_delta(mocker):
    mocker.patch("PIL.Image.open")
    image = PIL.Image.open("image.jpg")
    mocker.patch.object(image, "save")
    mocker.patch.object(image, "getexif", return_value={306: "2021:05:31 17:32:03"})
    change_image_timestamp("image.jpg", "new_image.jpg", offset=pd.DateOffset(hours=-5))
    args, kwargs = image.save.call_args
    assert kwargs["exif"][306] == "2021:05:31 12:32:03"  # Exif DateTime
    assert kwargs["exif"][36867] == "2021:05:31 12:32:03"  # Exif DateTimeOriginal
