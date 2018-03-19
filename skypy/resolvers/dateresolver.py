#!/usr/bin/env python
'''
Name  : Date Resolver,dateresolve.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Resolves the date supplied to a more standard format, yields 
        an object that holds the orig date, utc, and the season
'''

# imported standard modules
from datetime import date as today
import datetime
import math

# import custom modules
from ..version import *
from ..misc.functions import *

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

def checkconv(obj,epoch='ordinal'):
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
        if epoch == 'ordinal':
            fin = int(''.join([x for x in today.fromordinal(obj).timetuple()[0:3]]))
        elif epoch == 'julian':
            fin = datetime.datetime(2000, 1, 1) + datetime.timedelta(obj)
            fin = int(''.join([x for x in fin.timetuple()[0:3]]))
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
            if epoch == 'ordinal':
                fin = int(''.join([x for x in today.fromordinal(float(obj)).timetuple()[0:3]]))
            elif epoch == 'julian':
                fin = datetime.datetime(2000, 1, 1) + datetime.timedelta(obj)
                fin = int(''.join([x for x in fin.timetuple()[0:3]]))
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

def convertdatejdn(date,time,method=1):
    date = str(date)
    time = str(time)
    """
    1. Get current values for year, month, and day
    2. Same for time and make it a day fraction
    3. Calculate the julian day number via   https://en.wikipedia.org/wiki/Julian_day
    4. Add the day fraction to the julian day number

    """
    MJD_0 = 2400000.5
    MJD_JD2000 = 51544.5

    def fpart(x):
        """Return fractional part of given number."""
        return math.modf(x)[0]


    def ipart(x):
        """Return integer part of given number."""
        return math.modf(x)[1]


    def is_leap(year):
        """Leap year or not in the Gregorian calendar."""
        x = math.fmod(year, 4)
        y = math.fmod(year, 100)
        z = math.fmod(year, 400)

        # Divisible by 4 and,
        # either not divisible by 100 or divisible by 400.
        return not x and (y or not z)


    def gcal2jd(year, month, day):
        year = int(year)
        month = int(month)
        day = int(day)

        a = ipart((month - 14) / 12.0)
        jd = ipart((1461 * (year + 4800 + a)) / 4.0)
        jd += ipart((367 * (month - 2 - 12 * a)) / 12.0)
        x = ipart((year + 4900 + a) / 100.0)
        jd -= ipart((3 * x) / 4.0)
        jd += day - 2432075.5  # was 32075; add 2400000.5

        jd -= 0.5  # 0 hours; above JD is for midday, switch to midnight.

        return MJD_0, jd


    def jd2gcal(jd1, jd2):
        from math import modf

        jd1_f, jd1_i = modf(jd1)
        jd2_f, jd2_i = modf(jd2)

        jd_i = jd1_i + jd2_i

        f = jd1_f + jd2_f

        # Set JD to noon of the current date. Fractional part is the
        # fraction from midnight of the current date.
        if -0.5 < f < 0.5:
            f += 0.5
        elif f >= 0.5:
            jd_i += 1
            f -= 0.5
        elif f <= -0.5:
            jd_i -= 1
            f += 1.5

        l = jd_i + 68569
        n = ipart((4 * l) / 146097.0)
        l -= ipart(((146097 * n) + 3) / 4.0)
        i = ipart((4000 * (l + 1)) / 1461001)
        l -= ipart((1461 * i) / 4.0) - 31
        j = ipart((80 * l) / 2447.0)
        day = l - ipart((2447 * j) / 80.0)
        l = ipart(j / 11.0)
        month = j + 2 - (12 * l)
        year = 100 * (n - 49) + i + l

        return int(year), int(month), int(day), f


    def jcal2jd(year, month, day):
        year = int(year)
        month = int(month)
        day = int(day)

        jd = 367 * year
        x = ipart((month - 9) / 7.0)
        jd -= ipart((7 * (year + 5001 + x)) / 4.0)
        jd += ipart((275 * month) / 9.0)
        jd += day
        jd += 1729777 - 2400000.5  # Return 240000.5 as first part of JD.

        jd -= 0.5  # Convert midday to midnight.

        return MJD_0, jd


    def jd2jcal(jd1, jd2):
        from math import modf

        jd1_f, jd1_i = modf(jd1)
        jd2_f, jd2_i = modf(jd2)

        jd_i = jd1_i + jd2_i

        f = jd1_f + jd2_f

        # Set JD to noon of the current date. Fractional part is the
        # fraction from midnight of the current date.
        if -0.5 < f < 0.5:
            f += 0.5
        elif f >= 0.5:
            jd_i += 1
            f -= 0.5
        elif f <= -0.5:
            jd_i -= 1
            f += 1.5

        j = jd_i + 1402.0
        k = ipart((j - 1) / 1461.0)
        l = j - (1461.0 * k)
        n = ipart((l - 1) / 365.0) - ipart(l / 1461.0)
        i = l - (365.0 * n) + 30.0
        j = ipart((80.0 * i) / 2447.0)
        day = i - ipart((2447.0 * j) / 80.0)
        i = ipart(j / 11.0)
        month = j + 2 - (12.0 * i)
        year = (4 * k) + n + i - 4716.0

        return int(year), int(month), int(day), f

    y,mo,d,h,m,s= int(date[0:4]),int(date[4:6]),\
                 int(date[6:8]),int(time[0:2]),\
                 int(time[2:4]),int(time[4:6])
    return sum(gcal2jd(y,mo,d)) + h / 24. + m / (24. * 60.) + s / (24. * 60. * 60.)

def lst(jd,longit):
    '''
    jd is wanted lst julian date
    jd is float
    jd0 is previous julian date midnight (must be 0.5)
    h is hours since previous
    longit is in hours
    '''
    # find julian date of previous midnight
    if (jd % 1 ) < 0.5:
        jd0 = float(int(jd)) - 0.5
    else:
        jd0 = float(int(jd)) + 0.5

    MJD_0 = 2400000.5
    MJD_JD2000 = 51544.5
    h    = jd - jd0             # get hours since prev jd midnight
    mjd  = MJD_JD2000 + MJD_0   # mean julian day conv
    d,d0 = jd - mjd,jd0 - mjd   # num of days since j2000
    t    = d / 36525            # number of centuries since year 2000
    G = 6.697374558 #constant for year
    GMST = G + 0.06570982441908 * d0 +\
           1.00273790935 * h + 0.000026 * t**2 # greenwish mean sidereal time
    print(GMST)       
    GMST = GMST % 24       
    ep   = 23.4393 - 0.0000004 * d # obliquity
    loso = 280.47 + 0.98565 * d    # mean long of sun
    lan  = 125.04 - 0.052954 * d   # line of ascending node of moon
    ep,loso,lan = deg_2_rad([ep,loso,lan])
    nuta = -0.000319 * math.sin(lan) - \
            0.000024* math.sin(2.*loso) # nutation of logitude
    eqeq = nuta * math.cos(ep) # equation of equinoxes
    GAST = GMST + eqeq

    longit = longit / 15.

    # west justified
    print('d0:{},h:{},t:{},gmst:{},eq:{},gast:{},long:{}'\
          .format(d0,h,t,GMST,eqeq,GAST,longit))
    lst = GAST - longit
    lst0 = int(lst)
    delt = (lst - lst0) * 60.
    lst1 = int((lst - lst0) * 60.)
    lst2 = (delt - lst1) * 60.
    return lst,':'.join(map(str,[lst0,lst1,lst2]))


    



