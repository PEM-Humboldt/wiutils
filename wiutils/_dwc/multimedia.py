"""
Mapping from WI fields to DwC terms, constant values and term order for
the Darwin Core Simple Multimedia dataframe creation.
"""
constants = {
    "type": "Image",
    "format": "image/jpeg",
    "publisher": "Wildlife Insights",
}

mapping = {
    "identifier": "image_id",
    "references": "location",
    "created": "timestamp",
    "creator": "recorded_by",
    "contributor": "identified_by",
    "license": "license",
}

order = [
    "type",
    "format",
    "identifier",
    "references",
    "title",
    "created",
    "creator",
    "contributor",
    "publisher",
    "license",
]
