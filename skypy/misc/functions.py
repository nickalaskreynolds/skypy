#!/usr/bin/env python
'''
Name  : Functions, function.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Holds the highly used and general functions
'''

# import standard modules
from collections import Iterable
import math

# import custom modules
from ..version import *
from . import constants as constant

# checking python version
assert assertion()
__version__ = package_version()

def typecheck(obj): 
    '''
    Checks if object is iterable (array,list,tuple) and not string
    '''
    return not isinstance(obj, str) and isinstance(obj, Iterable)

def checkconv(coord):
    '''
    will take a coord convert to a list
    return the decimal conversion
    '''
    delimiters = [':',' ',',']
    failed = False
    orig = coord
    # if a string, handle
    if type(coord) == float:
        return coord
    if type(coord) == str:
        # check if float hidden as string
        try:
            return float(coord)
        except:
            # handle string proper by going through all delimiters
            count = 0
            while not typecheck(coord):
                #print(count)
                coord = coord.split(delimiters[count])
                if len(coord) == 1:
                    coord = coord[0]
                if count == len(delimiters) - 1:
                    failed = True
                    break
                count += 1
    # try with different scheme
    if failed == True:
        hold = coord
        sp = 'h'
        t0 = hold.split(sp)[0]
        if t0 == hold:
            sp = 'd'
            t0 = hold.split(sp)[0]


        if len([x for x in hold.split(sp) if x != '']) == 1:
            coord = [t0]
        else:
            t1 = hold.split(sp)[1].split('m')[0]
            if len(t1.split('.')) == 1:
                t2 = hold.split(sp)[1].split('m')[1].strip('s')
            else:
                t2 = ''
            hold = [t0,t1,t2]
            hold = [x for x in hold if ((x != '' )and (type(x) == str))]
            coord = hold

    # if list, make to float, final form
    #print(len(coord),orig)
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

def atan(x,y):
    '''
    find the arctan of 2 position points and remap to 0->2pi
    '''
    rads = math.atan2(y, x)
    if rads < 0:
        rads = 2*constant.pi + rads
    return rads

def rad_2_deg(rad):
    '''
    convert deg to radians
    '''
    if typecheck(rad):
        return [x * 180. / constant.pi for x in rad]
    else:
        return rad * 180. / constant.pi

def deg_2_rad(deg):
    '''
    convert deg to radians
    '''
    if typecheck(deg):
        return [x * constant.pi / 180. for x in deg]
    else:
        return deg * constant.pi / 180.

def min_max_altitude(lat,dec):
    '''
    find the main and max altitude of a sky pos
    given it's dec and current lat of location
    lat and dec in deg
    '''
    lat,dec = deg_2_rad([lat,dec])

    xmax = math.cos(dec) * math.cos(lat) + \
           math.sin(dec) * math.sin(lat)
    xmin = math.cos(dec) * math.cos(lat) - \
           math.sin(dec) * math.sin(lat)
    return math.asin(xmin),math.asin(xmax)

def secant(x):
    '''
    nicely compute secant
    '''
    if x > 0:
        z = 1./math.cos(x)
    else:
        z = 100
    if z > 100:
        return 100
    elif z < -100:
        return -100
    else:
        return z

def altitude(dec,ha,lat):
    '''
    given the dec, hour angle, and latitude, compute some needed parameters
    for the target including altitude, azimuth,parallactic angle
    '''
    dec,ha,lat = deg_2_rad([dec,ha,lat])
    cdec,sdec,cha,sha,clat,slat = math.cos(dec),math.sin(dec),\
                                  math.cos(ha),math.sin(ha),\
                                  math.cos(lat),math.sin(lat)
    x = math.asin(cdec * cha * clat + sdec * slat)
    y = sdec * clat - cdec * cha * slat
    z = -1. * cdec * sha
    az = math.atan2(z,y)
    if cdec == 0: #north or south pole
        if lat >= 0:
            parang = 180.
        else:
            parang = 0.
    else: # everywhere else
        # insert law of cosines/sines
        sinp = -1. * math.sin(az) * clat / cdec
        cosp = (-1. * math.cos(az) * cha) - (math.sin(az) * sha * slat)
        parang = math.atan2(sinp,cosp)
        parang = deg_2_rad(parang)
    az = deg_2_rad(az)
    if az < 0:
        az += 360.
    elif az > 360.:
        az -= 360.
    return x,y,z,az,parang

def airmass(secz):
    '''
    find the airmass of the target
    '''
    if secz < 0:
        return -1
    if secz > 12:
        return -1
    poly = [2.879465E-3,3.033104E-3,1.351167E-3,-4.716679E-5]
    seczm = secz - 1.
    result = 0
    for i in range(len(poly))[::-1]:
        result = (result + poly[i]) * seczm
    result = secz - result
    return result

def ha_alt(dec,lat,alt):
    '''
    finds the hour angle of the target
    given the dec is at altitude
    returns 100 or -100 for non values
    '''
    mina,maxa = min_max_altitude(lat,dec)
    if alt < mina:
        return 100
    elif alt > maxa:
        return -100
    dec,lat,coalt = deg_2_rad([dec,lat,constant.pi/2. - alt])
    x = (math.cos(coalt) - math.cos(dec) * math.cos(lat))/ \
        (math.sin(dec) * math.sin(lat))
    if abs(x) >= 1.:
        return deg_2_rad(math.acos(x)*15.)

def subtend(ra1,dec1,ra2,dec2):
    '''
    finds the angle between two position in the sky
    ra in hours and dec in deg
    '''
    ra1,ra2   = deg_2_rad([ra1*15.,ra2*15.])
    dec1,dec2 = deg_2_rad([dec1,dec2])
    x1 = math.cos(ra1)*math.cos(dec1)
    y1 = math.sin(ra1)*math.cos(dec1)
    z1 = math.sin(dec1)
    x2 = math.cos(ra2)*math.cos(dec2)
    y2 = math.sin(ra2)*math.cos(dec2)
    z2 = math.sin(dec2)  
    if (abs(z1) < 89.99) or (abs(z2) < 89.99):
        theta = math.acos(x1*x2+y1*y2+z1*z2)
    else: # near poles
        theta = math.acos(x1*x2+y1*y2)
    return theta







