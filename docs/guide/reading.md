# Reading

## Overview
Downloaded information from Wildlife Insights image projects is divided into four different files:

- **cameras.csv**: metadata about the devices (cameras) used in the project.
- **deployments.csv**: metadata about the placement of a camera, including start date, end date, coordinates and other camera settings.
- **images.csv**: contains data about each individual image, including species identifications and timestamp.
- **projects.csv**: metadata about project methodology and objectives.

Reading functions allow you to conveniently read these files (together at once or independently) as `pandas` dataframes in order to use them as inputs of other `wiutils` functions.

Here is a quick overview of the different reading functions and their description:

| Function                                                           | Description                                                                                                   |
|--------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| [`load_demo`](/reference/#wiutils.reading.load_demo)               | Loads the cameras, deployments, images and projects tables from a demo dataset.                               |
| [`read_bundle`](/reference/#wiutils.reading.read_bundle)           | Reads the cameras, deployments, images and projects tables from a specific Wildlife Insights project bundle.  |
| [`read_cameras`](/reference/#wiutils.reading.read_cameras)         | Reads the cameras' table from a specific Wildlife Insights project bundle.                                    |
| [`read_deployments`](/reference/#wiutils.reading.read_deployments) | Reads the deployments' table from a specific Wildlife Insights project bundle.                                |
| [`read_images`](/reference/#wiutils.reading.read_images)           | Reads the images' table from a specific Wildlife Insights project bundle.                                     |
| [`read_projects`](/reference/#wiutils.reading.read_projects)       | Reads the projects' table from a specific Wildlife Insights project bundle.                                   |

## Reading a bundle
A bundle is a zip file downloaded from Wildlife Insights containing the four different csv files described earlier. `wiutils` offers a convenient function to read these four files as `pandas` dataframes at once: `read_bundle`. You can either read the files directly from the downloaded zip file or from a folder where you extracted the contents.

!!! note

    This function always returns four items (dataframes) in the same order: cameras, deployments, images and projects.

Here is how you can read the files from a bundle:
=== "zip file"
    ```python
    import wiutils

    cameras, deployments, images, projects = wiutils.read_bundle("path/to/bundle.zip")
    ```

=== "folder"
    ```python
    import wiutils

    cameras, deployments, images, projects = wiutils.read_bundle("path/to/folder")
    ```

Notice that the only thing that changes is the path you are passing as the argument to the `read_bundle` function: when reading from a zip file, you need to specify the absolute or relative path to the file (including the .zip extension); when reading from a folder, you need to specify the absolute or relative path of the folder.

!!! note

    If you are using reading the files from the folder you extracted the contents to, make sure there are no nested folders; you have to specify the path to the folder that has the four csv files.

## Reading individual files
You can also read individual files from a bundle as `pandas` dataframes using one of the following functions:

- `read_cameras()`
- `read_deployments()`
- `read_images()`
- `read_projects()`

!!! note

    When reading indiviudal files (and also a bundle), the deployments and images dataframes will automatically have datetime types (instead of strings) for relevant columns (`start_date` and `end_date` for deployments and `timestamp` for images).

Two reasons to do this instead of reading all the files at once might be:

- You don't need to read the four files. For example, you need just to read the deployments.csv file to plot the date ranges. Instead of reading all the files (which can take some time depending on the size of the images.csv file), you just read the deployments.csv file as a dataframe.

- You need to have more control over how the files are read as dataframes. For example, you might want so specify the rows or columns that are going to be read or the data types for each column.

!!! note

    Just like the `read_bundle` function, the four functions to read individual files work on bundle zip files directly or a folder where their contents were extracted to.

For example, if you want to read just the deployments.csv file, you can use the `read_deployments` function:

```python
import wiutils

deployments = wiutils.read_deployments("path/to/bundle.zip")
```

With these functions, you have the possibility to pass any keyword argument accepted by the [`pandas.read_csv`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) function in order to have more control on how the files are read.

For example, you might want to just read the first 25000 rows of the images.csv file to test some functions before reading all the images:

```python
import wiutils

images = wiutils.read_deployments("path/to/folder", nrows=25000)  # Note that nrows is an argument accepted by pandas.read_csv
```

## Loading demo data
If you don't have a bundle file handy or just want to test `wiutils` functions using a smaller dataset, we provide two demo datasets that you can load as dataframes:

- `cajambre`
- `cristales`

Simply pass one of these two names to the `load_demo` function in order to get the four respective dataframes (i.e. cameras, deployments, images and projects):

```python
import wiutils

cameras, deployments, images, projects = wiutils.load_demo("cajambre")
```

We can then inspect one of our dataframes:
```pycon
>>> images
      project_id deployment_id  ... cv_confidence   license
0        2003123   CTCAJ013743  ...           NaN  CC-BY-NC
1        2003123   CTCAJ013743  ...           NaN  CC-BY-NC
2        2003123   CTCAJ013743  ...           NaN  CC-BY-NC
3        2003123   CTCAJ013743  ...           NaN  CC-BY-NC
4        2003123   CTCAJ013743  ...           NaN  CC-BY-NC
          ...           ...  ...           ...       ...
5248     2003123   CTCAJ193741  ...           NaN  CC-BY-NC
5249     2003123   CTCAJ193741  ...           NaN  CC-BY-NC
5250     2003123   CTCAJ193741  ...           NaN  CC-BY-NC
5251     2003123   CTCAJ193741  ...           NaN  CC-BY-NC
5252     2003123   CTCAJ193741  ...           NaN  CC-BY-NC

[5253 rows x 26 columns]

>>> images["timestamp"]
0      2014-12-08 07:46:00
1      2014-11-22 05:58:38
2      2014-12-08 07:46:02
3      2014-11-22 05:58:22
4      2014-10-23 12:31:30
               ...
5248   2014-11-26 05:13:00
5249   2014-11-17 22:09:58
5250   2014-11-23 04:42:34
5251   2014-11-11 21:26:54
5252   2014-11-11 13:26:34
Name: timestamp, Length: 5253, dtype: datetime64[ns]
```
