"""
Main command line interface of the pydplace package.

Like programs such as git, this cli splits its functionality into sub-commands
(see e.g. https://docs.python.org/2/library/argparse.html#sub-commands).
The rationale behind this is that while a lot of different tasks may be
triggered using this cli, most of them require common configuration.

The basic invocation looks like

    dplace [OPTIONS] <command> [args]

"""
from __future__ import unicode_literals, division, print_function
import sys
import argparse

from clldutils.clilib import ArgumentParserWithLogging
from clldutils.path import Path

import pydplace
from pydplace.api import Repos
import pydplace.commands
assert pydplace.commands


def main():  # pragma: no cover
    try:
        drepos = Repos(Path(pydplace.__file__).parent.parent)
    except:
        drepos = None

    parser = ArgumentParserWithLogging(pydplace.__name__)
    parser.add_argument('--repos', help=argparse.SUPPRESS, type=Repos, default=drepos)
    sys.exit(parser.main())
