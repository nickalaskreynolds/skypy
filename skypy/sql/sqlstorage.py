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
    '''
    To call:
    a= sql.(dir,file)
    a.calldb()
    a.writedb()
    a.db_selsort()
    a.db_delete()
    a.closedb()
    '''

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
            return False

    def calldb(self):
        '''
        Connect to DB
        '''
        self.db = sqlite3.connect(self.dbdir)
        self.sb = self.db.cursor() 

    def savedb(self):
        '''
        commit changes
        '''
        self.sb.commit() 

    def resetdb(self):
        '''
        reset the db
        '''
        self.db.rollback()

    def updatedb(self,findcol,findvalue,col,value):
        '''
        Update a db column (col) to value (value) where you match in findcol to findvalue
        By nature of programming, findvalue must be a string
        '''
        assert check_sql_input(col) and check_sql_input(findcol) and check_sql_input(findvalue)
        if type(value) == str:
            assert check_sql_input(value)
            self.sb.execute("UPDATE db set `%s` = '%s' where `%s` =  '%s'" % (col,value,findcol,findvalue))
        elif type(value) == float:
            self.sb.execute("UPDATE db set `%s` = %f where `%s` =  '%s'" % (col,value,findcol,findvalue))
        elif type(value) == int:
            self.sb.execute("UPDATE db set `%s` = %d where `%s` =  '%s'" % (col,value,findcol,findvalue))

    def writedb(self,db,x):
        '''
        Write to DB
        star uses    : name1, name2, type, ra, dec, epoch, ftype,fval, visible, lastupdate (10)
        location uses: name, lat, long, tz, T/F for DST, lastupdate                        (6)
        '''
        # protect against sql injection
        delimiters = ['>','|',';',' ','\\','[',']','{','}']
        assert typecheck(x) and (((len(x) == 10) or (len(x) == 6)) and (not typecheck(x[0])))
        for y in delimiters:
            assert len(str(x[0]).split(y)) == 1
        if db == 'star':
            self.sb.execute("INSERT INTO db VALUES ('{}','{}','{}',{},{},{},'{}',{},'{}',{})".format(x[0],x[1],x[2],float(x[3]),float(x[4]),int(x[5]),x[6],float(x[7]),x[8],int(x[9])))
        elif db == 'location':
            self.sb.execute("INSERT INTO db VALUES('{}',{},{},{},'{}',{})".format(x[0],float(x[1]),float(x[2]),int(x[3]),x[4],int(x[5])))

    def db_sel(self,col1,value):
        '''
        Search an open DB, single value select
        '''
        assert check_sql_input(col1) and check_sql_input(value)
        self.sb.execute("SELECT * FROM db WHERE `%s` like '%s'" % (col1,value))
        return self.sb.fetchall()

    def db_ssort(self,col1,top,order='asc'):
        '''
        Search an open DB, single column sort, pulling top values
        '''
        assert check_sql_input(col1) and check_sql_input(order)
        #                                                   col1 order   top
        cursor = self.sb.execute("SELECT * FROM db ORDER BY `%s` %s LIMIT %d" % (col1,order.upper(),int(top)))

        return [x for x in cursor]

    def db_dsort(self,col1,col2,top,order=['asc','asc']):
        '''
        Search an open DB, double column sort, pulling top values
        '''
        assert check_sql_input(col1) and check_sql_input(col2) and check_sql_input(order[0]) and check_sql_input(order[1])
        #                                                  col1 ordercol2  order   top
        cursor = self.sb.execute("SELECT * FROM db ORDER BY `%s` %s ,`%s` %s LIMIT %d" % (col1,order[0].upper(),col2,order[1].upper(),int(top)))
        return [x for x in cursor]

    def db_selsort(self,col1,value,col2,top,order='asc'):
        '''
        Search an open DB,Select from column, order by another, limit results
        '''
        assert check_sql_input(col1) and check_sql_input(value) and check_sql_input(col2) and check_sql_input(order)
        #                                                 col1    value        col2 order      top
        cursor = self.sb.execute("SELECT * FROM db WHERE `%s` like '%s' ORDER BY `%s` %s LIMIT %d" % (col1,value,col2,order.upper(),int(top)))
        return [x for x in cursor]

    def db_delete(self,col,name):
        '''
        Delete from Database
        '''
        assert check_sql_input(col) and check_sql_input(name)
        assert col in ['Name1','Name2','Name']
        self.sb.execute("DELETE from db where `%s` = '%s'" % (col,name))
        print('Total rows deleted: {}'.format(self.db.total_changes))

    def closedb(self):
        '''
        Close DB
        '''
        if self.db:
            self.db.close()

def check_sql_input(current):
    '''
    Protect against injection
    '''
    return len(current.split(' ')) == 1

def typecheck(obj): 
    from collections import Iterable
    '''
    Checks if object is iterable and not string
    '''
    return not isinstance(obj, str) and isinstance(obj, Iterable)
