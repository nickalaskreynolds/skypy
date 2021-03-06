#!/usr/bin/env python
'''
Name    : Config, config.py
Author  : Nickalas Reynolds
Date    : Fall 2017
Misc    : File handles reading in the configuration file and 
          for writing an example configuration file
Example : defaultconfig.py
'''

# imported standard modules
from os.path import isfile
from os import getcwd,remove
from sys import exit
from shutil import copyfile
from inspect import getfile
from importlib import import_module
from time import time as ctime

# import custom modules
from .colours import colours
from ..version import *

# checking python version
assert assertion()
__version__ = package_version()

# main class object for manipulating configuration files
class configuration(object):

    def __init__(self,inputfile=None,cwd=None):
        """
        Initialize the configuration class
        """

        self.time = '{}'.format(str(ctime()).split('.')[0])

        if cwd == None:
            self.cwd = getcwd()
        else:
            self.cwd = cwd

        self.params = None
        if inputfile == None:
            raise RuntimeError('Configuration file not specified, refer to example...')
        else:
            self.inputfile=self.remove_ext(self.find_file(inputfile))

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

    def read(self):
        """
        read the input file
        """
        temp = vars(import_module(self.inputfile))
        mainlibs=['time','numpy','scipy','version','datetime','os','sys']
        b = {}
        for i in temp:
            if (i.split('.')[0] not in mainlibs) and ('__' not in i):
                b[i] = temp[i]
        self.params = b
        if self.remove:
            remove('{}/{}.py'.format(self.cwd,self.inputfile))

    def get_params(self):
        """
        Return the parameters from the input file
        """
        return self.params

    def get_dir(self):
        """
        Return the directory where file was pulled
        """
        return self.directory


    def set_params(self,**kwargs):
        """
        Set the parameters in the object
        Only if param exists
        """
        if kwargs is not None:
            if self.params != None:
                temp = self.params
            for key, value in kwargs.items():
                if self.verify_params(key):
                    temp[key] = value

            self.params = temp

    def add_params(self,**kwargs):
        """
        Add new parameters in the object
        Only if param doesn't exist
        """
        if kwargs is not None:
            if self.params != None:
                temp = self.params
            for key, value in kwargs.items():
                if not self.verify_params(key):
                    temp[key] = value

            self.params = temp

    def verify_params(self,*args):
        """
        Verify that the keyword arguments are 
        within the configuration file
        """
        dictkeys = [x for x in self.params]
        for k in args:
            if k not in dictkeys:
                return False
            else:
                pass
        return True

    def remove_ext(self,inputfile):
        """
        Remove File extensions
        """
        return inputfile.strip('.py')

    def find_file(self,inputfile):
        '''
        Find the input file and make sure it is in current directory
        '''
        if isfile(inputfile):
            dest = "{}/config_{}.py".format(self.cwd,self.time)
            self.directory = '/'.join(inputfile.split('/')[:-1])
            if self.directory == '':
                self.directory = self.cwd
            copyfile(inputfile,dest)
            self.remove = True
        else:
            raise RuntimeError('Input file not found: {}'.format(inputfile))
        return dest.split('/')[-1]

if __name__ == "__main__":
    print('Testing module\n')
    print("{}".format(__doc__))
