"""
Field to term mapping between Wildlife Insights and the Darwin Core
standard.
"""
event = {
    "deployment_id": "eventID",
    "placename": "parentEventID",
    "event_description": "eventRemarks",
    "country_code": "countryCode",
    "feature_type": "locationRemarks",
    "latitude": "decimalLatitude",
    "longitude": "decimalLongitude",
}

multimedia = {
    "image_id": "identifier",
    "timestamp": "created",
    "recorded_by": "creator",
    "identified_by": "contributor",
    "license": "license",
}

occurrence = {
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
    "class": "class",
    "order": "order",
    "family": "family",
    "genus": "genus",
    "common_name": "vernacularName",
    "license": "accessRights",
    "location": "associatedMedia",
}
