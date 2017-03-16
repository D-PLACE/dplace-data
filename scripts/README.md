
Data curation scripts
=====================

Data from Glottolog
-------------------

When [Glottolog](http://glottolog.org) releases a new version, the D-PLACE data which is derived from Glottolog must be recreated. 
This is done by adapting the module globals `GLOTTOLOG_VERSION` and `GLOTTOLOG_YEAR` in [`glottolog.py`](glottolog.py) and
running
```
python glottolog.py PATH/TO/GLOTTOLOG/REPOS
```
This will recreate 
- the NEXUS files for Glottolog top-level family trees,
- the corresponding [index](../trees/index.csv) and
- the [languoid data](../csv/glottolog.csv).


Precomputed society-region mapping
----------------------------------

**FIXME: must be updated to work with new data layout!**

Require `csvkit`, `fiona` and `shapely`, all of which can be installed with `pip`.

1. Compute mapping:
   ```
   cd scripts
   python geo.py
   ```

2. Merge region-mapping and `csv/LatLong_data.csv` into `csv/society_locations.csv`.
   ```
   cd ../csv
   csvjoin LatLong_data.csv society_region.csv -c soc_id | csvcut -C 8  > society_locations.csv
   rm society_region.csv
   ```

