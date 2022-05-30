"""
Test cases for the wiutils.preprocessing.reduce_image_size function.
"""
import PIL.Image

from wiutils.preprocessing import reduce_image_size


def test_dimensions(mocker):
    mocker.patch("PIL.Image.open")
    image = PIL.Image.open()
    mocker.patch.object(image, "height", 60)
    mocker.patch.object(image, "width", 80)
    mocker.patch.object(image, "resize")
    reduce_image_size("image.jpg", "resized.jpg", factor=0.9, method=0)
    image.resize.assert_called_once_with((72, 54), 0)


def test_intact_exif(mocker):
    mocker.patch("PIL.Image.open")
    image = PIL.Image.open()
    mocker.patch.object(image, "format", "JPEG")
    mocker.patch.object(image, "getexif", return_value={306: "2017:04:21 23:11:08"})
    mocker.patch.object(image, "resize")
    result = image.resize()
    mocker.patch.object(image, "save")
    reduce_image_size("image.jpg", "resized.jpg")
    result.save.assert_called_once_with(
        "resized.jpg", format="JPEG", exif={306: "2017:04:21 23:11:08"}
    )
