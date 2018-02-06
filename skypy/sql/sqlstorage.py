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
from collections import Iterable

# import custom modules
from ..misc.colours import colours
from ..version import *

# checking python version
assert assertion()
__version__ = package_version()

class sql(object):

    def __init__(self,dbdir=None,dbname=None):
        '''
        Initialize the class
        '''
        self.time  = '{}'.format(str(ctime()).split('.')[0])
        self.db    = None
        self.dbdir = self.resolve_dir(dbdir,dbname)

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
        self.sb = self.db.cursor()   

    def writedb(self,db,value):
        '''
        Write to DB
        star uses    : name1, name2, type, ra, dec, epoch, ftype,fval, lastupdate
        location uses: name, lat, long, tz, T/F for DST, lastupdate
        '''
        values = verify_input_sql(db,value)
        with self.db:
            if db == 'star':
                self.sb.executemany('INSERT INTO db VALUES (?,?,?,?,?,?,?,?,?)',values)
            if db== 'location':
                self.sb.executemany('INSERT INTO db VALUES (?,?,?,?,?,?)',values)
            else:
                return

    def db_sel(self,col1,value):
        '''
        Search an open DB, single value select
        '''
        self.sb.execute("SELECT * FROM db WHERE `%s` like '%s'" % (col1,value))
        return self.sb.fetchall()

    def db_ssort(self,col1,top,order='asc'):
        '''
        Search an open DB, single column sort, pulling top values
        '''
        #                                                   col1 order   top
        cursor = self.sb.execute("SELECT * FROM db ORDER BY `%s` %s LIMIT %d" % (col1,order.upper(),int(top)))

        return [x for x in cursor]

    def db_dsort(self,col1,col2,top,order=['asc','asc']):
        '''
        Search an open DB, double column sort, pulling top values
        '''
        #                                                  col1 ordercol2  order   top
        cursor = self.sb.execute("SELECT * FROM db ORDER BY `%s` %s ,`%s` %s LIMIT %d" % (col1,order[0].upper(),col2,order[1].upper(),int(top)))
        return [x for x in cursor]

    def db_selsort(self,col1,value,col2,top,order='asc'):
        '''
        Search an open DB,Select from column, order by another, limit results
        '''
        #                                                 col1    value        col2 order      top
        cursor = self.sb.execute("SELECT * FROM db WHERE `%s` like '%s' ORDER BY `%s` %s LIMIT %d" % (col1,value,col2,order.upper(),int(top)))
        return [x for x in cursor]

    def db_delete(self,col,name):
        '''
        Delete from Database
        '''
        assert col in ['Name1','Name2','Name']
        self.sb.execute("DELETE from db where `%s` = '%s'" % (col,name))
        print('Total rows deleted: {}'.format(self.db.total_changes))

    def closedb(self):
        '''
        Close DB
        '''
        if self.db:
            self.db.close()

def verify_input_sql(db,values):
    '''
    Verify input for the respective sql db
    star uses    : name1, name2, type, ra, dec, epoch, ftype,fval, lastupdate
    location uses: name, lat, long, tz, T/F for DST, lastupdate
    '''
    final = []
    if (typecheck(values) and type(values) != tuple) and (len(values) == 9) or (len(values) == 6):
        final = [tuple(x) for x in values]
    elif typecheck(values) and type(values) == tuple:
        final = [values,]
    else:
        raise RuntimeError('Cannot verify input for sql')

    if db == 'star':
        if len(final[0]) != 9:
            raise RuntimeError('Cannot verify input for sql')
    elif db == 'location':
        if len(final[0]) != 6:
            raise RuntimeError('Cannot verify input for sql')

    return final

def typecheck(obj): 
    from collections import Iterable
    '''
    Checks if object is iterable and not string
    '''
    return not isinstance(obj, str) and isinstance(obj, Iterable)
