#!/usr/bin/env python
'''
Name  : Location Resolver,locationresolver.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Resolves the location supplied to a more standard format, yields 
        an object that holds the orig date, utc, and the season
'''

# import custom modules
from ..version import *
from ..misc.functions import *

# checking python version
assert assertion()
__version__ = package_version()


class location(object):
    '''
    This location object will better justify the location format
    '''

    def __init__(self,name,lat,lon,tz,dst):
        '''
        Initialize class
        name string
        lat long can be of any any standard format
        N W justified
        tz int
        dst y/n
        '''
        self.name   = name
        self.coords = self.justifycoords(lat,lon)
        self.tz     = self.timezone(tz)
        assert dst.lower() in ['y','n']
        self.dst    = dst.lower()

    def main(self):
        '''
        main call
        '''
        return self.name,self.coords,self.tz,self.dst

    def timezone(self,local):
        '''
        force timezones to be -12...12
        '''
        zones = [x for x in range(-12,13)]
        assert local in zones
        return local

    def justifycoords(self,lat,lon):
        '''
        Need to be N and W justified
        '''
        
        lat = checkconv(lat)
        lon = checkconv(lon)
        return lat,lon
