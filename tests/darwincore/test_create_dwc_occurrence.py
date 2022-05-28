# """
# Test cases for the wiutils.summarizing.create_dwc_records function.
# """
# import numpy as np
# import pandas as pd
# import pytest
#
# from wiutils.darwincore import create_dwc_records
#
#
# @pytest.fixture(scope="function")
# def images():
#     return pd.DataFrame(
#         {
#             "deployment_id": ["001", "001", "001", "002", "001"],
#             "image_id": ["bc6534f0", "003cb8eb", "a19bbd16", "740e09f5", "e09axa3q"],
#             "filename": [
#                 "1116011.JPG",
#                 "1225022.JPG",
#                 "1215016.JPG",
#                 "0113071.JPG",
#                 "1215017.JPG",
#             ],
#             "location": [
#                 "gs:/bc6.JPG",
#                 "gs:/bc5.JPG",
#                 "gs:/a19.JPG",
#                 "gs:/740.JPG",
#                 "gs:/e09.JPG",
#             ],
#             "is_blank": [0, 1, 0, 0, 0],
#             "identified_by": [
#                 "John Doe",
#                 "Jane Doe",
#                 "Jane Doe",
#                 "John Doe",
#                 "Jane Doe",
#             ],
#             "wi_taxon_id": ["f2efdae9", "f1856211", "32c0147f", "523439f4", "32c0147f"],
#             "class": ["No CV Result", np.nan, "Mammalia", "Mammalia", "Mammalia"],
#             "order": ["No CV Result", np.nan, "Rodentia", "Rodentia", "Rodentia"],
#             "family": [
#                 "No CV Result",
#                 np.nan,
#                 "Cuniculidae",
#                 "Cricetidae",
#                 "Cuniculidae",
#             ],
#             "genus": ["No CV Result", np.nan, "Cuniculus", np.nan, "Cuniculus"],
#             "species": ["No CV Result", np.nan, "paca nelsoni", np.nan, "paca nelsoni"],
#             "common_name": [
#                 "Blank",
#                 "Blank",
#                 "Spotted Paca",
#                 "Cricetidae Family",
#                 "Spotted Paca",
#             ],
#             "uncertainty": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "timestamp": [
#                 "2020-12-13 09:04:50",
#                 "2020-12-25 10:23:12",
#                 "2021-01-12 09:59:02",
#                 "2020-11-17 01:12:57",
#                 "2021-01-12 09:59:03",
#             ],
#             "age": [np.nan, np.nan, "adult", np.nan, "adult"],
#             "sex": [np.nan, np.nan, "unknown", "male", "unknown"],
#             "animal_recognizable": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "individual_id": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "number_of_objects": [1, 1, 2, 1, 2],
#             "individual_animal_notes": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "highlighted": [False, False, True, False, False],
#             "markings": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "cv_confidence": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "license": ["CC-BY-NC", "CC-BY-NC", "CC-BY-NC", "CC-BY-NC", "CC-BY-NC"],
#         }
#     )
#
#
# @pytest.fixture(scope="function")
# def deployments():
#     return pd.DataFrame(
#         {
#             "placename": ["90210", "90210"],
#             "deployment_id": ["001", "002"],
#             "recorded_by": ["Joe Bloggs", np.nan],
#         }
#     )
#
#
# def test_defaults(deployments, images):
#     result = create_dwc_records(images, deployments)
#     expected = pd.DataFrame(
#         {
#             "occurrenceID": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "parentEventID": ["90210", "90210", "90210", "90210", "90210"],
#             "eventID": ["001", "001", "001", "002", "001"],
#             "basisOfRecord": [
#                 "MachineObservation",
#                 "MachineObservation",
#                 "MachineObservation",
#                 "MachineObservation",
#                 "MachineObservation",
#             ],
#             "institutionCode": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "collectionCode": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "catalogNumber": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "occurrenceRemarks": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "recordNumber": [
#                 "bc6534f0",
#                 "003cb8eb",
#                 "a19bbd16",
#                 "740e09f5",
#                 "e09axa3q",
#             ],
#             "recordedBy": [
#                 "Joe Bloggs",
#                 "Joe Bloggs",
#                 "Joe Bloggs",
#                 np.nan,
#                 "Joe Bloggs",
#             ],
#             "organismID": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "organismQuantity": [np.nan, np.nan, 2, 1, 2],
#             "organismQuantityType": [
#                 np.nan,
#                 np.nan,
#                 "individuals",
#                 "individuals",
#                 "individuals",
#             ],
#             "sex": [np.nan, np.nan, "unknown", "male", "unknown"],
#             "lifeStage": [np.nan, np.nan, "adult", np.nan, "adult"],
#             "preparations": [
#                 "photograph",
#                 "photograph",
#                 "photograph",
#                 "photograph",
#                 "photograph",
#             ],
#             "eventDate": [
#                 "2020-12-13",
#                 "2020-12-25",
#                 "2021-01-12",
#                 "2020-11-17",
#                 "2021-01-12",
#             ],
#             "eventTime": ["09:04:50", "10:23:12", "09:59:02", "01:12:57", "09:59:03"],
#             "identifiedBy": [
#                 "John Doe",
#                 "Jane Doe",
#                 "Jane Doe",
#                 "John Doe",
#                 "Jane Doe",
#             ],
#             "dateIdentified": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "identificationRemarks": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "scientificNameID": [
#                 "f2efdae9",
#                 "f1856211",
#                 "32c0147f",
#                 "523439f4",
#                 "32c0147f",
#             ],
#             "identificationQualifier": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "scientificName": [
#                 np.nan,
#                 np.nan,
#                 "Cuniculus paca nelsoni",
#                 "Cricetidae",
#                 "Cuniculus paca nelsoni",
#             ],
#             "kingdom": [np.nan, np.nan, "Animalia", "Animalia", "Animalia"],
#             "phylum": [np.nan, np.nan, "Chordata", "Chordata", "Chordata"],
#             "class": [np.nan, np.nan, "Mammalia", "Mammalia", "Mammalia"],
#             "order": [np.nan, np.nan, "Rodentia", "Rodentia", "Rodentia"],
#             "family": [np.nan, np.nan, "Cuniculidae", "Cricetidae", "Cuniculidae"],
#             "genus": [np.nan, np.nan, "Cuniculus", np.nan, "Cuniculus"],
#             "specificEpithet": [np.nan, np.nan, "paca", np.nan, "paca"],
#             "infraspecificEpithet": [np.nan, np.nan, "nelsoni", np.nan, "nelsoni"],
#             "taxonRank": [np.nan, np.nan, "subspecies", "family", "subspecies"],
#             "scientificNameAuthorship": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "vernacularName": [
#                 np.nan,
#                 np.nan,
#                 "Spotted Paca",
#                 "Cricetidae Family",
#                 "Spotted Paca",
#             ],
#             "accessRights": [
#                 "CC-BY-NC",
#                 "CC-BY-NC",
#                 "CC-BY-NC",
#                 "CC-BY-NC",
#                 "CC-BY-NC",
#             ],
#             "associatedMedia": [
#                 "gs:/bc6.JPG",
#                 "gs:/bc5.JPG",
#                 "gs:/a19.JPG",
#                 "gs:/740.JPG",
#                 "gs:/e09.JPG",
#             ],
#         }
#     )
#     pd.testing.assert_frame_equal(result, expected)
#
#
# def test_remove_empty_optionals(deployments, images):
#     result = create_dwc_records(images, deployments, remove_empty_optionals=True)
#     expected = pd.DataFrame(
#         {
#             "occurrenceID": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "parentEventID": ["90210", "90210", "90210", "90210", "90210"],
#             "eventID": ["001", "001", "001", "002", "001"],
#             "basisOfRecord": [
#                 "MachineObservation",
#                 "MachineObservation",
#                 "MachineObservation",
#                 "MachineObservation",
#                 "MachineObservation",
#             ],
#             "institutionCode": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "collectionCode": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "catalogNumber": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "recordNumber": [
#                 "bc6534f0",
#                 "003cb8eb",
#                 "a19bbd16",
#                 "740e09f5",
#                 "e09axa3q",
#             ],
#             "recordedBy": [
#                 "Joe Bloggs",
#                 "Joe Bloggs",
#                 "Joe Bloggs",
#                 np.nan,
#                 "Joe Bloggs",
#             ],
#             "organismQuantity": [np.nan, np.nan, 2, 1, 2],
#             "organismQuantityType": [
#                 np.nan,
#                 np.nan,
#                 "individuals",
#                 "individuals",
#                 "individuals",
#             ],
#             "sex": [np.nan, np.nan, "unknown", "male", "unknown"],
#             "lifeStage": [np.nan, np.nan, "adult", np.nan, "adult"],
#             "preparations": [
#                 "photograph",
#                 "photograph",
#                 "photograph",
#                 "photograph",
#                 "photograph",
#             ],
#             "eventDate": [
#                 "2020-12-13",
#                 "2020-12-25",
#                 "2021-01-12",
#                 "2020-11-17",
#                 "2021-01-12",
#             ],
#             "eventTime": ["09:04:50", "10:23:12", "09:59:02", "01:12:57", "09:59:03"],
#             "identifiedBy": [
#                 "John Doe",
#                 "Jane Doe",
#                 "Jane Doe",
#                 "John Doe",
#                 "Jane Doe",
#             ],
#             "dateIdentified": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "scientificNameID": [
#                 "f2efdae9",
#                 "f1856211",
#                 "32c0147f",
#                 "523439f4",
#                 "32c0147f",
#             ],
#             "scientificName": [
#                 np.nan,
#                 np.nan,
#                 "Cuniculus paca nelsoni",
#                 "Cricetidae",
#                 "Cuniculus paca nelsoni",
#             ],
#             "kingdom": [np.nan, np.nan, "Animalia", "Animalia", "Animalia"],
#             "phylum": [np.nan, np.nan, "Chordata", "Chordata", "Chordata"],
#             "class": [np.nan, np.nan, "Mammalia", "Mammalia", "Mammalia"],
#             "order": [np.nan, np.nan, "Rodentia", "Rodentia", "Rodentia"],
#             "family": [np.nan, np.nan, "Cuniculidae", "Cricetidae", "Cuniculidae"],
#             "genus": [np.nan, np.nan, "Cuniculus", np.nan, "Cuniculus"],
#             "specificEpithet": [np.nan, np.nan, "paca", np.nan, "paca"],
#             "infraspecificEpithet": [np.nan, np.nan, "nelsoni", np.nan, "nelsoni"],
#             "taxonRank": [np.nan, np.nan, "subspecies", "family", "subspecies"],
#             "vernacularName": [
#                 np.nan,
#                 np.nan,
#                 "Spotted Paca",
#                 "Cricetidae Family",
#                 "Spotted Paca",
#             ],
#             "accessRights": [
#                 "CC-BY-NC",
#                 "CC-BY-NC",
#                 "CC-BY-NC",
#                 "CC-BY-NC",
#                 "CC-BY-NC",
#             ],
#             "associatedMedia": [
#                 "gs:/bc6.JPG",
#                 "gs:/bc5.JPG",
#                 "gs:/a19.JPG",
#                 "gs:/740.JPG",
#                 "gs:/e09.JPG",
#             ],
#         }
#     )
#     pd.testing.assert_frame_equal(result, expected)
#
#
# def test_language_es(deployments, images):
#     result = create_dwc_records(images, deployments, language="es")
#     expected = pd.DataFrame(
#         {
#             "occurrenceID": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "parentEventID": ["90210", "90210", "90210", "90210", "90210"],
#             "eventID": ["001", "001", "001", "002", "001"],
#             "basisOfRecord": [
#                 "Observación con máquina",
#                 "Observación con máquina",
#                 "Observación con máquina",
#                 "Observación con máquina",
#                 "Observación con máquina",
#             ],
#             "institutionCode": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "collectionCode": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "catalogNumber": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "occurrenceRemarks": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "recordNumber": [
#                 "bc6534f0",
#                 "003cb8eb",
#                 "a19bbd16",
#                 "740e09f5",
#                 "e09axa3q",
#             ],
#             "recordedBy": [
#                 "Joe Bloggs",
#                 "Joe Bloggs",
#                 "Joe Bloggs",
#                 np.nan,
#                 "Joe Bloggs",
#             ],
#             "organismID": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "organismQuantity": [np.nan, np.nan, 2, 1, 2],
#             "organismQuantityType": [
#                 np.nan,
#                 np.nan,
#                 "individuos",
#                 "individuos",
#                 "individuos",
#             ],
#             "sex": [np.nan, np.nan, "desconocido", "macho", "desconocido"],
#             "lifeStage": [np.nan, np.nan, "adulto", np.nan, "adulto"],
#             "preparations": [
#                 "fotografía",
#                 "fotografía",
#                 "fotografía",
#                 "fotografía",
#                 "fotografía",
#             ],
#             "eventDate": [
#                 "2020-12-13",
#                 "2020-12-25",
#                 "2021-01-12",
#                 "2020-11-17",
#                 "2021-01-12",
#             ],
#             "eventTime": ["09:04:50", "10:23:12", "09:59:02", "01:12:57", "09:59:03"],
#             "identifiedBy": [
#                 "John Doe",
#                 "Jane Doe",
#                 "Jane Doe",
#                 "John Doe",
#                 "Jane Doe",
#             ],
#             "dateIdentified": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "identificationRemarks": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "scientificNameID": [
#                 "f2efdae9",
#                 "f1856211",
#                 "32c0147f",
#                 "523439f4",
#                 "32c0147f",
#             ],
#             "identificationQualifier": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "scientificName": [
#                 np.nan,
#                 np.nan,
#                 "Cuniculus paca nelsoni",
#                 "Cricetidae",
#                 "Cuniculus paca nelsoni",
#             ],
#             "kingdom": [np.nan, np.nan, "Animalia", "Animalia", "Animalia"],
#             "phylum": [np.nan, np.nan, "Chordata", "Chordata", "Chordata"],
#             "class": [np.nan, np.nan, "Mammalia", "Mammalia", "Mammalia"],
#             "order": [np.nan, np.nan, "Rodentia", "Rodentia", "Rodentia"],
#             "family": [np.nan, np.nan, "Cuniculidae", "Cricetidae", "Cuniculidae"],
#             "genus": [np.nan, np.nan, "Cuniculus", np.nan, "Cuniculus"],
#             "specificEpithet": [np.nan, np.nan, "paca", np.nan, "paca"],
#             "infraspecificEpithet": [np.nan, np.nan, "nelsoni", np.nan, "nelsoni"],
#             "taxonRank": [np.nan, np.nan, "subespecie", "familia", "subespecie"],
#             "scientificNameAuthorship": [np.nan, np.nan, np.nan, np.nan, np.nan],
#             "vernacularName": [
#                 np.nan,
#                 np.nan,
#                 "Spotted Paca",
#                 "Cricetidae Family",
#                 "Spotted Paca",
#             ],
#             "accessRights": [
#                 "CC-BY-NC",
#                 "CC-BY-NC",
#                 "CC-BY-NC",
#                 "CC-BY-NC",
#                 "CC-BY-NC",
#             ],
#             "associatedMedia": [
#                 "gs:/bc6.JPG",
#                 "gs:/bc5.JPG",
#                 "gs:/a19.JPG",
#                 "gs:/740.JPG",
#                 "gs:/e09.JPG",
#             ],
#         }
#     )
#     pd.testing.assert_frame_equal(result, expected)
#
#
# def test_intact_input(images, deployments):
#     images_original = images.copy()
#     deployments_original = deployments.copy()
#     create_dwc_records(images, deployments)
#     pd.testing.assert_frame_equal(images_original, images)
#     pd.testing.assert_frame_equal(deployments_original, deployments)
