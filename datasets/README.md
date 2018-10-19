## Datasets

Variables and associated values coded for D-PLACE societies are organized into datasets,
according to their source.

Each dataset is identified by a short textual ID, e.g. "EA" for data originating from the
Ethnographic Atlas or "Binford" for the data from the Hunter- and Gatherer Database. The
data files for a dataset are kept in a subdirectory of `datasets` named with the dataset ID and must 
consist of the following files:
- `variables.csv`: The list of variables, coded in a dataset; must contain columns
  - `id`: D-PLACE-wide unique identifier for the variable
  - `title`
  - `definition`
  - `type`: one of `Ordinal`, `Continuous`, `Categorical`
  - `category`: comma-separated list of categories a variable belongs to.
  - `units`
  - `source`
  - `changes`
  - `notes`
- `data.csv`: The coded values; must contain columns
  - `soc_id`: Reference to a D-PLACE society ID.
  - `var_id`: Reference to a D-PLACE variable ID.
  - `code`: Reference to a categorical value described in `codes.csv` or a literal value.
  - `sub_case`
  - `year`
  - `comment`
  - `references`: Semicolon-separated list of reference keys.
  - `source_coded_data`
  - `admin_comment`

and may optionally also provide files:
- `codes.csv`: A list of category descriptions for categorical variables:
  - `var_id`: Reference to a D-PLACE variable ID.
  - `code`
  - `description`
  - `name`
- `references.csv`: A list of references:
  - `key`: The key used to refer to this source in the data
  - `citation`: The full citation.
- `societies.csv`: A list of additional societies coded in the dataset with columns:
  - `soc_id`: D-PLACE-wide unique identifier for the society
  - `xd_id`
  - `pref_name_for_society`
  - `ORIG_name_and_ID_in_this_dataset`
  - `alt_names_by_society`
  - `main_focal_year`
  - `HRAF_name_ID` 
  - `HRAF_link`
  - `origLat`
  - `origLong`
  - `Lat`
  - `Long`
  - `Comment` on location
  - `glottocode`: Code for the most specific Glottolog languoid which can be assigned to this society.
  - `glottocode_comment`: Comment on the assignment of a glottocode to this society.
- `societies_mapping.csv`: A CSV file mapping society IDs to similar societies in other datasets.

If a dataset provides societies (possibly exclusively), it is considered a "soceity
set" as well (or exclusively). While the D-PLACE web interface distinguishes these
two ways of contributing to D-PLACE, the data model does not - because this property
can be computed.

For a dataset to be considered for import into D-PLACE it must be registered, i.e. listed in the file [`index.csv`](index.csv), which also provides additional metadata for the dataset. [`index.csv`](index.csv) has the following columns:
- `id`: The dataset ID, i.e. the name of the subdirectory of `datasets` the data is kept in.
- `type`: one of `environmental`, `cultural`.
- `name`
- `description`
- `year`
- `author`
- `reference`: Full citation of the source

Explicit registration may be somewhat redundant in keeping the dataset ID in two places - the registry and the directory name - but allows for better control over what is considered ready for import, thus makes it possible to work on datasets in their "final place" until they are finished.


### Relations

Each dataset may contribute its own set of societies. Relations among the societies from different datasets are stored in a CSV mapping file `societies_mapping.csv` in the form
```
id,related
<soc-id>,<qualified-soc-id>[;<qualified-soc-id>]*
```
where `<qualified-soc-id>` is a string composed as `<dataset-id>: <original name> [<soc-id>]`.

Currently the only type of relation specified in the data is "equivalence", but this may be a misnomer, since this implies that the sets of equivalent societies form a partition of the set of all societies, which is not the case.

Note that changing the `xd_id` of a society requires re-computing the D-PLACE 
internal society relations.

