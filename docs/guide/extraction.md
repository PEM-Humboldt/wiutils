# Extraction

## Overview
Extraction functions allow you to extract different information from a Wildlife Insights project's images and deployments.

Here is a quick overview of the different extraction functions and their description:

| Function                                                                    | Description                                                                                          |
|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| [`get_date_ranges`](/reference/#wiutils.extraction.get_date_ranges)         | Gets deployment date ranges using information from either images, deployments or both.               |
| [`get_lowest_taxon`](/reference/#wiutils.extraction.get_lowest_taxon)       | Gets the lowest identified taxa and ranks.                                                           |
| [`get_scientific_name`](/reference/#wiutils.extraction.get_scientific_name) | Gets the scientific name of each image by concatenating their respective genus and specific epithet. |


For every snippet of code showed here, we will assume you have already ran the following code:

```python
import wiutils

cameras, deployments, images, projects = wiutils.load_demo("cajambre")
```

## Getting date ranges
We refer to date ranges as the range that a deployment was operating over time. This range can be the period between the installation and the removal of the camera in the deployment but can also be interpreted as the range between the first and last picture the camera took while it was deployed. Usually, these two date ranges should coincide but there are several reasons they might just partially overlap or that one might be shorter than the other. For example, a camera might have been deployed for a month, but after 15 days its battery died and stopped taking pictures. Another example might be that a camera was misconfigured when deployed and the timestamp of the pictures are delayed by a certain amount of days.

The `get_date_ranges` function offers a convenient way of getting (or computing in the case of images) these date ranges.

Here are some examples of extracting these date ranges from the deployments, the images and both:

=== "deployments"
    ```pycon hl_lines="17"
    >>> wiutils.get_date_ranges(deployments=deployments, source="deployments")

       deployment_id start_date   end_date       source
    0    CTCAJ013743 2014-10-22 2014-12-08  deployments
    1    CTCAJ023749 2014-10-22 2014-12-08  deployments
    2    CTCAJ033779 2014-10-22 2014-12-08  deployments
    3    CTCAJ043772 2014-10-23 2014-12-08  deployments
    4    CTCAJ053782 2014-10-26 2014-12-08  deployments
    5    CTCAJ063750 2014-10-23 2014-12-08  deployments
    6    CTCAJ073781 2014-10-25 2014-12-08  deployments
    7    CTCAJ083775 2014-10-24 2014-12-08  deployments
    8    CTCAJ093776 2014-10-24 2014-12-06  deployments
    9    CTCAJ103744 2014-10-24 2014-12-04  deployments
    10   CTCAJ113742 2014-10-25 2014-12-12  deployments
    11   CTCAJ123777 2014-10-24 2014-12-08  deployments
    12   CTCAJ133746 2014-10-26 2014-12-08  deployments
    13   CTCAJ143747 2014-10-24 2014-12-08  deployments
    14   CTCAJ143748 2014-10-24 2014-12-08  deployments
    15   CTCAJ153745 2014-10-27 2014-12-08  deployments
    16   CTCAJ163747 2014-10-25 2014-12-08  deployments
    17   CTCAJ183778 2014-10-25 2014-12-08  deployments
    18   CTCAJ193741 2014-10-25 2014-12-08  deployments
    ```

=== "images"
    ```pycon hl_lines="17"
    >>> wiutils.get_date_ranges(images=images, source="images")

       deployment_id start_date   end_date  source
    0    CTCAJ013743 2014-10-22 2014-12-08  images
    1    CTCAJ023749 2014-10-22 2014-12-08  images
    2    CTCAJ033779 2014-10-22 2014-12-08  images
    3    CTCAJ043772 2014-10-23 2014-12-08  images
    4    CTCAJ053782 2014-10-26 2014-12-08  images
    5    CTCAJ063750 2014-10-23 2014-12-08  images
    6    CTCAJ073781 2014-10-25 2014-12-08  images
    7    CTCAJ083775 2014-10-24 2014-12-08  images
    8    CTCAJ093776 2014-10-24 2014-12-06  images
    9    CTCAJ103744 2014-10-24 2014-12-04  images
    10   CTCAJ113742 2014-10-25 2014-12-12  images
    11   CTCAJ123777 2014-10-24 2014-12-08  images
    12   CTCAJ133746 2014-10-26 2014-12-08  images
    13   CTCAJ143747 2014-11-28 2014-11-28  images
    14   CTCAJ143748 2014-10-24 2014-12-08  images
    15   CTCAJ153745 2014-10-27 2014-12-08  images
    16   CTCAJ163747 2014-10-25 2014-12-08  images
    17   CTCAJ183778 2014-10-25 2014-12-08  images
    18   CTCAJ193741 2014-10-25 2014-12-08  images
    ```

=== "both"
    ```pycon hl_lines="17 36"
    >>> wiutils.get_date_ranges(images, deployments, source="both")

       deployment_id start_date   end_date       source
    0    CTCAJ013743 2014-10-22 2014-12-08       images
    1    CTCAJ023749 2014-10-22 2014-12-08       images
    2    CTCAJ033779 2014-10-22 2014-12-08       images
    3    CTCAJ043772 2014-10-23 2014-12-08       images
    4    CTCAJ053782 2014-10-26 2014-12-08       images
    5    CTCAJ063750 2014-10-23 2014-12-08       images
    6    CTCAJ073781 2014-10-25 2014-12-08       images
    7    CTCAJ083775 2014-10-24 2014-12-08       images
    8    CTCAJ093776 2014-10-24 2014-12-06       images
    9    CTCAJ103744 2014-10-24 2014-12-04       images
    10   CTCAJ113742 2014-10-25 2014-12-12       images
    11   CTCAJ123777 2014-10-24 2014-12-08       images
    12   CTCAJ133746 2014-10-26 2014-12-08       images
    13   CTCAJ143747 2014-11-28 2014-11-28       images
    14   CTCAJ143748 2014-10-24 2014-12-08       images
    15   CTCAJ153745 2014-10-27 2014-12-08       images
    16   CTCAJ163747 2014-10-25 2014-12-08       images
    17   CTCAJ183778 2014-10-25 2014-12-08       images
    18   CTCAJ193741 2014-10-25 2014-12-08       images
    19   CTCAJ013743 2014-10-22 2014-12-08  deployments
    20   CTCAJ023749 2014-10-22 2014-12-08  deployments
    21   CTCAJ033779 2014-10-22 2014-12-08  deployments
    22   CTCAJ043772 2014-10-23 2014-12-08  deployments
    23   CTCAJ053782 2014-10-26 2014-12-08  deployments
    24   CTCAJ063750 2014-10-23 2014-12-08  deployments
    25   CTCAJ073781 2014-10-25 2014-12-08  deployments
    26   CTCAJ083775 2014-10-24 2014-12-08  deployments
    27   CTCAJ093776 2014-10-24 2014-12-06  deployments
    28   CTCAJ103744 2014-10-24 2014-12-04  deployments
    29   CTCAJ113742 2014-10-25 2014-12-12  deployments
    30   CTCAJ123777 2014-10-24 2014-12-08  deployments
    31   CTCAJ133746 2014-10-26 2014-12-08  deployments
    32   CTCAJ143747 2014-10-24 2014-12-08  deployments
    33   CTCAJ143748 2014-10-24 2014-12-08  deployments
    34   CTCAJ153745 2014-10-27 2014-12-08  deployments
    35   CTCAJ163747 2014-10-25 2014-12-08  deployments
    36   CTCAJ183778 2014-10-25 2014-12-08  deployments
    37   CTCAJ193741 2014-10-25 2014-12-08  deployments
    ```

As you can see, one of the deployments (`CTCAJ143747`) was installed from 2014-10-24 to 2014-12-08 but the images only span over one day: 2014-11-28.

This is easier to see if we compute the delta between the start and end dates. The `get_date_ranges` already has a parameter for that:
```pycon hl_lines="17 36"
>>> wiutils.get_date_ranges(images, deployments, source="both", compute_delta=True)

   deployment_id start_date   end_date       source  delta
0    CTCAJ013743 2014-10-22 2014-12-08       images     47
1    CTCAJ023749 2014-10-22 2014-12-08       images     47
2    CTCAJ033779 2014-10-22 2014-12-08       images     47
3    CTCAJ043772 2014-10-23 2014-12-08       images     46
4    CTCAJ053782 2014-10-26 2014-12-08       images     43
5    CTCAJ063750 2014-10-23 2014-12-08       images     46
6    CTCAJ073781 2014-10-25 2014-12-08       images     44
7    CTCAJ083775 2014-10-24 2014-12-08       images     45
8    CTCAJ093776 2014-10-24 2014-12-06       images     43
9    CTCAJ103744 2014-10-24 2014-12-04       images     41
10   CTCAJ113742 2014-10-25 2014-12-12       images     48
11   CTCAJ123777 2014-10-24 2014-12-08       images     45
12   CTCAJ133746 2014-10-26 2014-12-08       images     43
13   CTCAJ143747 2014-11-28 2014-11-28       images      0
14   CTCAJ143748 2014-10-24 2014-12-08       images     45
15   CTCAJ153745 2014-10-27 2014-12-08       images     42
16   CTCAJ163747 2014-10-25 2014-12-08       images     44
17   CTCAJ183778 2014-10-25 2014-12-08       images     44
18   CTCAJ193741 2014-10-25 2014-12-08       images     44
19   CTCAJ013743 2014-10-22 2014-12-08  deployments     47
20   CTCAJ023749 2014-10-22 2014-12-08  deployments     47
21   CTCAJ033779 2014-10-22 2014-12-08  deployments     47
22   CTCAJ043772 2014-10-23 2014-12-08  deployments     46
23   CTCAJ053782 2014-10-26 2014-12-08  deployments     43
24   CTCAJ063750 2014-10-23 2014-12-08  deployments     46
25   CTCAJ073781 2014-10-25 2014-12-08  deployments     44
26   CTCAJ083775 2014-10-24 2014-12-08  deployments     45
27   CTCAJ093776 2014-10-24 2014-12-06  deployments     43
28   CTCAJ103744 2014-10-24 2014-12-04  deployments     41
29   CTCAJ113742 2014-10-25 2014-12-12  deployments     48
30   CTCAJ123777 2014-10-24 2014-12-08  deployments     45
31   CTCAJ133746 2014-10-26 2014-12-08  deployments     43
32   CTCAJ143747 2014-10-24 2014-12-08  deployments     45
33   CTCAJ143748 2014-10-24 2014-12-08  deployments     45
34   CTCAJ153745 2014-10-27 2014-12-08  deployments     42
35   CTCAJ163747 2014-10-25 2014-12-08  deployments     44
36   CTCAJ183778 2014-10-25 2014-12-08  deployments     44
37   CTCAJ193741 2014-10-25 2014-12-08  deployments     44
```

If you prefer wide-format tables over long-format tables, the `get_date_ranges` has a `pivot` parameter:
```pycon hl_lines="19"
>>> wiutils.get_date_ranges(images, deployments, source="both", compute_delta=True, pivot=True)

               start_date               end_date                  delta
source        deployments     images deployments     images deployments images
deployment_id
CTCAJ013743    2014-10-22 2014-10-22  2014-12-08 2014-12-08          47     47
CTCAJ023749    2014-10-22 2014-10-22  2014-12-08 2014-12-08          47     47
CTCAJ033779    2014-10-22 2014-10-22  2014-12-08 2014-12-08          47     47
CTCAJ043772    2014-10-23 2014-10-23  2014-12-08 2014-12-08          46     46
CTCAJ053782    2014-10-26 2014-10-26  2014-12-08 2014-12-08          43     43
CTCAJ063750    2014-10-23 2014-10-23  2014-12-08 2014-12-08          46     46
CTCAJ073781    2014-10-25 2014-10-25  2014-12-08 2014-12-08          44     44
CTCAJ083775    2014-10-24 2014-10-24  2014-12-08 2014-12-08          45     45
CTCAJ093776    2014-10-24 2014-10-24  2014-12-06 2014-12-06          43     43
CTCAJ103744    2014-10-24 2014-10-24  2014-12-04 2014-12-04          41     41
CTCAJ113742    2014-10-25 2014-10-25  2014-12-12 2014-12-12          48     48
CTCAJ123777    2014-10-24 2014-10-24  2014-12-08 2014-12-08          45     45
CTCAJ133746    2014-10-26 2014-10-26  2014-12-08 2014-12-08          43     43
CTCAJ143747    2014-10-24 2014-11-28  2014-12-08 2014-11-28          45      0
CTCAJ143748    2014-10-24 2014-10-24  2014-12-08 2014-12-08          45     45
CTCAJ153745    2014-10-27 2014-10-27  2014-12-08 2014-12-08          42     42
CTCAJ163747    2014-10-25 2014-10-25  2014-12-08 2014-12-08          44     44
CTCAJ183778    2014-10-25 2014-10-25  2014-12-08 2014-12-08          44     44
CTCAJ193741    2014-10-25 2014-10-25  2014-12-08 2014-12-08          44     44
```

!!! note

    When using `pivot=True`, the resulting dataframe will have a [`pandas.MultiIndex`](https://pandas.pydata.org/docs/user_guide/advanced.html#advanced-hierarchical) on the column axis.

## Getting the scientific names
Wildlife Insights' images file has a set of columns with the taxonomic classification for identified images. However, these columns do not include the scientific name; the genus and epithet are stored in independent columns (*i.e.* `genus` and `species`). The `get_scientific_name` function is a convenient function to concatenate those two columns while accounting for images where the classification down to the species was not possible.

For example, lets take a look at those two columns in the images dataframe:
```pycon
>>> images[["genus", "species"]]

        genus  species
0        Homo  sapiens
1     Tinamus    major
2        Homo  sapiens
3     Tinamus    major
4        Homo  sapiens
       ...      ...
5248      NaN      NaN
5249   Mazama   temama
5250      NaN      NaN
5251      NaN      NaN
5252  Tinamus    major
```

We can use the `get_scientific_name` to extract the scientific name for each image:
```pycon
>>> wiutils.get_scientific_name(images)

0        Homo sapiens
1       Tinamus major
2        Homo sapiens
3       Tinamus major
4        Homo sapiens
            ...
5248              NaN
5249    Mazama temama
5250              NaN
5251              NaN
5252    Tinamus major
```

Notice how the scientific name is left empty in some images as they did not have any classification (at least up to species rank).

By default, the scientific name for all the images without a classification down to the species rank will be left empty. However, there might be some cases where a classification down to genus (but not species) was made, and you want to keep the genus as the scientific name. For those cases, there is the `keep_genus` parameter.

We can find these cases in our dataset first:
```pycon
>>> images.loc[(images["genus"].notna()) & (images["species"].isna()), "genus"].unique()

Int64Index([ 639,  656,  709,  733, 1196, 1229, 1404, 1405, 1431, 1443, 1858,
            3237, 3269, 3740, 3846, 3894, 4136, 4170, 4185, 4515, 4551],
           dtype='int64')
```
There are multiple images where the genus was identified but the species was not.

We can now create a subset including one of these images (and another two just for comparison purposes):
```pycon
>>> subset = images.loc[[1, 5, 639]]
>>> subset[["genus", "species"]]

         genus species
1      Tinamus   major
5          NaN     NaN
639  Leptotila     NaN
```



And now, we can illustrate the difference when using the default value for the parameter and when setting it to `True`.

=== "`keep_genus=False`"

    ```pycon
    >>> wiutils.get_scientific_name(subset, keep_genus=False)

    1      Tinamus major
    5                NaN
    639              NaN
    dtype: object
    ```

=== "`keep_genus=True`"

    ```pycon
    >>> wiutils.get_scientific_name(subset, keep_genus=True)

    1      Tinamus major
    5                NaN
    639        Leptotila
    dtype: object
    ```

There might be some cases where you want to add an Open Nomenclature classifier (*i.e.* [sp., *"[...] used after the generic name when the specimen has not been identified down to the species level [...]"*](https://doi.org/10.1111/2041-210X.12594)) to the resulting scientific name for images where the classification got down to genus but not species. The `get_scientific_name` function has another parameter for this: `add_qualifier`. Note that this parameter only has an effect when `keep_genus=True`.
```pycon
>>> wiutils.get_scientific_name(subset, keep_genus=True, add_qualifier=True)

1      Tinamus major
5                NaN
639    Leptotila sp.
```

Notice how the qualifier was only added for the specific case where the genus was present but the species was not.

## Getting the lowest taxa and ranks
In many cases, you'll want to be able to extract the lowest identified taxa for the images and maybe their ranks as well. The `get_lowest_taxon` function allows you to get this information.

Let's find those cases where the images were just identified down to the family level.
```pycon
>>> images[(images["family"].notna()) & (images["genus"].isna())].index

Int64Index([ 788,  789,  790,  801,  808,  820,  821,  822,  831,  832,
            ...
            5230, 5231, 5232, 5233, 5236, 5237, 5240, 5241, 5248, 5250],
           dtype='int64', length=222)
```

Let's create a new subset to illustrate how this function works. We will use a subset like the last one, but we will add another row with one of the images we just found.
```pycon
>>> subset = images.loc[[1, 5, 639, 788]]
>>> subset[["family", "genus", "species"]]

          family      genus species
1      Tinamidae    Tinamus   major
5            NaN        NaN     NaN
639   Columbidae  Leptotila     NaN
788  Didelphidae        NaN     NaN
```

We can now use the `get_lowest_taxon` function to get the lowest identified taxon for each image:
```pycon
>>> wiutils.get_lowest_taxon(subset)

1      Tinamus major
5                NaN
639        Leptotila
788      Didelphidae
dtype: object
```

We can also get the lowest identified rank by using the `return_rank` parameter:
```pycon
>>> taxa, ranks = wiutils.get_lowest_taxon(subset, return_rank=True)
>>> ranks

1      species
5          NaN
639      genus
788     family
dtype: object
```
