#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import numpy as np
import sys

try:
    stars = np.loadtxt('starlist.txt.backup',skiprows=11,dtype=str)
except:
    print('If file not found, go to https://github.com/nickalaskreynolds/skypy.git/database/ and grab file')
    sys.exit(1)

try:
    con = lite.connect('star.sql')
    cur = con.cursor()   
    cur.execute('DROP TABLE IF EXISTS db')
    cur.execute('CREATE TABLE db(Name1 TEXT, Name2 TEXT, Type TEXT, RA TEXT, DEC TEXT, EPOCH INT, FluxT TEXT, FluxV FLOAT,lastupdate INT)')
    for x in stars: 
        cur.execute("INSERT INTO db VALUES('{}','{}','{}','{}','{}',{},'{}',{},{})".format(x[0],x[1],x[2],x[3],x[4],int(x[5]),x[6],float(x[7]),int(x[8])))
    con.commit()
    
except lite.Error as e:
    
    if con:
        con.rollback()
        
    print("Error %s:" % e.args[0])
    sys.exit(1)
    
finally:
    
    if con:
        con.close() 

con = lite.connect('star.sql')
cur = con.cursor()   
with con:    
    cur = con.cursor()    
    cur.execute("SELECT * FROM db")

    rows = cur.fetchall()

    for row in rows:
        print(row)


try:
    locations = np.loadtxt('location.txt.backup',skiprows=3,dtype=str)
except:
    print('If file not found, go to https://github.com/nickalaskreynolds/skypy.git/database/ and grab file')
    sys.exit(1)

try:
    con = lite.connect('location.sql')
    cur = con.cursor()   
    cur.execute('DROP TABLE IF EXISTS db')
# Name             LAT(N)      LONG(W)    UTC DST(Y/N) LastUpdated
    cur.execute('CREATE TABLE db(Name1 TEXT, Lat TEXT, Long TEXT, UTC INT, DST TEXT,lastupdate INT)')
    for x in locations: 
        #print(len(x))
        #print(x)
        cur.execute("INSERT INTO db VALUES('{}','{}','{}',{},'{}',{})".format(x[0],x[1],x[2],int(x[3]),x[4],int(x[5])))

    con.commit()
    
except lite.Error as e:
    
    if con:
        con.rollback()
        
    print("Error %s:" % e.args[0])
    sys.exit(1)
    
finally:
    
    if con:
        con.close() 

con = lite.connect('location.sql')
cur = con.cursor()   
with con:    
    cur = con.cursor()    
    cur.execute("SELECT * FROM db")

    rows = cur.fetchall()

    for row in rows:
        print(row)
