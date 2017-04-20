# coding: utf8
from __future__ import unicode_literals, print_function, division
from unittest import TestCase

from clldutils.path import Path


class Tests(TestCase):
    def test_Repo(self):
        from pydplace.api import Repos

        with self.assertRaises(IOError):
            Repos(Path(__file__).parent)
