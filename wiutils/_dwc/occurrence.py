"""
Mapping from WI fields to DwC terms, constant values and term order for
the Darwin Core Occurrence dataframe creation.
"""
constants = {
    "basisOfRecord": "MachineObservation",
    "preparations": "photograph",
}

mapping = {
    "deployment_id": "eventID",
    "placename": "parentEventID",
    "identified_by": "identifiedBy",
    "image_id": "recordNumber",
    "recorded_by": "recordedBy",
    "number_of_objects": "organismQuantity",
    "sex": "sex",
    "age": "lifeStage",
    "individual_animal_notes": "occurrenceRemarks",
    "individual_id": "organismID",
    "wi_taxon_id": "taxonID",
    "class": "class",
    "order": "order",
    "family": "family",
    "genus": "genus",
    "common_name": "vernacularName",
}

order = [
    "eventID",
    "parentEventID",
    "eventDate",
    "eventTime",
    "identifiedBy",
    "identificationRemarks",
    "recordNumber",
    "recordedBy",
    "organismQuantity",
    "organismQuantityType",
    "sex",
    "lifeStage",
    "preparations",
    "associatedMedia",
    "occurrenceRemarks",
    "organismID",
    "institutionCode",
    "collectionCode",
    "basisOfRecord",
    "taxonID",
    "scientificName",
    "kingdom",
    "phylum",
    "class",
    "order",
    "family",
    "genus",
    "specificEpithet",
    "infraspecificEpithet",
    "taxonRank",
    "vernacularName",
]
