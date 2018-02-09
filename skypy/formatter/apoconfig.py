#!/usr/bin/env python
'''
Name  : APO Config, apoconfig.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Config File for apo output
'''

config={
    'pprint' : True,\
    'newline': True,\
    'headerbreak'  : '#',\
    'includefields': True,\
    'header'       : '',\
    'interfielddelimiter': ' ',\
    'intrafielddelimiter': ['',':',':',''],\
    'fields'     : ['Name','RA','Dec','Magnitude'],\
    'fieldprefix': ['','','','Magntitude='],\
    'fieldsuffix': ['','','',''],\
    'customend'  : '',\
    'customfield': ["Telescope Home",98,30,"CSys=Mount; RotType=Mount; RotAng=0"],\
    'customend'  : ''
}
