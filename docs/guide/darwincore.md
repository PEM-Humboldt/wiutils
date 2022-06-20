# Darwin Core

## Overview
Darwin Core functions allow you to convert tables from Wildlife Insights format to the Darwin Core Standard. This is useful to publish information from Wildlife Insights projects to different biodiversity information centers (*e.g.* [GBIF](https://www.gbif.org/)).

Here is a quick overview of the different Darwin Core functions and their description:

| Function                                                                          | Description                                                                                                                                     |
|-----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| [`create_dwc_archive`](/reference/#wiutils.darwincore.create_dwc_archive)         | Creates a Darwin Core Archive consisting of four different cores and extensions: Event, Occurrence, Measurement or Facts and Simple Multimedia. |
| [`create_dwc_event`](/reference/#wiutils.darwincore.create_dwc_event)             | Creates a Darwin Core Event dataframe from deployments and projects information.                                                                |
| [`create_dwc_measurement`](/reference/#wiutils.darwincore.create_dwc_measurement) | Creates a Darwin Core Measurement or Facts dataframe from cameras and deployments information.                                                  |
| [`create_dwc_multimedia`](/reference/#wiutils.darwincore.create_dwc_multimedia)   | Creates a Darwin Core Simple Multimedia dataframe from images and deployments information.                                                      |
| [`create_dwc_occurrence`](/reference/#wiutils.darwincore.create_dwc_occurrence)   | Creates a Darwin Core Occurrence dataframe from images, deployments and projects information                                                    |

!!! note

    The Darwin Core functions only map available information from Wildlife Insights to Darwin Core Standard terms across four different cores/extensions. However, it is possible that you might want to add more terms and complement this information before publishing it (*e.g.* adding geographic or taxonomic details to the events and occurrences). [`regi0`](https://github.com/PEM-Humboldt/regi0), another Python package, might be useful for this.

For every snippet of code showed here, we will assume you have already run the following code:
```python
import wiutils

cameras, deployments, images, projects = wiutils.load_demo("cajambre")
```

## Creating the Event Core

The [Darwin Core Event](https://rs.gbif.org/core/dwc_event_2022-02-02.xml) is *the category of information pertaining to an action that occurs at some location during some time*. In this context, events can be thought of as deployments.

Here is a map between Wildlife Insights fields from different tables (source) and Darwin Core Event terms. Some terms have constant values or are computed using existing information:

| source (WI) | field (WI)                 | term (DwC)       | constant    | comments                                                          |
|-------------|----------------------------|------------------|-------------|-------------------------------------------------------------------|
| deployments | deployment_id              | eventID          |             |                                                                   |
| deployments | placename                  | parentEventID    |             |                                                                   |
| -           | -                          | samplingProtocol | camera trap |                                                                   |
| -           | -                          | sampleSizeValue  |           1 |                                                                   |
| -           | -                          | sampleSizeUnit   | camera      |                                                                   |
| -           | -                          | samplingEffort   |             | Delta (in days) between end_date and start_date +  "trap-nights". |
| deployments | start_date, end_date       | eventDate        |             | Concatenation of both fields using "/".                           |
| deployments | event_description          | eventRemarks     |             |                                                                   |
| projects    | country_code               | countryCode      |             | Converted from ISO 3166-1 alpha-3 to ISO 3166-1 alpha-2.          |
| deployments | feature_type               | locationRemarks  |             |                                                                   |
| deployments | latitude                   | decimalLatitude  |             |                                                                   |
| deployments | longitude                  | decimalLongitude |             |                                                                   |
| -           | -                          | geodeticDatum    | WGS84       |                                                                   |
| projects    | project_admin_organization | institutionCode  |             |                                                                   |


The `create_dwc_event` function allows you to create a dataframe with this information. You'll need to pass both the deployments and projects dataframes:
```pycon
>>> event =  wiutils.create_dwc_event(deployments, projects)
>>> event

        eventID parentEventID  ... geodeticDatum     institutionCode
0   CTCAJ103744       CTCAJ10  ...         WGS84  Instituto Humboldt
1   CTCAJ033779       CTCAJ03  ...         WGS84  Instituto Humboldt
2   CTCAJ163747       CTCAJ16  ...         WGS84  Instituto Humboldt
3   CTCAJ193741       CTCAJ19  ...         WGS84  Instituto Humboldt
4   CTCAJ083775       CTCAJ08  ...         WGS84  Instituto Humboldt
5   CTCAJ123777       CTCAJ12  ...         WGS84  Instituto Humboldt
6   CTCAJ143748       CTCAJ14  ...         WGS84  Instituto Humboldt
7   CTCAJ133746       CTCAJ13  ...         WGS84  Instituto Humboldt
8   CTCAJ073781       CTCAJ07  ...         WGS84  Instituto Humboldt
9   CTCAJ183778       CTCAJ18  ...         WGS84  Instituto Humboldt
10  CTCAJ093776       CTCAJ09  ...         WGS84  Instituto Humboldt
11  CTCAJ113742       CTCAJ11  ...         WGS84  Instituto Humboldt
12  CTCAJ153745       CTCAJ15  ...         WGS84  Instituto Humboldt
13  CTCAJ043772       CTCAJ04  ...         WGS84  Instituto Humboldt
14  CTCAJ063750       CTCAJ06  ...         WGS84  Instituto Humboldt
15  CTCAJ023749       CTCAJ02  ...         WGS84  Instituto Humboldt
16  CTCAJ053782       CTCAJ05  ...         WGS84  Instituto Humboldt
17  CTCAJ013743       CTCAJ01  ...         WGS84  Instituto Humboldt
18  CTCAJ143747       CTCAJ14  ...         WGS84  Instituto Humboldt

[19 rows x 14 columns]

>>> event.columns

Index(['eventID', 'parentEventID', 'samplingProtocol', 'sampleSizeValue',
       'sampleSizeUnit', 'samplingEffort', 'eventDate', 'eventRemarks',
       'countryCode', 'locationRemarks', 'decimalLatitude', 'decimalLongitude',
       'geodeticDatum', 'institutionCode'],
      dtype='object')
```

You can then save the file to different formats:
```pycon
>>> event.to_csv("Event.csv", index=False)  # csv
>>> event.to_csv("Event.txt", index=False, header=None, sep=" ")  # txt
>>> event.to_excel("Event.xlsx", index=False)  # xlsx
```


## Creating the Occurrence Core / Extension

The [Darwin Core Occurrence](https://rs.gbif.org/core/dwc_occurrence_2022-02-02.xml) is *the category of information pertaining to the existence of an Organism at a particular place at a particular time*. In this context, occurrences can be thought of as biodiversity records (*i.e.* non-duplicate images with identified wildlife).

Here is a map between Wildlife Insights fields from different tables (source) and Darwin Core Occurrence terms. Some terms have constant values or are computed using existing information:

| source (WI)         | field (WI)                 | term (DwC)            | constant           | comments                                                                                                                                                                                                             |
|---------------------|----------------------------|-----------------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| images, deployments | deployment_id              | eventID               |                    |                                                                                                                                                                                                                      |
| deployments         | placename                  | parentEventID         |                    |                                                                                                                                                                                                                      |
| images              | timestamp                  | eventDate             |                    | Extracted date from timestamp                                                                                                                                                                                        |
| images              | timestamp                  | eventTime             |                    | Extracted time from timestamp                                                                                                                                                                                        |
| images              | identified_by              | identifiedBy          |                    |                                                                                                                                                                                                                      |
| images              | uncertainty                | identificationRemarks |                    |                                                                                                                                                                                                                      |
| images              | image_id                   | recordNumber          |                    |                                                                                                                                                                                                                      |
| deployments         | recorded_by                | recordedBy            |                    |                                                                                                                                                                                                                      |
| images              | number_of_objects          | organismQuantity      |                    |                                                                                                                                                                                                                      |
| -                   | -                          | organismQuantityType  | individual(s)      |                                                                                                                                                                                                                      |
| images              | sex                        | sex                   |                    |                                                                                                                                                                                                                      |
| images              | age                        | lifeStage             |                    |                                                                                                                                                                                                                      |
| -                   | -                          | preparations          | photograph         |                                                                                                                                                                                                                      |
| images              | location                   | associatedMedia       |                    | Because one occurrence can have multiple associated images, this field is a pipe separated list of those images location. Also, image locations are converted from Google Cloud Storage URI (gs://) to an HTTPS URL. |
| images              | individual_animal_notes    | occurrenceRemarks     |                    |                                                                                                                                                                                                                      |
| images              | individual_id              | organismID            |                    |                                                                                                                                                                                                                      |
| projects            | project_admin_organization | institutionCode       |                    |                                                                                                                                                                                                                      |
| -                   | -                          | basisOfRecord         | MachineObservation |                                                                                                                                                                                                                      |
| images              | wi_taxon_id                | taxonID               |                    |                                                                                                                                                                                                                      |
| -                   | -                          | scientificName        |                    | Computed using wiutils.get_lowest_taxon.                                                                                                                                                                             |
| -                   | -                          | kingdom               | Animalia           |                                                                                                                                                                                                                      |
| -                   | -                          | phylum                | Chordata           |                                                                                                                                                                                                                      |
| images              | class                      | class                 |                    |                                                                                                                                                                                                                      |
| images              | order                      | order                 |                    |                                                                                                                                                                                                                      |
| images              | family                     | family                |                    |                                                                                                                                                                                                                      |
| images              | genus                      | genus                 |                    |                                                                                                                                                                                                                      |
| images              | species                    | specificEpithet       |                    | Corresponds to the first word in the species field.                                                                                                                                                                  |
| images              | species                    | infraspecificEpithet  |                    | Corresponds to the second word in the species field.                                                                                                                                                                 |
| -                   | -                          | taxonRank             |                    | Computed using wiutils.get_lowest_taxon.                                                                                                                                                                             |
| images              | common_name                | vernacularName        |                    |                                                                                                                                                                                                                      |

The `create_dwc_occurrence` function allows you to create a dataframe with this information. The `create_dwc_event` allow you to create a dataframe with this information. You'll need to pass the images, deployments and projects dataframes. Because occurrences only consider non-duplicate images, this function allows you to pass an arbitrary time window to remove duplicate images (using the `remove_duplicates` function under the hood) with the `remove_duplicate_kws` parameter. Here is an example to create the Occurrence Core / Extension using a one-hour window:
```pycon
>>> occurrence = wiutils.create_dwc_occurrence(images, deployments, projects, remove_duplicate_kws={"interval": 1, "unit": "hours"})
>>> occurrence

         eventID parentEventID  ... taxonRank                vernacularName
0    CTCAJ013743       CTCAJ01  ...   species                         Human
1    CTCAJ013743       CTCAJ01  ...   species                 Great Tinamou
2    CTCAJ013743       CTCAJ01  ...   species                         Human
3    CTCAJ013743       CTCAJ01  ...   species              Tome's Spiny Rat
4    CTCAJ013743       CTCAJ01  ...   species                 Great Tinamou
..           ...           ...  ...       ...                           ...
567  CTCAJ193741       CTCAJ19  ...   species                         Tayra
568  CTCAJ193741       CTCAJ19  ...    family                 Possum Family
569  CTCAJ193741       CTCAJ19  ...    family                 Possum Family
570  CTCAJ193741       CTCAJ19  ...   species  Central American Red Brocket
571  CTCAJ193741       CTCAJ19  ...    family                 Possum Family

[572 rows x 30 columns]

>>> occurrence.columns

Index(['eventID', 'parentEventID', 'eventDate', 'eventTime', 'identifiedBy',
       'identificationRemarks', 'recordNumber', 'recordedBy',
       'organismQuantity', 'organismQuantityType', 'sex', 'lifeStage',
       'preparations', 'associatedMedia', 'occurrenceRemarks', 'organismID',
       'institutionCode', 'basisOfRecord', 'taxonID', 'scientificName',
       'kingdom', 'phylum', 'class', 'order', 'family', 'genus',
       'specificEpithet', 'infraspecificEpithet', 'taxonRank',
       'vernacularName'],
      dtype='object')
```

You can then save the file to different formats:
```pycon
>>> occurrence.to_csv("Occurrence.csv", index=False)  # csv
>>> occurrence.to_csv("Occurrence.txt", index=False, header=None, sep=" ")  # txt
>>> occurrence.to_excel("Occurrence.xlsx", index=False)  # xlsx
```
## Creating the Measurement or Facts Extension

The [Darwin Core Simple Measurement or Facts](https://rs.gbif.org/extension/dwc/measurements_or_facts_2022-02-02.xml) is a *support for measurements or facts, allowing links to any type of Core*. In this context, it has relevant information about cameras and deployments and is linked to the Event Core.

Here is a map between Wildlife Insights fields from different tables (source) and four Darwin Core Measurement or Facts terms. The `measurementType` and `measurementUnit` terms have constant values:

| **term (DwC)**  | measurementType       | measurementValue   | measurementUnit | measurementRemarks         |
|-----------------|-----------------------|--------------------|-----------------|----------------------------|
| **source (WI)** | **constant**          | **field (WI)**     | **constant**    | **field (WI)**             |
| cameras         | camera make           | make               |                 |                            |
| cameras         | camera serial number  | serial_number      |                 |                            |
| cameras         | camera year purchased | year_purchased     |                 |                            |
| deployments     | bait type             | bait_type          |                 | bait_description           |
| deployments     | quiet period          | quiet_period       | seconds         |                            |
| deployments     | camera functioning    | camera_functioning |                 |                            |
| deployments     | sensor height         | sensor_height      |                 | height_other               |
| deployments     | sensor orientation    | sensor orientation |                 | orientation_other          |
| deployments     | plot treatment        | plot_treatment     |                 | plot_treatment_description |
| deployments     | detection distance    | detection_distance | meters          |                            |

The `create_dwc_measurement` function allows you to create a dataframe with this information. You'll need to pass both the deployments and cameras dataframes:
```pycon
>>> measurement = wiutils.create_dwc_measurement(deployments, cameras)

         eventID     measurementType  ... measurementUnit measurementRemarks
0    CTCAJ103744         camera make  ...             NaN                NaN
1    CTCAJ033779         camera make  ...             NaN                NaN
2    CTCAJ163747         camera make  ...             NaN                NaN
3    CTCAJ193741         camera make  ...             NaN                NaN
4    CTCAJ083775         camera make  ...             NaN                NaN
..           ...                 ...  ...             ...                ...
109  CTCAJ063750  sensor orientation  ...             NaN                NaN
110  CTCAJ023749  sensor orientation  ...             NaN                NaN
111  CTCAJ053782  sensor orientation  ...             NaN                NaN
112  CTCAJ013743  sensor orientation  ...             NaN                NaN
113  CTCAJ143747  sensor orientation  ...             NaN                NaN

[114 rows x 5 columns]

Index(['eventID', 'measurementType', 'measurementValue', 'measurementUnit',
       'measurementRemarks'],
      dtype='object')
```

Notice that there is an extra column (`eventID`) which links the measurements to their respective camera/deployment. Even though this term is not on the [extension description]((https://rs.gbif.org/extension/dwc/measurements_or_facts_2022-02-02.xml), it is used to link to the Event Core when using tools such as the [Integrated Publishing Toolkit (IPT)](https://www.gbif.org/ipt).

```pycon
>>> measurement.to_csv("MeasurementOrFacts.csv", index=False)  # csv
>>> measurement.to_csv("MeasurementOrFacts.txt", index=False, header=None, sep=" ")  # txt
>>> measurement.to_excel("MeasurementOrFacts.xlsx", index=False)  # xlsx
```

## Creating the Simple Multimedia Extension

The [Darwin Core Simple Multimedia](https://rs.gbif.org/extension/gbif/1.0/multimedia.xml) is a *simple extension for exchanging metadata about multimedia resources, in particular links to image, video and audio files*. In this context, it has relevant information about all the images from a project, including those without identified wildlife.

Here is a map between Wildlife Insights fields from different tables (source) and Darwin Core Simple Multimedia terms. Some terms have constant values or are computed using existing information:

| source (WI)         | field (WI)    | term (DwC)  | constant          | comments                                                                                                     |
|---------------------|---------------|-------------|-------------------|--------------------------------------------------------------------------------------------------------------|
| images, deployments | deployment_id | eventID     |                   |                                                                                                              |
| -                   | -             | type        | Image             |                                                                                                              |
| -                   | -             | format      | image/jpeg        |                                                                                                              |
| images              | image_id      | identifier  |                   |                                                                                                              |
| images              | location      | references  |                   | Image location is converted from Google Cloud Storage URI (gs://) to an HTTP URL.                            |
| images              | -             | title       |                   | Computed using wiutils.get_lowest_taxon. For blank or unidentified images, title is 'Blank or unidentified'. |
| images              | timestamp     | created     |                   |                                                                                                              |
| deployments         | recorded_by   | creator     |                   |                                                                                                              |
| images              | identified_by | contributor |                   |                                                                                                              |
| -                   | -             | publisher   | Wildlife Insights |                                                                                                              |
| images              | license       | license     |                   |                                                                                                              |

The `create_dwc_multimedia` function allows you to create a dataframe with this information. You'll need to pass both the images and deployments dataframes:
```pycon
>>> multimedia = wiutils.create_dwc_multimedia(images, deployments)
>>> multimedia

          eventID   type  ...          publisher   license
0     CTCAJ013743  Image  ...  Wildlife Insights  CC-BY-NC
1     CTCAJ013743  Image  ...  Wildlife Insights  CC-BY-NC
2     CTCAJ013743  Image  ...  Wildlife Insights  CC-BY-NC
3     CTCAJ013743  Image  ...  Wildlife Insights  CC-BY-NC
4     CTCAJ013743  Image  ...  Wildlife Insights  CC-BY-NC
           ...    ...  ...                ...       ...
5248  CTCAJ193741  Image  ...  Wildlife Insights  CC-BY-NC
5249  CTCAJ193741  Image  ...  Wildlife Insights  CC-BY-NC
5250  CTCAJ193741  Image  ...  Wildlife Insights  CC-BY-NC
5251  CTCAJ193741  Image  ...  Wildlife Insights  CC-BY-NC
5252  CTCAJ193741  Image  ...  Wildlife Insights  CC-BY-NC

[5253 rows x 11 columns]

>>> multimedia.columns

Index(['eventID', 'type', 'format', 'identifier', 'references', 'title',
       'created', 'creator', 'contributor', 'publisher', 'license'],
      dtype='object')
```

```pycon
>>> multimedia.to_csv("SimpleMultimedia.csv", index=False)  # csv
>>> multimedia.to_csv("SimpleMultimedia.txt", index=False, header=None, sep=" ")  # txt
>>> multimedia.to_excel("SimpleMultimedia.xlsx", index=False)  # xlsx
```

## Creating the Darwin Core Archive

The Darwin Core Archive is a structured collection of text files containing different cores and extensions (see more about this on https://www.gbif.org/darwin-core). In this context, we refer to the Darwin Core Archive as the four cores / extensions that result from Wildlife Insights information:

- Darwin Core Event
- Darwin Core Occurrence
- Darwin Core Simple Multimedia
- Darwin Core Measurement or Facts

By having these four files, you can use tools such as the [Integrated Publishing Toolkit (IPT)](https://www.gbif.org/ipt) to publish the project's information.

The `create_dwc_archive` function uses the other four Darwin Core functions described above to conveniently create these four dataframes at once. Notice that this function also has the `remove_duplicate_kws` parameter:
```pycon
>>> event, occurrence, measurement, multimedia = wiutils.create_dwc_archive(cameras, deployments, images, projects, remove_duplicate_kws={"interval": 1, "unit": "hours"})
```
