# Filtering

## Overview
Filtering functions allow you to remove specific images from a Wildlife Insights dataset. These functions are useful to explore the images but also to filter them before using other functions, specially the summarizing ones.

Here is a quick overview of the different filtering functions and their description:

| Function                                                                               | Description                                                                                          |
|----------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| [`remove_domestic`](/reference/#wiutils.filtering.remove_domestic)                     | Removes images where the identification corresponds to a domestic species.                           |
| [`remove_duplicates`](/reference/#wiutils.filtering.remove_duplicates)                 | Removes duplicate records (images) from the same taxon in the same deployment given a time interval. |
| [`remove_inconsistent_dates`](/reference/#wiutils.filtering.remove_inconsistent_dates) | Removes images where the timestamp is outside the date range of the corresponding deployment.        |
| [`remove unidentified`](/reference/#wiutils.filtering.remove_unidentified)             | Removes unidentified (up to a specific taxonomic rank) images.                                       |

!!! note

    All the filtering functions have a `reset_index` parameter that is `False` by default. If you want to have a new consecutive index from 0 to n - 1 (n being the number of rows in the dataframe) instead of keeping the original index after filtering the images, pass `reset_index=True`.

For every snippet of code showed here, we will assume you have already run the following code:

```python
import wiutils

cameras, deployments, images, projects = wiutils.load_demo("cajambre")
```

## Removing unidentified images
Camera traps are usually deployed to record animals in the wild. However, sometimes they might be activated by a moving leaf or branch and register images without any wildlife. Furthermore, there might be some cases where neither of the Wildlife Insights computer vision algorithm and the researcher were able to identify an animal on a given image.

If we check the images dataframe, we will see that it has 5253 rows (*i.e.* images):
```pycon
>>> len(images)
5253
```

However, not all of these images have an identification:
```pycon
>>> images["class"].isna().sum()
917
>>> images["genus"].isna().sum()
1881
```
Of all the images, 917 did not have any identification at all and 1881 were not identified down to at least the genus level.

We can use the `remove_unidentified` function to remove images without an identification down to a specific level. For example, we can remove all the images that did not have any identification at all:
```pycon
>>> subset = wiutils.remove_unidentified(images, rank="class")
>>> len(subset)
4336
```

Likewise, we can remove all the images that were not identified down to the genus level:
```pycon
>>> subset = wiutils.remove_unidentified(images, rank="genus")
>>> len(subset)
3372
```

The `rank` parameter accepts any of the following values:

- `"species"`
- `"genus"`
- `"family"`
- `"order"`
- `"class"`

More specific ranks will likely have more images removed. For example, for `rank="order"` only images without an identification for order (and therefore all the lower ranks -family, genus and species-) will be removed. However, for `rank="species"`, all the images that were not identified down to the species level (*i.e.* do not have an epithet) will be removed.

To better illustrate this, let's take a subset of the images dataframe:
```pycon
>>> subset = images.loc[[1, 5, 639, 788]]
>>> columns = ["class", "order", "family", "genus", "species"]  # We will use this later.
>>> subset[columns]

        class             order       family      genus species
1        Aves  Struthioniformes    Tinamidae    Tinamus   major
5         NaN               NaN          NaN        NaN     NaN
639      Aves     Columbiformes   Columbidae  Leptotila     NaN
788  Mammalia   Didelphimorphia  Didelphidae        NaN     NaN
```

And now, let's remove unidentified images using different values for the `rank` parameter:

```pycon
>>> wiutils.remove_unidentified(subset, rank="class")[columns]

        class             order       family      genus species
1        Aves  Struthioniformes    Tinamidae    Tinamus   major
639      Aves     Columbiformes   Columbidae  Leptotila     NaN
788  Mammalia   Didelphimorphia  Didelphidae        NaN     NaN

>>> wiutils.remove_unidentified(subset, rank="genus")[columns]

    class             order      family      genus species
1    Aves  Struthioniformes   Tinamidae    Tinamus   major
639  Aves     Columbiformes  Columbidae  Leptotila     NaN

>>> wiutils.remove_unidentified(subset, rank="species")[columns]

  class             order     family    genus species
1  Aves  Struthioniformes  Tinamidae  Tinamus   major
```
As you can see, when we pass `rank="class"` only one image is removed but when we pass `rank="species"` three images are removed.

## Removing duplicate images
There are at least two different cases where you might consider a set of images as duplicates:

- Your camera is configured to take multiple shots when activated, resulting in multiple images of the same individual when an animal activated it.
- The camera captured an animal that returned after a certain time (could be seconds, minutes or even days) and activated the camera again, resulting in multiple images of the same individual.

The `remove_duplicates` function allows you to specify an arbitrary time window for which images in the same deployment with the same identification (*i.e.* **lowest identified taxon**) will be removed (except for the first record).

Let's create a subset (with only one deployment and one taxon) of the images dataframe to illustrate the two cases described above:
```pycon hl_lines="7 10 13 16"
>>> subset = images[(images["deployment_id"] == "CTCAJ093776") & (images["genus"] == "Leptotila")]
>>> subset = subset.sort_values("timestamp")
>>> columns = ["deployment_id", "genus", "species", "timestamp"]  # We will use this later.
>>> subset[columns]

     deployment_id      genus species           timestamp
4170   CTCAJ093776  Leptotila     NaN 2014-11-06 07:20:10
1229   CTCAJ093776  Leptotila     NaN 2014-11-06 07:20:12
1405   CTCAJ093776  Leptotila     NaN 2014-11-06 07:20:12
1431   CTCAJ093776  Leptotila     NaN 2014-11-11 08:49:02
4136   CTCAJ093776  Leptotila     NaN 2014-11-11 08:49:02
1196   CTCAJ093776  Leptotila     NaN 2014-11-11 08:49:04
3740   CTCAJ093776  Leptotila     NaN 2014-11-15 09:27:46
3846   CTCAJ093776  Leptotila     NaN 2014-11-15 09:27:48
4185   CTCAJ093776  Leptotila     NaN 2014-11-15 09:27:48
3894   CTCAJ093776  Leptotila     NaN 2014-11-18 10:02:16
1404   CTCAJ093776  Leptotila     NaN 2014-11-18 10:02:18
1443   CTCAJ093776  Leptotila     NaN 2014-11-18 10:02:18
```

Notice how some images are just a few seconds apart from each other; it is evident that there are four groups of images. Instead of overestimating the records of *Leptotila*, we might assume that each group of images corresponds to one individual and that there are four different individuals of that genus in total (see the highlighted rows). Because within each group the images are just two seconds apart from each other, we can use an arbitrary time window of five seconds to remove duplicate images:
```pycon
>>> result = wiutils.remove_duplicates(subset, interval=5, unit="seconds")
>>> result[columns]

     deployment_id      genus species           timestamp
4170   CTCAJ093776  Leptotila     NaN 2014-11-06 07:20:10
1431   CTCAJ093776  Leptotila     NaN 2014-11-11 08:49:02
3740   CTCAJ093776  Leptotila     NaN 2014-11-15 09:27:46
3894   CTCAJ093776  Leptotila     NaN 2014-11-18 10:02:16
```

Now there are only four images for that genus.

For the second case, we might assume that images within a four-day interval correspond to the same individual. Thus, we are going to remove those images using an arbitrary window of four days.
```pycon
>>> result = wiutils.remove_duplicates(subset, interval=4, unit="days")
>>> result[columns]

     deployment_id      genus species           timestamp
4170   CTCAJ093776  Leptotila     NaN 2014-11-06 07:20:10
1431   CTCAJ093776  Leptotila     NaN 2014-11-11 08:49:02
3740   CTCAJ093776  Leptotila     NaN 2014-11-15 09:27:46
```

Now there are only three images because the third and fourth group are considered as one individual.

!!! note

    The `remove_duplicates` function recognizes  duplicates of the same taxon, regardless of the taxonomic rank. For example, if you have one deployment with images that were identified down to the *Leptotila* genus and images that were identified as *Leptotila verreauxi*, duplicates will be recognized independently for each taxon, regardless of the time window used.

By default, the `remove_duplicates` function uses a five-minute interval but depending on your project, you might want to use a different time window. The `interval` parameter accepts any positive integer and the `unit` parameter has to be one of:

- `"weeks"`
- `"days"`
- `"hours"`
- `"minutes"`
- `"seconds"`

## Removing images with domestic species
Depending on where the camera traps were deployed, it is not uncommon to register domestic species (*e.g.* dogs, cats or pigs). For different analysis, such as computing diversity indices, you might want to ignore these species. The `remove_domestic` function does this by removing images from the following species (or subspecies):

- **Cat**: *Felis catus*
- **Cattle**: *Bos bubalis*, *Bos taurus*, *Bubalus bubalis*
- **Chicken**: *Gallus domesticus*, *Gallus gallus domesticus*
- **Dog**: *Canis familiaris*, *Canis familiaris domesticus*, *Canis lupus familiaris*
- **Donkey**: *Equus asinus*
- **Duck**: *Anas platyrhynchos*, *Anas platyrhynchos domesticus*
- **Goat**: *Capra hircus*
- **Goose**: *Anser anser*, *Anser cygnoides*
- **Guinea fowl**: *Numida meleagris*, *Phasianus meleagris*
- **Horse**: *Equus caballus*, *Equus ferus caballus*
- **Human**: *Homo sapiens*
- **Muscovy duck**: *Cairina moschata domestica*
- **Pig**: *Sus domesticus*, *Sus scrofa domesticus*
- **Sheep**: *Ovis aries*
- **Turkey**: *Meleagris gallopavo*

!!! note

    This is not a comprehensive list of domestic species and it might be improved. Feel free to create a pull request if you want to add more species to the [list](https://github.com/PEM-Humboldt/wiutils/blob/master/wiutils/_domestic.py).

Using the images dataframe, we can remove domestic species as follows:
```pycon
>>> subset = wiutils.remove_domestic(images)
>>> len(subset)
4772
>>> len(images) - len(subset)
481
```

We can see that there were 481 images with identified domestic species.

It is possible that in some cases domestic species were identified down just to the genus but not the species level. By default, the `remove_domestic` function extracts the scientific names from the images and compares it to the list of domestic species. However, it offers a broader strategy that uses just the genera from both the images and the list of domestic species. To use this strategy, use the `broad` parameter:
```python
wiutils.remove_domestic(images, broad=True)
```

!!! warning

    When passing `broad=True` to the `remove_domestic` function, there are some special cases where non-domestic species might be deleted. For example, if you have images from both dogs and wolfs (genus *Canis*), their records will be removed when using a broader strategy.

## Removing images with inconsistent dates
As shown in the [extraction](/guide/extraction#getting-date-ranges) section, there might be cases where image dates do not coincide with their corresponding deployment dates. Usually because of camera misconfiguration, this can lead to images having dates that are outside the deployment range. In certain scenarios where associated dates are essential (*e.g.* computing detection histories), it is probably a good idea to remove those images. The `remove_inconsistent_dates` removes all the images whose date is outside the corresponding deployment range.

!!! warning

    The `remove_inconsistent_dates` assumes that deployment date ranges coming from Wildlife Insights are correct. Wrong dates could lead to the removal of consistent images.

The `cajambre` demo dataset does not have any inconsistent images, so we will have to modify some images' dates to show how this function work. Let's take the first deployment (`CTCAJ013743`) as an example, using the `get_date_ranges` function:
```pycon
>>> date_ranges = wiutils.get_date_ranges(images, deployments, source="both", pivot=True)
>>> date_ranges.loc["CTCAJ013743"]

            source
start_date  deployments   2014-10-22
            images        2014-10-22
end_date    deployments   2014-12-08
            images        2014-12-08
Name: CTCAJ013743, dtype: datetime64[ns]
```

This particular deployment was working from 2014-10-22 to 2014-12-08 and its first and last image coincide with those dates. Let's subtract a few days from the dates of all the images of that deployment so some fall outside the range:
```pycon
>>> import pandas as pd
>>> images.loc[images["deployment_id"] == "CTCAJ013743", "timestamp"]

0      2014-12-07 07:46:00
1      2014-11-21 05:58:38
2      2014-12-07 07:46:02
3      2014-11-21 05:58:22
4      2014-10-22 12:31:30
               ...
2857   2014-10-23 06:09:42
2858   2014-10-21 12:09:38
2859   2014-10-22 10:15:42
2860   2014-10-22 09:53:50
2861   2014-10-22 10:53:52
Name: timestamp, Length: 501, dtype: datetime64[ns]

>>> images_copy = images.copy()  # Copy the dataframe before modifying it.
>>> images_copy.loc[images_copy["deployment_id"] == "CTCAJ013743", "timestamp"] -= pd.DateOffset(days=20)
>>> images_copy.loc[images_copy["deployment_id"] == "CTCAJ013743", "timestamp"]

0      2014-11-18 07:46:00
1      2014-11-02 05:58:38
2      2014-11-18 07:46:02
3      2014-11-02 05:58:22
4      2014-10-03 12:31:30
               ...
2857   2014-10-04 06:09:42
2858   2014-10-02 12:09:38
2859   2014-10-03 10:15:42
2860   2014-10-03 09:53:50
2861   2014-10-03 10:53:52
Name: timestamp, Length: 501, dtype: datetime64[ns]
```

Now, let's check the date ranges again:
```pycon
>>> date_ranges = wiutils.get_date_ranges(images_copy, deployments, source="both", pivot=True)
>>> date_ranges.loc["CTCAJ013743"]

            source
start_date  deployments   2014-10-22
            images        2014-10-02
end_date    deployments   2014-12-08
            images        2014-11-18
Name: CTCAJ013743, dtype: datetime64[ns]
```

There is a 20-day difference between deployments and images ranges. We can now use the `remove_inconsistent_dates` function:

```pycon
>>> subset = wiutils.remove_inconsistent_dates(images_copy, deployments)
>>> len(images_copy) - len(subset)
390
```

There were 390 inconsistent images in our modified images dataframe.
