
# Releasing `dplace-data`

## Check the data

The consistency and completeness of the data must be checked running
```
dplace check
```
Any `ERROR`s must be fixed and `WARNING`s inspected closely.


## Update data from Glottolog

If a new Glottolog version has become available since the last release, the Glottolog
data included in `dplace-data` (language family trees and [languoid metadata](csv/glottolog.csv)) must be updated. This is done running the command
```
dplace glottolog PATH/TO/GLOTTOLOG/REPOS YEAR VERSION
```


## Assign societies to TDWG regions

If new societies have been added (or the geo-coordinates of existing societies have
been updated), the [assignment of TDWG regions](geo/societies_tdwg.json) has to be
updated as well. To do this, run
```
dplace tdwg
```

## Update the list of sources

We make the sources of our data transparent by extracting the information from the
index files into [`SOURCES.md`](SOURCES.md). This is done running
```
dplace readme
```


## Create a release

Create a new release by navigating to https://github.com/D-PLACE/dplace-data/releases
and pushing "Draft a new release". Choose a release tag prefixed with `v` to make 
sure the release will be picked up by ZENODO.

Allow ZENODO some time to process the release, then search for the release on
ZENODO, copy the corresponding DOI badge and paste it at the end of the release
description.


## Create derived releases

- Create a corresponding release of D-PLACE/dplace-cldf
- Release the new data in the clld app

