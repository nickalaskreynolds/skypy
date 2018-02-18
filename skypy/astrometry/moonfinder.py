#!/usr/bin/env python
'''
Name  : Moon Finder, moonfinder.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Finds the moons position in the sky given a time and location
        Reason this is separate because high parallax
'''
# work in progress

# import standard modules

# import nonstandard modules
import numpy as np
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, SkyCoord,get_moon,get_sun

# import custom modules
from ..misc.colours import colours
from ..version import *

# checking python version
assert assertion()
__version__ = package_version()

# input time and location object
# calculates the position of the moon, the phase, and the relative brightness
def moonaltaz(location,time):
    '''
    return moon posution at given time
    '''
    frame_obs = AltAz(obstime=time,location=location)
    targaltaz = get_moon(time=time,location=location).transform_to(frame_obs)
    return targaltaz

def conv(dec):
    neg = if dec < 0
    dec = abs(dec)
    temp0 = int(dec)
    temp1 = (dec - temp0)*60.
    temp2 = int(temp1)
    temp3 = round((temp2 - temp1)*60.,4)
    if neg:
        temp0 = -1.* temp0
    return '{}d{}m{}s'.format(temp0,temp2,temp3)

def moon_phase_angle(time, ephemeris=None):
    '''
    Calculate lunar orbital phase in radians.
    '''
    # TODO: cache these sun/moon SkyCoord objects

    sun = get_sun(time)
    moon = get_moon(time, ephemeris=ephemeris)
    elongation = sun.separation(moon)
    return np.arctan2(sun.distance*np.sin(elongation),
                      moon.distance - sun.distance*np.cos(elongation))

def moon_illumination(time, ephemeris=None):
    '''
    Calculate fraction of the moon illuminated.
    '''
    i = moon_phase_angle(time, ephemeris=ephemeris)
    k = (1 + np.cos(i))/2.0
    return k.value
