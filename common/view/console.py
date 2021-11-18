# -*- coding: utf-8 -*-
'''Library contains a log function'''

__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.7'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config, os, threading
import control.fio as fio
import model.ymd as ymd

################################################################################
# Functions handling outputs to screen or log
def log(
        s,            # String to print on the screen
        always=False  # If set to True it always prints on a screen
    ):
    '''Function shows output sstring (s) on screen based on variable verbose and debug.
       Output always to screen, set variable always to True.
       If debug set to True it wait for keypress to move on.'''
    s = str(s)
    if config.debug: # Debug modus
        input(s)
    elif config.verbose or always: # Verbose modus
        print(s)

    # Write log if selected
    if config.log:
        write_log(s)

def log_r(
        s,            # String to print on the screen
        always=False  # If set to True it always prints on a screen
    ):
    '''Function shows output string (s) --- on the same line --- based on the
       variable verbose. Output always to screen, set variable always to True.'''
    s = f'\r{s}'
    if config.debug: # Debug modus
        input(s) # untested
    elif config.verbose or always:
        print(s, end='')

    # Write log if selected
    if config.log:
        write_log(s)

def write_log(s):
    '''Function writes a log from console output'''
    ok = False
    with threading.Lock():
        mem_log, mem_verbose = config.log, config.verbose # Remember values
        config.log, config.verbose = False, False # No write or log to screen
        log_name = config.log_name if config.log_name else f'log_common_{ymd.yyyymmdd_now()}.log'
        path = os.path.join(config.dir_log, log_name)
        ok = fio.write(path, f'{s}\n', 'a')
        config.log, config.verbose = mem_log, mem_verbose # Set back values
    return ok

def verbose(verbose=False):
    '''Function checks parameter if set to True itoverrides the default verbose
       initialization from config.py'''
    return verbose if verbose else config.verbose
