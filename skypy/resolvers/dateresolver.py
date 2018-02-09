#!/usr/bin/env python
'''
Name  : Date Resolver,dateresolve.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Resolves the date supplied to a more standard format, yields 
        an object that holds the orig date, utc, and the season
'''

# CHECK THIS!!!!!!!!

# imported standard modules
from collections import Iterable
from datetime import date as today

# import custom modules
from ..version import *

# checking python version
assert assertion()
__version__ = package_version()

class date(object):
    '''
    input date,location wanted for query
    output formated date
    '''
    def __init__(self,orig=None,hemi='n'):
        nhemi = ['n','northern','north']
        shemi = ['s','southern','south']
        if orig == None:
            orig = today.today().timetuple()[0:3]
        self.original = checkconv(orig)
        if hemi.lower() in nhemi:
            self.location = nhemi[0]
        elif hemi.lower in shemi:
            self.location = shemi[0]
        self.season   = self.findseason()
        self.final    = '{}.{}'.format(self.original,self.season)

    def get_params(self):
        return dir(self)

    def get_functions(self):
        return vars(self)

    def formatter(self):
        '''
        returns standard formatted date
        '''
        return self.final

    def findseason(self):
        '''
        Northern hemi bias seasons
        MM-DD
        '''
        seasons={'1':['01-01','02-29','Late-Winter'],\
                 '2':['03-01','04-31','Spring'],\
                 '3':['05-01','06-31','Early-Summer'],\
                 '4':['07-01','08-31','Late-Summer' ],\
                 '5':['09-01','10-31','Fall' ],\
                 '6':['11-01','12-31','Early-Winter'],\
                 }
        if self.location == 'n':
            month = int(str(self.original)[4:6])
        else:
            month = (int(str(self.original)[4:6]) + 6)
            if month > 12:
                month = month - 12
        seasonkey = str(month//2 + month%2)
        return seasons[seasonkey][2]

def checkconv(obj):
    '''
    will take a obj and convert to list proper
    probably more complicated than ever needs to be
    '''
    delimiters = [':',' ','/',',','.']
    # delimiting scheme assumes YYYY,MM,DD format
    # if obj is number of days since epoch, Julian(1950) or Ordinal(2001)
    if (type(obj) == float) or (type(obj) == int):
        try:
            # try if int object is already in proper format
            temp = str(obj)
            y = temp[0:4]
            m = temp[4:6]
            d = temp[6:8]
            if (0 < float(m) < 13) and (0 < float(d) < 32):
                # returns int
                return obj
        except:
            pass
        print('Assuming time since Ordinal (2001)')
        fin = int(''.join([x for x in today.fromordinal(obj).timetuple()[0:3]]))
        # returns int
        return fin
    # if object is string
    if type(obj) == str:
        # if str is already of proper format
        try:
            y = obj[0:4]
            m = obj[4:6]
            d = obj[6:8]
            if (0 < float(m) < 13) and (0 < float(d) < 32):
                # returns int
                return int(obj)
        except:
            pass
        # check if float hidden as string
        try:
            fin = int(''.join([x for x in today.fromordinal(float(obj)).timetuple()[0:3]]))
            print('Assuming time since Ordinal (2001)')
            return fin
        except:
            # handle string proper
            count = 0
            while not typecheck(obj):
                obj = obj.split(delimiters[count])
                if len(obj) == 1:
                    obj = obj[0]
                count += 1
    # should now be of list format [YYYY MM DD] if was string float or int
    # if list, make to float, final form
    if typecheck(obj):
        # if in proper format
        if len(obj) == 3:
            y = obj[0]
            if len(str(y)) != 4:
                if y > int(str(today.today().timetuple()[0])[-2:])+1:
                    y = '19{}'.format(y)
                else:
                    y = '20{}'.format(y)
            m = obj[1]
            if len(str(m)) != 2:
                m = '0{}'.format(m)
            d = obj[2]
            if len(str(d)) != 2:
                d = '0{}'.format(d)
            if (0 < int(m) < 13) and (0 < int(d) < 32):
                return int(''.join(map(str,[y,m,d])))
        elif len(obj) == 1:
            # if an iterable of len one with float
                return checkconv(obj[0])
        else:
            try:
                return [checkconv(x) for x in obj]
            except:
                print('Date object incorrect format')
                return False

def typecheck(obj): 
    '''
    checks type of obj and verifies it is iterable proper
    '''
    return not isinstance(obj, str) and isinstance(obj, Iterable)
