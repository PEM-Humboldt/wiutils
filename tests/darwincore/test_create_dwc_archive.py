"""
Test cases for the wiutils.darwincore.create_dwc_archive function.
"""

import wiutils.darwincore
from wiutils.darwincore import create_dwc_archive


def test_calls(mocker):
    mocker.patch("wiutils.darwincore.create_dwc_event")
    mocker.patch("wiutils.darwincore.create_dwc_measurement")
    mocker.patch("wiutils.darwincore.create_dwc_multimedia")
    mocker.patch("wiutils.darwincore.create_dwc_occurrence")
    create_dwc_archive(None, None, None, None)
    wiutils.darwincore.create_dwc_event.assert_called_once()
    wiutils.darwincore.create_dwc_measurement.assert_called_once()
    wiutils.darwincore.create_dwc_multimedia.assert_called_once()
    wiutils.darwincore.create_dwc_occurrence.assert_called_once()
