#!/usr/bin/env python
'''
Name  : Parser, parser.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Parses config files
'''

# import custom modules
from ..misc.colours import colours
from ..version import *
from ..misc.config import configuration as config

# checking python version
assert assertion()
__version__ = package_version()


def init(ifile=None):
    '''
    initialize the config file
    '''
    temp = config(ifile)['config']
    return temp

def base_templates():
    '''
    returns the original templates
    '''
    from glob import glob
    files = glob(__file__ + '/*config*')
    del files[files.index('templateconfig.py')]
    return [x.strip('.py').strip('config') for x in files]

def user_templates():
    '''
    returns user templates
    must be in .cache
    '''
    from os.path import expanduser
    home = '{}/.cache/skypy/templates'.format(expanduser("~"))
    from glob import glob
    files = glob('{}/.py'.format(home))
    return [x.strip('.py').strip('config') for x in files]

def write(configstyle,data,oname):
    '''
    write to file based on template
    '''
    
    return


    


