# Architecture Proposal for D-PLACE v3.0

The data collected/aggregated/curated for D-PLACE 3 should be organized in a more distributed way, optimized for
- distributed curation/maintenance, in particular
  - making additions easy (even more so, if there are blog posts describing how to do that - e.g. to compare your own data with D-PLACE's)
  - integrating work-in-progress datasets in a better way
- easier access to individual datasets.

## Examples

Aggregated databases using a model that could serve as example for D-PLACE:
- [lexibank](https://github.com/lexibank/) - a big collection of lexical data for the world's languages
- UniversalDependencies (UD): [on GitHub](https://github.com/UniversalDependencies/), [website](https://universaldependencies.org/)


## One GitHub repository per dataset/phylogeny

- Each citable unit of data aggregated in D-PLACE should be curated in its own GitHub repository (preferably - but not necessarily under the [D-PLACE GitHub organization](https://github.com/D-PLACE)).
- The basic distribution format for datasets should be a [CLDF](https://cldf.clld.org) derivative - but additional distribution formats could be provided, e.g.
  - a "flat CSV file" format for datasets
  - a Nexus file for phylogenies
- `cldfbench` should be used to transparently separate editable data sources from distribution formats in these repositories.

To date, this would mean about 12 repositories for D-PLACE datasets, and 26 for D-PLACE phylogenies. From our experience with lexibank (>100 datasets),
that would seem manageable - also for the forseeable future. Considering the different types of data in D-PLACE, a naming convention for the repositories
could be adopted (something along the lines of `dplace-dataset-<AUTHOR><YEAR>` and `dplace-phylogeny-<AUTHOR><YEAR>`), to make browsing simpler.


## The D-PLACE umbrella/brand

Just like UD's "tools" and "docs" repositories, or lexibank's `pylexibank` package, there would be quite a bit of infrastructure making
up the D-PLACE umbrella or brand:

- `pydplace`: a curation package, ensuring individual repositories meet common standards
- `D-PLACE/societysets` - a repository to catalog society sets (and mappings between them) which have been used to collect cross-cultural data (much like https://concepticon.clld.org catalogs concept lists used to collect lexical data)
- D-PLACE GitHub org
- D-PLACE Zenodo community - cataloging released versiond of D-PLACE datasets
- https://d-place.org - the store front
- The blog/book/cookbook?


## Open Questions

- Attribution: Will easy access to individual datasets (e.g. EA) dilute the D-PLACE brand? Can this be prevented with suitable citation recommendations?
  E.g. [lexibank's datasets](https://zenodo.org/communities/lexibank?page=1&size=20) typically have titles like "CLDF dataset derived from SOURCE", so
  D-PLACE datasets could have titles like "D-PLACE dataset derived from Murdock's Ethnographic Atlas".
