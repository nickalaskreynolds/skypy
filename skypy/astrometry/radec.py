#!/usr/bin/env python
'''
Name  : RA DEC, radec.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : From the RA DEC resolve the alt az of an object
        Also, consequently, return when object is visible
'''
# import standard modules

# import custom modules
from ..misc.colours import colours
from ..version import *

# checking python version
assert assertion()
__version__ = package_version()

# input time and location object


class body(object):
    # assuming ra and dec in 
    def __init__(self):
        self.ra   = ra
        self.dec  = dec
        self.loc  = location
        self.time = time

