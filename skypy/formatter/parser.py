#!/usr/bin/env python
'''
Name  : Parser, parser.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Parses config files
'''
# import standard modules
from glob import glob
from os.path import expanduser
import os 
from collections import Iterable
dir_path = os.path.dirname(os.path.realpath(__file__))
home = '{}/.cache/skypy/templates'.format(expanduser("~"))

# import custom modules
from ..misc.colours import colours
from ..version import *
from ..misc.config import configuration as config

# checking python version
assert assertion()
__version__ = package_version()

def typecheck(obj): 
    '''
    Checks if object is iterable and not string
    '''
    return not isinstance(obj, str) and isinstance(obj, Iterable)

def initconfig(ifile=None):
    '''
    initialize the config file
    '''
    if os.path.isfile(ifile):
        temp  = config(ifile)
        temp.read()
        temp = temp.get_params()['config']
    elif (ifile in dir_strip(all_templates())):
        temp1 = all_templates()
        temp2 = temp1[dir_strip(temp1).index(ifile.strip('.py'))]
        temp  = config(temp2)
        temp.read()
        temp = temp.get_params()['config']
    else:
        temp = None
    return temp

def dir_strip(temp):
    if typecheck(temp):
        return [''.join(x.split('/')[-1].split('.')[:-1]) for x in temp]
    else:
        return ''.join(temp.split('/')[-1].split('.')[:-1])

def all_templates():
    return user_templates() + base_templates()

def base_templates():
    '''
    returns the original templates
    '''
    files = glob(dir_path + '/*config*')
    del files[files.index(dir_path + '/templateconfig.py')]
    return [x for x in files]

def user_templates():
    '''
    returns user templates
    must be in .cache
    '''
    files = glob('{}/*'.format(home))
    return [x for x in files]

def write(configfile,data,oname):
    '''
    write to file based on template
    '''
    config = initconfig(configfile)
    with open(oname,'r') as f:
        for x in config['header']:
            f.write('{} {} \n'.format(config['commentline'],x))
        if config['includefields']:
            f.write('{} {} \n'.format(config['commentline'],pprinting(config['fields'],len(config['fields']),False,5)))

        f.write('{}'.format(pprinting(create_str(data,config),len(config['fields']),True,3)))

        if config['customfield']:
                f.write('{} \n'.format(pprinting(config['customfield'],len(config['customfield']),False,5)))
        if config['customend']:
                f.write('{} {} \n'.format(config['commentline'],x))

def create_str(data,config):
    prefix = config['fieldprefix']
    suffix = config['fieldsuffix']
    interdelim = config['interfielddelimiter']
    final = []
    for j in data:
        temp = [prefix[i] + p + suffix[i] + interdelim for i,p in enumerate(j)]
        temp[-1] = str(temp[-1]).strip(interdelim) + '\n'
        final.append(tuple(temp))
    return final


def pprinting(obj, cols=4, columnwise=True, gap=4):
    """
    Print the given list in evenly-spaced columns.

    Parameters
    ----------
    obj : list
        The list to be printed.
    cols : int
        The number of columns in which the list should be printed.
    columnwise : bool, default=True
        If True, the items in the list will be printed column-wise.
        If False the items in the list will be printed row-wise.
    gap : int
        The number of spaces that should separate the longest column
        item/s from the next column. This is the effective spacing
        between columns based on the maximum len() of the list items.
    """
    import math

    sobj = [str(item) for item in obj]
    if cols > len(sobj): cols = len(sobj)
    max_len = max([len(item) for item in sobj])
    if columnwise: cols = int(math.ceil(float(len(sobj)) / float(cols)))
    plist = [sobj[i: i+cols] for i in range(0, len(sobj), cols)]
    if columnwise:
        if not len(plist[-1]) == cols:
            plist[-1].extend(['']*(len(sobj) - len(plist[-1])))
        plist = zip(*plist)
    printer = '\n'.join([
        ''.join([c.ljust(max_len + gap) for c in p])
        for p in plist])
    return printer



