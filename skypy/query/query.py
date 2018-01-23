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


def simbadoquery(qon):
    '''
    will do a general object query of simbad
    '''
    s = Simbad()
    s.add_votable_fields('id(1)','id(2)','ra(d)','dec(d)','ubv')
    r = s.query_object(qon)
    # need to add slicer to grab only needed data
    return r.as_array()

def simbadrquery(qon):
    '''
    will do a general region query of simbad
    '''
    s = Simbad()
    s.add_votable_fields('id(1)','id(2)','ra(d)','dec(d)','ubv')
    r = s.query_object(qon)
    # need to add slicer to grab only needed data
    return r.as_array()

def vizierquery(qon):
    '''
    returns standard formatted date
    '''
    return

def organize(oarray):
    '''
    organize the data output
    '''
    # take the data input and put into the list of tuples or tuple objects
    return
