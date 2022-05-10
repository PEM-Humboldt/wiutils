# Getting started

`wiutils` has several utilities for exploring and manipulating (filtering, plotting and summarizing) information from [Wildlife Insights](https://www.wildlifeinsights.org/) projects. These functions are useful to compute basic statistics, prepare the information for further analysis (*e.g.* occupancy models) and translate it into other standards (*i.e.* Darwin Core) that facilitate its publication on biodiversity information centers (*e.g.* GBIF).

## Installation
Currently, `wiutils` works with Python versions 3.6 through 3.10.

Using `pip`:
```shell
pip install wiutils
```

Using `conda`:
```shell
conda install -c conda-forge wiutils
```

## Execution
To check whether the installation of `wiutils` was successful, execute the following command:

```shell
python -c "import wiutils"
```
If this does not throw any error, the installation was successful.

You can use `wiutils` function by importing the package from a Python console or script. For more information about the available functions, check the [documentation](https://wiutils.readthedocs.io).
