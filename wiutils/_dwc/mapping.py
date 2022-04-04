"""
Field mapping between Wildlife Insights and the Darwin Core standard.
"""
events = {
    "deployment_id": "eventID",
    "placename": "parentEventID",
    "event_name": "eventRemarks",
    "feature_type": "locationRemarks",
    "latitude": "decimalLatitude",
    "longitude": "decimalLongitude",
}

records = {
    "placename": "parentEventID",
    "deployment_id": "eventID",
    "individual_animal_notes": "occurrenceRemarks",
    "image_id": "recordNumber",
    "recorded_by": "recordedBy",
    "individual_id": "organismID",
    "number_of_objects": "organismQuantity",
    "sex": "sex",
    "age": "lifeStage",
    "identified_by": "identifiedBy",
    "uncertainty": "identificationRemarks",
    "wi_taxon_id": "scientificNameID",
    "scientific_name": "scientificName",
    "class": "class",
    "order": "order",
    "family": "family",
    "genus": "genus",
    "common_name": "vernacularName",
    "license": "accessRights",
    "location": "associatedMedia",
}
