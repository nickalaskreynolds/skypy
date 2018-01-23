#!/usr/bin/env python
'''
Name  : SQL Storage, sqlstorage.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Will handle the databases using sqlite
'''

# imported standard modules
from os.path import isfile

# import nonstandard modules
from astroquery.simbad import Simbad
from astropy import coordinates
import astropy.units as u

# import custom modules
from ..misc.colours import colours
from ..version import *

# checking python version
assert assertion()
__version__ = package_version()


def general():

>>> s = Simbad()
>>> s.add_votable_fields('id(1)','id(2)','ra(d)','dec(d)','ubv')
>>> r = s.query_object('m31')
>>> r
>>> r.as_array()





