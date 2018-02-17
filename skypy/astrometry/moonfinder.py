#!/usr/bin/env python
'''
Name  : Moon Finder, moonfinder.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Finds the moons position in the sky given a time and location
        Reason this is separate because high parallax
'''
# import standard modules

# import custom modules
from ..misc.colours import colours
from ..version import *

# checking python version
assert assertion()
__version__ = package_version()

# input time and location object
# calculates the position of the moon, the phase, and the relative brightness

