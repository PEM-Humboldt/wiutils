# How to contribute
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
