#!/usr/bin/env python

from distutils.core import setup

setup(name='plumber_analysis',
      version='0.01',
      description='Analysis package for PLUMBER data',
      author='Bart Nijssen',
      author_email='nijssen@uw.edu',
      url='http://www.github.com/bartnijssen/plumber_analysis',
      packages=['plumber'],
      py_modules=['plumber.io', 'plumber.plot', 'plumber.plumber',
                  'plumber.utils'],
     )
