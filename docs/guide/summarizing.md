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


Except from the `compute_detection_history` function, all the summarizing functions have a `groupby` argument to specify whether the results should be groupped by deployment (using the `deployment_id` column in the images file) or by location (using the `placename` columns in the deployments file). By default, this argument is `"deployment"` but you might want to use `"location"` for those projects where each location had multiple deployments over time.

!!! note

    All the summarizing functions group images by taxa to compute the different statistics. If you want to ignore images that do not have a species or genus level identification, make sure to use the `remove_unidentified` function on the images dataframe first.

For every snippet of code showed here, we will assume you have already run the following code:
```python
import wiutils

cameras, deployments, images, projects = wiutils.load_demo("cajambre")
```

## Computing count summary

## Computing detection

## Computing detection history

## Computing general count

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
