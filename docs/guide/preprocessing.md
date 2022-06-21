# Preprocessing

## Overview
Unlike all other functions in `wiutils`, preprocessing functions are meant to be used before uploading data to Wildlife Insights rather than after downloading processed information (*i.e.* the different tables).

Here is a quick overview of the different Darwin Core functions and their description:

| Function                                                                               | Changes an image's associated timestamp metadata for a new timestamp.                               |
|----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| [`change_image_timestamp`](/reference/#wiutils.preprocessing.change_image_timestamp)   | Plots the activity hours of one or multiple taxa by grouping all observations into a 24-hour range. |
| [`convert_video_to_images`](/reference/#wiutils.preprocessing.convert_video_to_images) | Converts a video to images with an associated timestamp.                                            |
| [`reduce_image_size`](/reference/#wiutils.preprocessing.reduce_image_size)             | Reduces image file size by resampling using a given factor.                                         |

## Changing an image's timestamp
Trail cameras record the date and time when taking a picture. This information is stored as metadata that Wildlife Insights automatically reads when you upload images to the platform. If the camera was misconfigured, it is possible that timestamps are wrong and thus, the resulting tables from Wildlife Insights will be biased. The `change_image_timestamp` function creates a copy of an image modifying its datetime metadata (using [Exif tags](https://exiftool.org/TagNames/EXIF.html)).

You must pass the path of the original image, the path of the modified image that will be created and an arbitrary timestamp to overwrite the original one. Here is an example:
```pycon
>>> wiutils.change_image_timestamp("path/to/input.jpg", "path/to/output.jpg", timestamp="2017-04-21 21:53:12")
```

The function does not return anything; it rather saves the output image at the specified location.

The timestamp parameter can be either a string (must be parseable by `pandas`), a [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects) object or a [`pandas.Timestamp`](https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.html) object.

A common case is that the date and time was not setup correctly in the camera before deploying it and all the images have now a shifted timestamp. You probably don't want to give an arbitrary timestamp to each image in this case but rather use an offset. For example, imagine that you know you need to add five days to all the images' timestamp for a particular deployment. You can loop through those images and use the `offset` parameter like this:
```pycon
>>> import pandas as pd
>>> wiutils.change_image_timestamp("path/to/input.jpg", "path/to/output.jpg", offset=pd.DateOffset(days=5))
```

Take a look at the [`pd.Offset`](https://pandas.pydata.org/docs/reference/api/pandas.tseries.offsets.DateOffset.html) documentation for a list of all possible temporal parameter (*e.g.* `hours`, `days` or `weeks`) that you can pass. Note that it is also possible that instead of adding an arbitrary unit of time to the timestamp you might rather want to subtract from it. In this case, just pass a negative value. For example, if you wanted to subtract eight hours from the original timestamp:
```pycon
>>> import pandas as pd
>>> wiutils.change_image_timestamp("path/to/input.jpg", "path/to/output.jpg", offset=pd.DateOffset(hours=-8))
```

## Converting a video to multiple images
Some trail cameras are able to record videos when activated. However, Wildlife Insights does not process videos, so you won't be able to upload them to the platform. There are many reasons you might end up having videos that you still want to use for your Wildlife Insights projects. The `convert_video_to_images` function converts a video to multiple images (with the corresponding datetime metadata) so you can upload them to Wildlife Insights. This function takes the path of the input video to convert and the path of a folder to save the extracted images to. For example:
```pycon
>>> wiutils.convert_video_to_images("path/to/video.mp4", "path/to/folder")
```

By default, it will save and image for each frame of the video. This might be a lot of images depending on the length of the video. The `offset` parameter lets you specify an offset (in seconds) between frames (it always includes the first frame). For example, if you wanted to save an image for every three seconds of the video:
```pycon
>>> wiutils.convert_video_to_images("path/to/video.mp4", "path/to/folder", offset=3)
```

As mentioned above, the saved  images will have a timestamp that is computed automatically from the timestamp of the video and the location of the frame in the duration of the video. However, depending on the make of the trail camera, it is possible that the video does not have an associated timestamp (usually happens with the AVI videos). In this case, you'll need to explicitly pass a timestamp of the beginning of the video (usually displayed at the bottom of the video):
```pycon
>>> wiutils.convert_video_to_images("path/to/video.avi", "path/to/folder", timestamp="2017-04-21 21:53:12")
```

The timestamp parameter can be either a string (must be parseable by `pandas`), a [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects) object or a [`pandas.Timestamp`](https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.html) object.

By default, all the generated images will be saved using the JPG format. If for some reason you want to change this, specify another format using the `image_format` parameter:
```pycon
>>> wiutils.convert_video_to_images("path/to/video.mp4", "path/to/folder", image_format="png")
```

## Reducing an image's size
Depending on the make and configuration of the camera, it might capture high resolution images whose size is relatively big. Wildlife Insights has a size limit for each image, so you won't be able to upload images that are too big. The `reduce_image_size` function lets you downscale and image using an arbitrary resampling factor in order to reduce its size. The function takes the path of the original image, the path of the modified image that will be created and the resampling factor (which is a value between 0 and 1). Here is an example:
```pycon
>>> wiutils.reduce_image_size("path/to/input.jpg", "path/to/output.jpg", factor=0.9)
```

By default, the resample is done using a lanczos filter. There are [different available filters,](https://pillow.readthedocs.io/en/stable/reference/Image.html#resampling-filters) and you can find a description of them at: <https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-filters>

For example, if instead of using a lanczos filter you wanted to use a faster (but with a lower downsampling quality) filter, you can use the nearest algorithm by passing an integer to the `method` parameter:
```pycon
>>> wiutils.reduce_image_size("path/to/input.jpg", "path/to/output.jpg", method=0)
```
