# Summarizing

## Overview
Summarizing functions allow you to group images by deployment, location or taxon and compute detection or abundance statistics.

Here is a quick overview of the different summarizing functions and their description:


| Function                                                                                 | Description                                                                                                                                          |
|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`compute_count_summary`](/reference/#wiutils.summarizing.compute_count_summary)         | Computes a summary of images, records and taxa count by deployment.                                                                                  |
| [`compute_detection`](/reference/#wiutils.summarizing.compute_detection)                 | Computes the detection (in terms of abundance or presence)of each taxon by deployment.                                                               |
| [`compute_detection_history`](/reference/#wiutils.summarizing.compute_detection_history) | Computes the detection history (in terms of abundance or presence) by taxon and deployment, grouping observations into specific days-long intervals. |
| [`compute_general_count`](/reference/#wiutils.summarizing.compute_general_count)         | Computes the general abundance and number of deployments for each taxon.                                                                             |
| [`compute_hill_numbers`](/reference/#wiutils.summarizing.compute_hill_numbers)           | Computes the Hill numbers of order q (also called effective number of species) by site for some given values of q.                                   |


Except from the `compute_detection_history` function, all the summarizing functions have a `groupby` argument to specify whether the results should be grouped by deployment (using the `deployment_id` column in the images file) or by location (using the `placename` columns in the deployments file). By default, this argument is `"deployment"` but you might want to use `"location"` for those projects where each location had multiple deployments over time.

Another important thing to mention is that, because images can have multiple objects (*i.e.* animals), abundance across summarizing functions is computed by summing the `number_of_objects` column of the images file rather than counting each image as an individual.

!!! note

    All the summarizing functions group images by taxa to compute the different statistics. If you want to ignore images that do not have a species or genus level identification, make sure to use the `remove_unidentified` function on the images dataframe first.

For every snippet of code showed here, we will assume you have already run the following code:
```python
import wiutils

cameras, deployments, images, projects = wiutils.load_demo("cajambre")
```

## Computing count summary
The `compute_count_summary` functions allows you to get a summary of images and identifications by deployment.

!!! note

    The `compute_count_summary` function removes unidentified and duplicate images under the hood to get the number of identified images and records. Thus, you should avoid using these filters on the images dataframe before calling this function.

Here is an example:
```pycon
>>> wiutils.compute_count_summary(images)

   deployment_id  total_images  identified_images  records  taxa
0    CTCAJ013743           501                397       33     9
1    CTCAJ023749            75                 59       10     8
2    CTCAJ033779           156                118       25    10
3    CTCAJ043772           351                291       26     6
4    CTCAJ053782           222                148       29     7
5    CTCAJ063750           186                153       31    11
6    CTCAJ073781           120                108       15     8
7    CTCAJ083775           600                544       56    11
8    CTCAJ093776           978                888       58    14
9    CTCAJ103744           174                118       22     8
10   CTCAJ113742           321                272       55     7
11   CTCAJ123777           210                138       38    11
12   CTCAJ133746           236                178       31    10
13   CTCAJ143747             1                  1        1     1
14   CTCAJ143748            75                 63       12     7
15   CTCAJ153745           111                 86       15     7
16   CTCAJ163747           327                288       54     9
17   CTCAJ183778           216                164       27     7
18   CTCAJ193741           393                322       56     8
```

By default, this function return a dataframe with the following columns:

- `total_images`: the number of images for each deployment.
- `identified_images`: the number of images for each deployment.
- `records`: the number of records (*i.e.* number of individuals of the same taxa after duplicate image removal) for each deployment.
- `taxa`: number of unique taxa for each deployment.

This function uses two filters to compute the last three columns: `remove_unidentified` and `remove_duplicates`. In order to control the behavior of these filters (*i.e.* change the default filter values), the `compute_count_summary` has two arguments: `remove_unidentified_kws` and `remove_duplicates_kws`. Both accept a dictionary with the arguments that are going to be passed to the [`remove_unidentified`](/reference/#wiutils.filtering.remove_unidentified) and the [`remove_duplicates`](/reference/#wiutils.filtering.remove_duplicates) functions. For example, you might want this summary to have the number of identified images for everything that was identified down to at least the family level and remove those duplicate images withing a five-day window:
```pycon
>>> wiutils.compute_count_summary(images, remove_unidentified_kws={"rank": "family"}, remove_duplicates_kws={"interval": 5, "unit": "days"})

   deployment_id  total_images  identified_images  records  taxa
0    CTCAJ013743           501                379       16     8
1    CTCAJ023749            75                 57        8     7
2    CTCAJ033779           156                106       15     8
3    CTCAJ043772           351                291       12     6
4    CTCAJ053782           222                148       17     7
5    CTCAJ063750           186                153       19    11
6    CTCAJ073781           120                108       12     8
7    CTCAJ083775           600                535       24     8
8    CTCAJ093776           978                229       24    13
9    CTCAJ103744           174                118       14     8
10   CTCAJ113742           321                260       12     6
11   CTCAJ123777           210                135       19    10
12   CTCAJ133746           236                172       19     9
13   CTCAJ143747             1                  1        1     1
14   CTCAJ143748            75                 63       10     7
15   CTCAJ153745           111                 86       13     7
16   CTCAJ163747           327                270       14     7
17   CTCAJ183778           216                164       14     7
18   CTCAJ193741           393                319       14     7
```

Notice how there are fewer identified images, fewer number of records and fewer number of unique taxa in each deployment.

The `compute_count_summary` function also offer two arguments to add number of records and taxa divided by class: `add_records_by_class` and `add_taxa_by_class`:
```pycon
>>> result = wiutils.compute_count_summary(images, add_records_by_class=True, add_taxa_by_class=True)
>>> result.columns

Index(['deployment_id', 'total_images', 'identified_images', 'records',
       'records_mammalia', 'records_aves', 'records_reptilia',
       'records_amphibia', 'taxa', 'taxa_mammalia', 'taxa_aves',
       'taxa_reptilia', 'taxa_amphibia'],
      dtype='object')
```

Notice how the result has now more columns, with records and taxa discriminated by taxonomic class. Depending on the number of unique classes present in the images file, the number of columns will vary. For example, if you had only mammals in your images, only two new columns would have been created: `records_mammalia` and `taxa_mammalia`.

If instead of grouping taxa by deployment you want to group taxa by location, use the `groupby` parameter (notice that you have to pass the deployments dataframe as well):
```pycon
>>> wiutils.compute_count_summary(images, deployments, groupby="location")

   placename  total_images  identified_images  records  taxa
0    CTCAJ01           501                397       33     9
1    CTCAJ02            75                 59       10     8
2    CTCAJ03           156                118       25    10
3    CTCAJ04           351                291       26     6
4    CTCAJ05           222                148       29     7
5    CTCAJ06           186                153       31    11
6    CTCAJ07           120                108       15     8
7    CTCAJ08           600                544       56    11
8    CTCAJ09           978                888       58    14
9    CTCAJ10           174                118       22     8
10   CTCAJ11           321                272       55     7
11   CTCAJ12           210                138       38    11
12   CTCAJ13           236                178       31    10
13   CTCAJ14            76                 64       13     8
14   CTCAJ15           111                 86       15     7
15   CTCAJ16           327                288       54     9
16   CTCAJ18           216                164       27     7
17   CTCAJ19           393                322       56     8
```

## Computing detection
The `compute_detection` function allows you to compute abundance by taxon by deployment (or location).
```pycon
>>> wiutils.compute_detection(images)

             taxon deployment_id  value
0         Amphibia   CTCAJ013743      0
1         Amphibia   CTCAJ023749      0
2         Amphibia   CTCAJ033779      0
3         Amphibia   CTCAJ043772      0
4         Amphibia   CTCAJ053782      0
..             ...           ...    ...
565  Tinamus major   CTCAJ143748      0
566  Tinamus major   CTCAJ153745     48
567  Tinamus major   CTCAJ163747    127
568  Tinamus major   CTCAJ183778      6
569  Tinamus major   CTCAJ193741     13

[570 rows x 3 columns]
```

If instead of computing the number of observations we just wanted to compute presence and absence, we can set the `compute_abundance` parameter to `False`:
```pycon
>>> wiutils.compute_detection(images, compute_abundance=False)

             taxon deployment_id  value
0         Amphibia   CTCAJ013743      0
1         Amphibia   CTCAJ023749      0
2         Amphibia   CTCAJ033779      0
3         Amphibia   CTCAJ043772      0
4         Amphibia   CTCAJ053782      0
..             ...           ...    ...
565  Tinamus major   CTCAJ143748      0
566  Tinamus major   CTCAJ153745      1
567  Tinamus major   CTCAJ163747      1
568  Tinamus major   CTCAJ183778      1
569  Tinamus major   CTCAJ193741      1

[570 rows x 3 columns]
```

If you prefer a wide-format table over a long-format table, use the `pivot` parameter:
```pycon
>>> wiutils.compute_detection(images, pivot=True)
                       taxon  CTCAJ013743  ...  CTCAJ183778  CTCAJ193741
0                   Amphibia            0  ...            0            0
1                       Aves           18  ...            0            3
2           Canis familiaris            3  ...            0            0
3                 Crax rubra            0  ...            0            0
4    Crypturellus berlepschi            0  ...            0            0
5             Cuniculus paca            0  ...            0            0
6        Dasyprocta punctata            0  ...            0            0
7       Dasypus novemcinctus            5  ...            0            0
8                Didelphidae            0  ...            0          165
9      Didelphis marsupialis            6  ...            0            0
10              Eira barbara            0  ...            0           12
11  Herpailurus yagouaroundi            0  ...            0            0
12              Homo sapiens          287  ...            9           30
13        Leopardus pardalis            6  ...            0            0
14                 Leptotila            0  ...            0            0
15   Leptotrygon veraguensis            0  ...            0           16
16             Mazama temama            0  ...          110           81
17      Micrastur ruficollis           10  ...            0            0
18             Pecari tajacu            0  ...            0            0
19           Penelope ortoni            0  ...            0            0
20       Procyon cancrivorus            0  ...            0            0
21   Proechimys semispinosus            5  ...            9            0
22                  Rallidae            0  ...            9            0
23       Rhynchortyx cinctus            0  ...            0            0
24                  Rodentia            0  ...            0            0
25       Sciurus granatensis            0  ...            3            0
26                  Squamata            0  ...            0            0
27         Tamandua mexicana            0  ...            0            3
28        Tigrisoma lineatum            0  ...           30            0
29             Tinamus major           57  ...            6           13

[30 rows x 20 columns]
```

If instead of grouping observations by deployment you want to group observations by location, use the `groupby` parameter (notice that you have to pass the deployments dataframe as well):
```pycon

             taxon placename  value
0         Amphibia   CTCAJ01      0
1         Amphibia   CTCAJ02      0
2         Amphibia   CTCAJ03      0
3         Amphibia   CTCAJ04      0
4         Amphibia   CTCAJ05      0
..             ...       ...    ...
535  Tinamus major   CTCAJ14      0
536  Tinamus major   CTCAJ15     48
537  Tinamus major   CTCAJ16    127
538  Tinamus major   CTCAJ18      6
539  Tinamus major   CTCAJ19     13

[540 rows x 3 columns]
```

## Computing detection history
Detection histories summarize taxa observations in each deployment over time. They are useful to create occupancy models (see the [R package `unmarked`](https://www.jstatsoft.org/article/view/v043i10) for examples). The `compute_detection_history` allows you to create detection histories using an arbitrary number of days to group observations into.

!!! note

    All images without an identification down to at least the class level will be removed before computing the detection histories. You can use the `remove_unidentified` function before if you want to narrow the images even further down to more specific rank (*e.g.* genus).

By default, observations are going to be grouped into one-day intervals but the `days` parameter lets you control this number. For example, we can group observations into multiple five-day intervals:
```pycon
>>> wiutils.compute_detection_history(images, deployments, days=5)

              taxon deployment_id  timestamp  value
0          Amphibia   CTCAJ013743 2014-10-22    0.0
1          Amphibia   CTCAJ013743 2014-10-27    0.0
2          Amphibia   CTCAJ013743 2014-11-01    0.0
3          Amphibia   CTCAJ013743 2014-11-06    0.0
4          Amphibia   CTCAJ013743 2014-11-11    0.0
             ...           ...        ...    ...
6265  Tinamus major   CTCAJ193741 2014-11-21    0.0
6266  Tinamus major   CTCAJ193741 2014-11-26    0.0
6267  Tinamus major   CTCAJ193741 2014-12-01    0.0
6268  Tinamus major   CTCAJ193741 2014-12-06    0.0
6269  Tinamus major   CTCAJ193741 2014-12-11    NaN

[6270 rows x 4 columns]
```

In this result, there is a row for the observations (`value` column) during a specific interval for a taxon in a given deployment. One thing to note is that, by default, the interval start date (in this case 2014-10-22) is taken from the earliest start date of all the deployments. For different reasons that were already explained in the [extraction section](extraction.md#getting-date-ranges), you might want the interval start date to rather be the date of the first image across all the deployments. In that case, pass `date_range="images"` when calling the `compute_detection_history` function.

If you prefer a wide-format table over a long-format table, use the `pivot` parameter:
```pycon
>>> wiutils.compute_detection_history(images, deployments, days=5, pivot=True)

             taxon deployment_id  ...  2014-12-06  2014-12-11
0         Amphibia   CTCAJ013743  ...         0.0         NaN
1         Amphibia   CTCAJ023749  ...         0.0         NaN
2         Amphibia   CTCAJ033779  ...         0.0         NaN
3         Amphibia   CTCAJ043772  ...         0.0         NaN
4         Amphibia   CTCAJ053782  ...         0.0         NaN
..             ...           ...  ...         ...         ...
565  Tinamus major   CTCAJ143748  ...         0.0         NaN
566  Tinamus major   CTCAJ153745  ...         3.0         NaN
567  Tinamus major   CTCAJ163747  ...        12.0         NaN
568  Tinamus major   CTCAJ183778  ...         0.0         NaN
569  Tinamus major   CTCAJ193741  ...         0.0         NaN

[570 rows x 13 columns]
```

Look how now there is a column for each interval and the number of rows is much smaller.

If instead of computing the number of observations we just wanted to compute presence and absence, we can set the `compute_abundance` parameter to `False`:
```pycon hl_lines="11 12"
>>> wiutils.compute_detection_history(images, deployments, days=5, compute_abundance=False, pivot=True)

             taxon deployment_id  ...  2014-12-06  2014-12-11
0         Amphibia   CTCAJ013743  ...         0.0         NaN
1         Amphibia   CTCAJ023749  ...         0.0         NaN
2         Amphibia   CTCAJ033779  ...         0.0         NaN
3         Amphibia   CTCAJ043772  ...         0.0         NaN
4         Amphibia   CTCAJ053782  ...         0.0         NaN
..             ...           ...  ...         ...         ...
565  Tinamus major   CTCAJ143748  ...         0.0         NaN
566  Tinamus major   CTCAJ153745  ...         1.0         NaN
567  Tinamus major   CTCAJ163747  ...         1.0         NaN
568  Tinamus major   CTCAJ183778  ...         0.0         NaN
569  Tinamus major   CTCAJ193741  ...         0.0         NaN

[570 rows x 13 columns]
```

In the examples above, you can see that there are multiple `NaN` values. These correspond to intervals that are outside the corresponding deployment date range and are thus masked.

## Computing general count
The `compute_general_count` allows you to create a summary of observations by taxon.
```pycon
>>> wiutils.compute_general_count(images)

                       taxon     n  deployments
0                   Amphibia     3            1
1                       Aves  1014            9
2           Canis familiaris     3            1
3                 Crax rubra   274            7
4    Crypturellus berlepschi    12            2
5             Cuniculus paca   248           10
6        Dasyprocta punctata    16            3
7       Dasypus novemcinctus   414           10
8                Didelphidae   213            4
9      Didelphis marsupialis   199           13
10              Eira barbara    18            2
11  Herpailurus yagouaroundi     6            1
12              Homo sapiens   478           16
13        Leopardus pardalis    23            3
14                 Leptotila    21            4
15   Leptotrygon veraguensis   285            5
16             Mazama temama   285            5
17      Micrastur ruficollis    15            2
18             Pecari tajacu   335            2
19           Penelope ortoni    12            1
20       Procyon cancrivorus    24            3
21   Proechimys semispinosus   389           17
22                  Rallidae     9            1
23       Rhynchortyx cinctus    54            3
24                  Rodentia     3            1
25       Sciurus granatensis    23            5
26                  Squamata    18            3
27         Tamandua mexicana    76            8
28        Tigrisoma lineatum    30            1
29             Tinamus major   457           16
```

It shows the number of individuals for each taxon as well as the number of deployments where that particular taxon was recorded (at least once).

You can also add the higher taxonomic classification for each taxon using the `add_taxonomy` parameter:
```pycon
>>> result = wiutils.compute_general_count(images, add_taxonomy=True)
>>> result.columns

Index(['taxon', 'n', 'deployments', 'class', 'order', 'family', 'genus',
       'species'],
      dtype='object')
```

If instead of getting the number of deployments where each taxon was recorded you want to get the number of locations, use the `groupby` parameter (notice that you have to pass the deployments dataframe as well):
```pycon
>>> wiutils.compute_general_count(images, deployments, groupby="location")

                       taxon     n  locations
0                   Amphibia     3          1
1                       Aves  1014          9
2           Canis familiaris     3          1
3                 Crax rubra   274          7
4    Crypturellus berlepschi    12          2
5             Cuniculus paca   248         10
6        Dasyprocta punctata    16          3
7       Dasypus novemcinctus   414         10
8                Didelphidae   213          4
9      Didelphis marsupialis   199         13
10              Eira barbara    18          2
11  Herpailurus yagouaroundi     6          1
12              Homo sapiens   478         16
13        Leopardus pardalis    23          3
14                 Leptotila    21          4
15   Leptotrygon veraguensis   285          5
16             Mazama temama   285          5
17      Micrastur ruficollis    15          2
18             Pecari tajacu   335          2
19           Penelope ortoni    12          1
20       Procyon cancrivorus    24          3
21   Proechimys semispinosus   389         17
22                  Rallidae     9          1
23       Rhynchortyx cinctus    54          3
24                  Rodentia     3          1
25       Sciurus granatensis    23          5
26                  Squamata    18          3
27         Tamandua mexicana    76          8
28        Tigrisoma lineatum    30          1
29             Tinamus major   457         16
```

## Computing hill numbers
Hill numbers or the effective number of species are diversity indices used to quantify the taxonomic diversity in a community. Hill numbers are parameterized by an order $q$, which determines the sensitivity to species (or taxa) relative abundances.

For any value of $q$ different from $1$, the corresponding diversity index is computed as follows:
$$
^{q}D = \left(\sum_{i=1}^{R} p_{i}^{q}\right)^{1/(1-q)}
$$

When $q=1$, the diversity index is computed as follows:
$$
^{1}D = exp \left(-\sum_{i=1}^{R} p_{i} \ln(p_{i})\right)
$$

In both equations, $R$ is richness (*i.e.* total number of species or taxa) and $p_i$ is the relative abundance of species or taxon $i$.

The most common values of $q$ that are used to compute Hill numbers are:

- $0$, which corresponds to species richness.
- $1$, which corresponds to the Shannon diversity.
- $2$, which corresponds to the Simpson diversity.

The `compute_hill_numbers` function allows you to compute these indices for any given values of $q$, grouping taxa by deployment or location. By default, Hill numbers are computed using $q$ values of $0$, $1$ and $2$.

For example, we can compute species richness, Shannon diversity and Simpson diversity for the demo dataset:
```pycon
>>> result = wiutils.compute_hill_numbers(images)
>>> result.head(9)  # Show just the first three deployments

  deployment_id  q          D
0   CTCAJ013743  0   9.000000
1   CTCAJ013743  1   2.773289
2   CTCAJ013743  2   1.828984
3   CTCAJ023749  0   8.000000
4   CTCAJ023749  1   5.444932
5   CTCAJ023749  2   4.080891
6   CTCAJ033779  0  10.000000
7   CTCAJ033779  1   7.020295
8   CTCAJ033779  2   5.701884
```

If you prefer wide-format tables over long-format tables, the `compute_hill_numbers` has a `pivot` parameter:
```pycon
>>> result = wiutils.compute_hill_numbers(images, pivot=True)
>>> result.head(3)  # Show just the first three deployments

  deployment_id     0         1         2
0   CTCAJ013743   9.0  2.773289  1.828984
1   CTCAJ023749   8.0  5.444932  4.080891
2   CTCAJ033779  10.0  7.020295  5.701884
```

If you wanted to compute just the Shannon and Simpson diversity, you can use the `q_values` parameter to change the default values:
```pycon
>>> result = wiutils.compute_hill_numbers(images, q_values=[1, 2])
>>> result.head(6) # Show just the first three deployments

  deployment_id  q         D
0   CTCAJ013743  1  2.773289
1   CTCAJ013743  2  1.828984
2   CTCAJ023749  1  5.444932
3   CTCAJ023749  2  4.080891
4   CTCAJ033779  1  7.020295
5   CTCAJ033779  2  5.701884
```

If instead of grouping taxa by deployment you want to group taxa by location, use the `groupby` parameter (notice that you have to pass the deployments dataframe as well):
```pycon
>>> result = wiutils.compute_hill_numbers(images, deployments, groupby="location")
>>> result.head(9) # Show just the first three deployments

   placename  q          D
0    CTCAJ01  0   9.000000
1    CTCAJ01  1   2.773289
2    CTCAJ01  2   1.828984
3    CTCAJ02  0   8.000000
4    CTCAJ02  1   5.444932
5    CTCAJ02  2   4.080891
6    CTCAJ03  0  10.000000
```
