#!/usr/bin/env python
'''
Name  : Location Resolver,locationresolver.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Resolves the location supplied to a more standard format, yields 
        an object that holds the orig date, utc, and the season
'''

# imported standard modules
from collections import Iterable

# import custom modules
from ..version import *

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

def checkconv(coord):
    '''
    will take a coord convert to a list
    return the decimal conversion
    '''
    delimiters = [':',' ','  ',',']
    # if a string, handle
    if type(coord) == float:
        return coord
    if type(coord) == str:
        # check if float hidden as string
        try:
            return float(coord)
        except:
            # handle string proper
            while not typecheck(coord):
                count = 0
                coord = coord.split(delimiters[count])
                if len(coord) == 1:
                    coord = coord[0]
                count += 1
    # if list, make to float, final form
    if typecheck(coord):
        if len(coord) == 3:
            temp0,temp1,temp2 = map(float,coord)
            total = abs(temp0) + temp1/60. + temp2/3600
        elif len(coord) == 2:
            temp0,temp1 = map(float,coord)
            temp2 = temp1/60. - temp1
            total = abs(temp0) + temp1/60. + temp2/3600
        elif len(coord) == 1:
            # if an iterable of len one with float
            try:
                return float(coord[0])
            except:
                return checkconv(coord[0])
        if temp0 < 0.:
            total = total * -1
    return total

def typecheck(obj): 
    '''
    checks type of obj and verifies it is iterable proper
    '''
    return not isinstance(obj, str) and isinstance(obj, Iterable)
