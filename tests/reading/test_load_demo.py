"""
Test cases for the wiutils.reading.load_demo function.
"""
import pytest

from wiutils.reading import load_demo


def test_demo_one():
    cameras, deployments, images, projects = load_demo("cajambre")
    assert cameras.shape == (18, 6)
    assert deployments.shape == (19, 27)
    assert images.shape == (5253, 26)
    assert projects.shape == (1, 27)


def test_demo_two():
    cameras, deployments, images, projects = load_demo("cristales")
    assert cameras.shape == (19, 6)
    assert deployments.shape == (19, 27)
    assert images.shape == (4950, 26)
    assert projects.shape == (1, 27)


def test_invalid_name():
    with pytest.raises(ValueError):
        load_demo("dct")
