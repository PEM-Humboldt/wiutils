# Getting started

`wiutils` has several utilities for exploring and manipulating (filtering, plotting and summarizing) information from [Wildlife Insights (WI)](https://www.wildlifeinsights.org/) projects. These functions are useful to compute basic statistics, prepare the information for further analysis (*e.g.* occupancy models) and translate it into other standards (*i.e.* Darwin Core) that facilitate its publication on biodiversity information centers (*e.g.* GBIF).

## Installation
Currently, `wiutils` works with Python versions 3.6 through 3.10.

### Stable
You can install the latest stable version of `wiutils` using either [`pip`](https://pip.pypa.io) or [`conda`](https://docs.conda.io) (recommended). In either case, we recommend creating a virtual environment for the installation.

=== "pip"
    ```shell
    pip install wiutils
    ```

=== "conda"
    ```shell
    conda install -c conda-forge wiutils
    ```

!!! note

    If you are using `conda`, the installation is only available through the [`conda-forge`](https://conda-forge.org/) channel.

### From source
If you prefer to install `wiutils` from source, you'll need to install it from the GitHub repository. This can be done with `pip` or a combination of `pip` and `git`.

=== "pip"
    ```shell
    pip install --upgrade https://github.com/PEM-Humboldt/wiutils/tarball/master
    ```

=== "pip + git"
    ```shell
    pip install git+https://github.com/PEM-Humboldt/wiutils.git#egg=wiutils
    ```

## Overview
`wiutils` has a wide range of functions to explore and manipulate information from WI projects. To get started and use most of these functions, you'll need to download your projects to your machine. Data from WI has a specific standard and depending on the type of project (*i.e.* images or sequences), every download will be divided into four of the following five files: `projects.csv`, `cameras.csv`, `deployments.csv`, `images.csv`, `sequences.csv`.

!!! warning

    Except for functions that take only deployment information as an input, `wiutils` does not support sequence projects yet.

Functions in `wiutils` can be grouped in seven different categories:

1. **Reading**: functions to read information from WI projects into DataFrames.
2. **Filtering**: functions to filter WI images based on different conditions.
3. **Extraction**: functions for extracting information based on different WI image's columns.
4. **Summarizing**: functions to summarize (*i.e.* create new tables) WI data.
5. **Plotting**: functions to plot information from the images and deployments tables.
6. **Darwin Core**: functions to translate WI data to the Darwin Core standard.
7. **Preprocessing**: functions to preprocess videos and images before uploading them to WI.

!!! note

    Preprocessing functions are the only functions that do not need WI data as an input; rather they work on images and videos to preprocess data before uploading it to Wildlife Insights.

### Reading
| Function                                                  | Description                                                                          |
|-----------------------------------------------------------|--------------------------------------------------------------------------------------|
| [`read_project`](reference/reading/#wiutils.read_project) | Reads images and deployments tables for a specific Wildlife Insights project bundle. |

### Filtering
| Function                                                                              | Description                                                                                          |
|---------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| [`remove_domestic`](reference/filtering/#wiutils.remove_domestic)                     | Removes images where the identification corresponds to a domestic species.                           |
| [`remove_duplicates`](reference/filtering/#wiutils.remove_duplicates)                 | Removes duplicate records (images) from the same taxon in the same deployment given a time interval. |
| [`remove_inconsistent_dates`](reference/filtering/#wiutils.remove_inconsistent_dates) | Removes images where the timestamp is outside the date range of the corresponding deployment.        |
| [`remove unidentified`](reference/filtering/#wiutils.remove_unidentified)             | Removes unidentified (up to a specific taxonomic rank) images.                                       |

### Extraction
| Function                                                                   | Description                                                                                          |
|----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| [`get_lowest_taxon`](reference/extraction/#wiutils.get_lowest_taxon)       | Gets the lowest identified taxa and ranks.                                                           |
| [`get_scientific_name`](reference/extraction/#wiutils.get_scientific_name) | Gets the scientific name of each image by concatenating their respective genus and specific epithet. |

### Summarizing
| Function                                                                                | Description                                                                                                                                          |
|-----------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`compute_count_summary`](reference/summarizing/#wiutils.compute_count_summary)         | Computes a summary of images, records and taxa count by deployment                                                                                   |
| [`compute_date_ranges`](reference/summarizing/#wiutils.compute_date_ranges)             | Computes deployment date ranges using information from either images, deployments or both                                                            |
| [`compute_detection`](reference/summarizing/#wiutils.compute_detection)                 | Computes the detection (in terms of abundance or presence)of each taxon by deployment.                                                               |
| [`compute_detection_history`](reference/summarizing/#wiutils.compute_detection_history) | Computes the detection history (in terms of abundance or presence) by taxon and deployment, grouping observations into specific days-long intervals. |
| [`compute_general_count`](reference/summarizing/#wiutils.compute_general_count)         | Computes the general abundance and number of deployments for each taxon.                                                                             |
| [`compute_hill_numbers`](reference/summarizing/#wiutils.compute_hill_numbers)           | Computes the Hill numbers of order q (also called effective number of species) by site for some given values of q.                                   |

### Plotting
| Function                                                                       | Description                                                                                         |
|--------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| [`plot_activity_hours`](reference/plotting/#wiutils.plot_activity_hours)       | Plots the activity hours of one or multiple taxa by grouping all observations into a 24-hour range. |
| [`plot_date_ranges`](reference/plotting/#wiutils.plot_date_ranges)             | Plots deployment date ranges.                                                                       |
| [`plot_detection_history`](reference/plotting/#wiutils.plot_detection_history) | Plots detection history matrix for a given species.                                                 |

### Darwin Core


### Preprocessing
| Function                                                                              | Changes an image's associated timestamp metadata for a new timestamp.                               |
|---------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| [`change_image_timestamp`](reference/preprocessing/#wiutils.change_image_timestamp)   | Plots the activity hours of one or multiple taxa by grouping all observations into a 24-hour range. |
| [`convert_video_to_images`](reference/preprocessing/#wiutils.convert_video_to_images) | Converts a video to images with an associated timestamp.                                            |
| [`reduce_image_size`](reference/preprocessing/#wiutils.reduce_image_size)             | Reduces image file size by resampling using a given factor.                                         |

## Wildlife Insights
Wildlife Insights is *a cloud-based platform that uses machine learning to identify animals in camera trap images*. Apart from helping with image classification, Wildlife Insights allows to store and manage camera trap data and metadata. It also offers the possibility to download this data in a convenient format for further analysis and sharing. To learn more about Wildlife Insights go to <https://www.wildlifeinsights.org/get-started>.


