#!/usr/bin/env python
'''
Name  : SQL Storage, sqlstorage.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Will handle the databases using sqlite
'''

# imported standard modules
from os.path import isfile
from time import time as ctime
import sqlite3

# import custom modules
from .colours import colours
from ..version import *

# checking python version
assert assertion()
__version__ = package_version()


class sql(sqlobject):

    def __init__(self,dbdir=None,dbname=None):
        '''
        Initialize the class
        '''
        self.time  = '{}'.format(str(ctime()).split('.')[0])
        self.db    = None
        self.dbdir = self.resolvedir(dbdir,dbname)

    def get_functions(self):
        '''
        return all defined functions 
        '''
        return dir(self)

    def get_inputs(self):
        '''
        return all input variables initialized
        '''
        return vars(self)

    def resolve_dir(self,dbdir,dbname):
        '''
        resolve the directory name of the db
        '''
        if isfile('{}/{}'.format(dbdir,dbname)):
            return '{}/{}'.format(dbdir,dbname)
        else:
            return '{}/{}'.format(__path__[0],dbname)

    def calldb(self):
        '''
        Connect to DB
        '''
        self.db = sqlite3.connect(self.dbdir)

    def writedb(self,db,value):
        '''
        Write to DB
        star uses    : name1, name2, type, ra, dec, epoch, ubv, lastupdate
        location uses: name, lat, long, tz, T/F for DST, lastupdate
        '''
        self.sb.cursor()
        value = verify_input_sql(db,value)
        if cmd == 'star':
            self.db.executemany('INSERT INTO db VALUES (?,?,?,?,?,?,?,?,?,?)',values)
            self.db.commit()
        if cmd == 'location':
            self.db.executemany('INSERT INTO db VALUES (?,?,?,?,?,?)',values)
            self.db.commit()
        else:
            return

    def db_single(self,col1,value):
        '''
        Search an open DB, single column value select
        '''
        self.sb.cursor()
        t = (value,)
        self.db.execute('SELECT * FROM db WHERE symbol>=?', t)
        return self.db.fetchall()

    def db_ssort(self,col1,top):
        '''
        Search an open DB, single column sort, pulling top values
        '''
        self.sb.cursor()
        t = (value,)
        self.db.execute('SELECT * FROM db WHERE symbol>=?', t)
        return self.db.fetchall()

    def db_dsort(self,col1,col2,top):
        '''
        Search an open DB, double column sort, pulling top values
        '''
        self.sb.cursor()
        return self.db.fetchall()

    def db_tsort(self,col1,col2,col3,top):
        '''
        Search an open DB,triple column sort, pulling top values
        '''
        self.sb.cursor()
        return self.db.fetchall()

    def closedb(self):
        '''
        Close DB
        '''
        self.db.close()

def verify_input_sql(db,values):
    '''
    Verify input for the respective sql db
    star uses    : name1, name2, type, ra, dec, epoch, ubv, lastupdate
    location uses: name, lat, long, tz, T/F for DST, lastupdate
    '''
    if db == 'star':

    elif db == 'location'

def typecheck(obj): 
    '''
    Checks if object is iterable and not string
    '''
    return not isinstance(obj, str) and isinstance(obj, Iterable)
