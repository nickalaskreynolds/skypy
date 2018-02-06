#!/usr/bin/env python
'''
Name  : Location Resolver,locationresolve.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Resolves the location supplied to a more standard format, yields 
        an object that holds the orig date, utc, and the season
'''

# UNTESTED

# imported standard modules

# import custom modules
from ..version import *
from collections import Iterable

# checking python version
assert assertion()
__version__ = package_version()

def typecheck(obj): return not isinstance(obj, str) and isinstance(obj, Iterable)

class location(object):

    def __init__(self,lat,lon,tz=0):
        '''
        input lat and long in +-DD.DDDN/S/E/W format 
        must both be strings
        37.124N,-97.124E
        '''
        self.coords = self.justifycoords(lat,lon)
        self.tz     = self.timezone(tz)

    def main(self):
        return self.coords,self.tz,self.hemisphere(self.coords[0])

    def timezone(self,local):
        zones = [x for x in range(-12,13)]
        assert local in zones
        return local

    def hemisphere(self,hemi):
        if hemi > 0:
            return 'n'
        else:
            return 's'

    def justifycoords(self,lat,lon):
        '''
        Will N and E justify coords
        They have to be strings
        '''
        
        lat = checkconv(lat)
        lon = checkconv(lon)

        if lat[-1:].lower() == 'n':
            lat = float(lat[:-1])
        else:
            lat = -1.* float(lat[:-1])

        if lon[-1:].lower() == 'e':
            lon = float(lon[:-1])
        else:
            lon = -1.* float(lon[:-1])
        return lat,lon

    def cat(init,delim=' ',to=''):
        if typecheck(init):
            init = ' '.join(init)
        return to.join(init.split(delim))

    def checkconv(coord,direc='n'):
        '''
        will take a string coord of standard delimiters ' ' or ':'
        convert to a list
        return the decimal conversion and direction
        '''
        coord = cat(coord,' ',':')

        if len(coord.split(':')) == 3:
            try:
                t = float(coord[-1:])
                direc = 'n'
            except:
                direc = coord[-1:]
                coord = coord[:-1]

            if len(coord.split(':'))>0:
                tmp = lat.split(':')
                fin = tmp[0] + \
                      tmp[1]/60. +\
                      tmp[2]/3600.+\
            return '{}{}'.format(fin,direc)
        else:
            try:
                t = float(coord[-1:])
                direc = 'n'
            except:
                direc = coord[-1:]
                coord = coord[:-1]

            return '{}{}'.format(coord,direc)
