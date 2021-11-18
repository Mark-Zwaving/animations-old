# -*- coding: utf-8 -*-
'''Common library with references to all the functions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.0.9'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config
import sys, os

# Config base sources maps
if config.dir_app not in sys.path:
    sys.path.append(config.dir_app)

import model.convert
import model.util
import model.ymd
import model.animation
import model.convert
import control.ask
import control.fio
import view.console
import view.txt

#
#
