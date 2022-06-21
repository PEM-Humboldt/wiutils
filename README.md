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
Everybody is welcome to contribute to `wiutils`. People can contribute to the development of the package but also to the improvement of the documentation and by [reporting potential bugs](https://github.com/PEM-Humboldt/wiutils/issues).

## Setup
It is recommended to install the package using a [virtual environment](https://www.python.org/dev/peps/pep-0405/) to avoid tampering other Python installations in your system.

Clone this repo in your computer:
```shell
git clone https://github.com/PEM-Humboldt/wiutils.git
```

Go to the project's root:
```shell
cd wiutils
```

Install the package in development mode:
```shell
pip install --editable .[dev,docs,test]
```

Make sure that any new development is done in a new branch. After you are finished, submit a [pull request](https://docs.github.com/en/pull-requests) to incorporate the changes.

## Unit tests
Execute the following command inside the project's root:
```shell
pytest tests/
```

## Python versions
`wiutils` works with Python versions 3.6 through 3.10. To make sure that the code works for all these versions, [`tox`](https://tox.wiki) is used. Make sure you have installed these Python versions on your system and then run the following command inside the project's root:
```shell
tox
```

This will run all the unit tests for every Python version to make sure everything works correctly.

If you add any new depedency to the project, make sure to run tox as follows so it can recreate the environments:
```shell
tox -r
```

## Code coverage
We make sure the code coverage is 100%. Ideally, when implementing new features or making changes, you should make sure that the code coverage is still 100%. For this, run the coverage for the tests:
```shell
coverage run -m pytest tests/
```

And then run the report:
```shell
coverage report -m -i
```

## Code style
We use pre-commit hooks to make sure new changes adhere to different coding guidelines. You need to install these hooks just once (ideally before doing any commit) by running:
```shell
pre-commit install
```

After that, every commit you try to make will run the hooks before committing the changes. If the hooks modified your changes, you'll have to add those files and commit again.

## Authors and contributors
* Adriana Restrepo-Isaza
* Angélica Diaz-Pulido
* Marcelo Villa-Piñeros - [marcelovilla](https://github.com/marcelovilla)

## License
This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.
