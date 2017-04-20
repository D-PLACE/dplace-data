# dplace-data

Data for [D-PLACE](https://d-place.org).

Research that uses data from D-PLACE should cite both the original source(s) of
the data and the paper by Kirby et al. in which D-PLACE was first presented
(e.g., research using cultural data from the Binford Hunter-Gatherer dataset:

    Binford (2001); Binford and Johnson (2006); Kirby et al. 2016).

The reference list should include the date data were accessed and URL for [D-PLACE](https://d-place.org),
in addition to the full references for Binford (2001), Binford and Johnson (2006), 
and Kirby et al. 2016.

## Versions

See the [list of releases](https://github.com/D-PLACE/dplace-data/releases) for available released versions of D-PLACE data.


## The python client library `pydplace`


To install `pydplace` you need a python installation on your system, running python 2.7 or >3.4. Run
```
python setup.py develop
```
on the top level of this repository to install the requirements, `pydplace` and
the command line interface `dplace`.

### CLI

Command line functionality is implemented via sub-commands of `dplace`. The list of
available sub-commands can be inspected running
```
$ dplace --help
usage: deplace [-h] [--verbosity VERBOSITY] [--log-level LOG_LEVEL]
                 [--repos REPOS]
                 command ...
...

Use 'dplace help <cmd>' to get help about individual commands.
```

### Python API

D-PLACE data can also be accessed programmatically from within python programs.
All functionality is mediated through an instance of `pydplace.api.Repos`, e.g.
```python
>>> from pydplace.api import Repos
>>> api = Repos('.')
>>> print(api)
<D-PLACE data repos v1.0-296-gb6f975e at .>
```
