#!/usr/bin/env python
'''
Name  : Date Resolver,dateresolve.py
Author: Nickalas Reynolds
Date  : Fall 2017
Misc  : Resolves the date supplied to a more standard format, yields 
        an object that holds the orig date, utc, and the season
'''

# CHECK THIS!!!!!!!!

class date(object):

    def __init__(self,orig,local,tz=0):
        self.original = orig
        self.utc      = self.convutc()
        self.location = location(local,tz).main()
        self.season   = self.findseason()
        self.final    = '{}-{}'.format(self.utc,self.season)

    def get_params(self):
        return dir(self)

    def get_functions(self):
        return vars(self)

    def formatter(self):
        '''
        returns standard formatted date
        '''
    def convutc(self):
        '''
        converts date to utcformat
        YYYY-MM-DD-HH-MM-SS
        '''


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

        curr = self.utc.split('-')[1:2]
        for x in seasons:
            if curr[0] in '-'.join([seasons[x][0].split('-')[0],seasons[x][1].split('-')[0]]).split('-'):
                if self.location[1] == 'n':
                    self.season = seasons[x][2]
                else:
                    self.season = seasons[str((int(x)+3)%6)][2]
                break
