"""
Constant values for the events and records DwC tables.
"""
import numpy as np

events = {
    "institutionCode": np.nan,
    "sampleSizeValue": 1,
    "sampleSizeUnit": "trap-nights",
    "samplingProtocol": "camera-trap",
    "continent": np.nan,
    "country": np.nan,
    "countryCode": np.nan,
    "stateProvince": np.nan,
    "county": np.nan,
    "locality": np.nan,
    "minimumElevationInMeters": np.nan,
    "maximumElevationInMeters": np.nan,
    "geodeticDatum": "EPSG:4326",
}

records = {
    "occurrenceID": np.nan,
    "basisOfRecord": "MachineObservation",
    "institutionCode": np.nan,
    "collectionCode": np.nan,
    "catalogNumber": np.nan,
    "preparations": "photograph",
    "dateIdentified": np.nan,
    "identificationQualifier": np.nan,
    "scientificNameAuthorship": np.nan,
}
