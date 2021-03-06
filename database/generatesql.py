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

for i,j in enumerate(stars):
    for x,y in enumerate(j):
        if x == 3:
            if len(y.split(':')) == 3:
                temp0,temp1,temp2 = map(float,y.split(':'))
                total = abs(temp0) + temp1/60. + temp2/3600
            else:
                temp0,temp1 = map(float,y.split(':'))
                temp2 = temp1/60. - temp1
                total = abs(temp0) + temp1/60. + temp2/3600
            if temp0 < 0.:
                total = total * -1
            stars[i][x] = str(total)
        elif x == 4:
            if len(y.split(':')) == 3:
                temp0,temp1,temp2 = map(float,y.split(':'))
                total = abs(temp0) + temp1/60. + temp2/3600
            else:
                temp0,temp1 = map(float,y.split(':'))
                temp2 = temp1/60. - temp1
                total = abs(temp0) + temp1/60. + temp2/3600
            if temp0 < 0.:
                total = total * -1
            stars[i][x] = str(total)
            break

try:
    con = lite.connect('star.sql')
    cur = con.cursor()   
    cur.execute('DROP TABLE IF EXISTS db')
    cur.execute('CREATE TABLE db(NAME1 TEXT, NAME2 TEXT, TYPE TEXT, RA FLOAT, DEC FLOAT, EPOCH INT, FLUXT TEXT, FLUXV FLOAT, TIMEVISIBLE TEXT,LASTUPDATED INT)')
    for x in stars: 
        cur.execute("INSERT INTO db VALUES('{}','{}','{}',{},{},{},'{}',{},'{}',{})".format(x[0],x[1],x[2],float(x[3]),float(x[4]),int(x[5]),x[6],float(x[7]),x[8],int(x[9])))
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

for i,j in enumerate(locations):
    for x,y in enumerate(j):
        if x == 1:
            temp0,temp1,temp2 = map(float,y.split(':'))
            total = abs(temp0) + temp1/60. + temp2/3600
            if temp0 < 0.:
                total = total * -1
            locations[i][x] = str(total)

        elif x == 2:
            temp0,temp1,temp2 = map(float,y.split(':'))
            total = abs(temp0) + temp1/60. + temp2/3600
            if temp0 < 0.:
                total = total * -1
            locations[i][x] = str(total)
            break

try:
    con = lite.connect('location.sql')
    cur = con.cursor()   
    cur.execute('DROP TABLE IF EXISTS db')
# Name             LAT(N)      LONG(W)    UTC DST(Y/N) LastUpdated
    cur.execute('CREATE TABLE db(NAME1 TEXT, LAT FLOAT, LONG FLOAT, UTC INT,HEIGHT FLOAT,LASTUPDATE INT)')
    for x in locations: 
        #print(len(x))
        #print(x)
        cur.execute("INSERT INTO db VALUES('{}',{},{},{},{},{})".format(x[0],float(x[1]),float(x[2]),int(x[3]),float(x[4]),int(x[5])))

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
