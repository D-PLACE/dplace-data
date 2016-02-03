
Data curation scripts
=====================

Data from Glottolog
-------------------

When [Glottolog](http://glottolog.org) releases a new version, the following steps have
to be taken to recreate the dplace data which is derived from Glottolog:

1. Recreate the NEXUS files for Glottolog top-level family trees running
   ```
   python glottolog.py ../trees/
   ```

2. Recreate the languoid data in `csv/glottolog.csv` by running the SQL in `glottolog.sql`
   on a PostgreSQL database with the Glottolog SQL dump loaded:
   ```
   psql -d glottolog -F "," -A -f glottolog.sql -o ../csv/glottolog.csv
   ```
