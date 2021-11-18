# wiutils

`wiutils` has utilities for exploring and transforming information downloaded from Wildlife Insights projects.

## Installation

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

* Angélica Diaz-Pulido
* Marcelo Villa-Piñeros - [marcelovilla](https://github.com/marcelovilla)

## License
This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

[1]: https://github.com/Toblerity/Fiona#installation
[2]: https://github.com/mapbox/rasterio#installation
