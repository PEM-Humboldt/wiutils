"""
Field mapping between Wildlife Insights and the Darwin Core standard.
"""
event = field_map = {
    "deployment_id": "eventID",
    "project_id": "parentEventID",
    "event_name": "eventRemarks",
    "feature_type": "locationRemarks",
    "latitude": "decimalLatitude",
    "longitude": "decimalLongitude"
}

record = {
    "deployment_id": "eventID",
    "project_id": "parentEventID",
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
    "class": "class",
    "order": "order",
    "family": "family",
    "genus": "genus",
    "species": "specificEpithet",
    "common_name": "vernacularName",
    "license": "accessRights",
    "location": "associatedMedia"
}
