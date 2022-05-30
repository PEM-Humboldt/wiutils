# wiutils

![](https://img.shields.io/pypi/pyversions/wiutils)
![](https://img.shields.io/pypi/v/wiutils?color=blue)
![](https://img.shields.io/conda/vn/conda-forge/wiutils?color=blue)

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

You can use `wiutils` functions by importing the package from a Python console or script. For more information about the available functions, check the [documentation](https://wiutils.readthedocs.io).

## How to contribute
It is recommended to install the package using a [virtual environment](https://www.python.org/dev/peps/pep-0405/) to avoid tampering other Python installations in your system.

1. Clone this repo in your computer:
```shell
git clone https://github.com/PEM-Humboldt/wiutils.git
```

2. Go to the project's root:
```shell
cd wiutils
```

3. Install the package in development mode:
```shell
pip install --editable .[dev,docs,test]
```


### Unit tests
Execute the following command inside the project's root:
```
pytest tests/
```

## Authors and contributors
* Adriana Restrepo-Isaza
* Angélica Diaz-Pulido
* Marcelo Villa-Piñeros - [marcelovilla](https://github.com/marcelovilla)

## License
This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.
