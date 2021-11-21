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
def process(
        s,            # String to print on the screen
        verbose=None,  # If set to True it always prints on a screen
        log=None,     # Overwrite default log
        debug=None    # Overwrite default debug
    ):
    '''Function processes logging processes'''
    if verbose == None: # No overwrite, use default
        if config.verbose:
            print(s)
    elif verbose: # Overwrite default config
        print(s)

    if debug == None: # No overwrite, use default
        if config.debug: # Debug modus
            input(s)
    elif debug:
        input(s)

    # Write log if selected
    if log == None:  # No overwrite, use default
        if config.log:
            write_log(s)
    elif log:
        write_log(s)


def log(
        s,            # String to print on the screen
        verbose=None,  # If set to True it always prints on a screen
        log=None,     # Overwrite default log
        debug=None    # Overwrite default debug
    ):
    '''Function shows output sstring (s) on screen based on variable verbose and debug.
       Output always to screen, set variable always to True.
       If debug set to True it wait for keypress to move on.'''
    s = str(s)
    process( s, verbose, log, debug )


def log_r(
        s,            # String to print on the screen
        verbose=None,  # If set to True it always prints on a screen
        log=None,      #
        debug=None
    ):
    '''Function shows output string (s) --- on the same line --- based on the
       variable verbose. Output always to screen, set variable always to True.'''
    s = f'\r{s}'

    if verbose == None: # No overwrite, use default
        if config.verbose:
            print(s, end='')
    elif verbose: # Overwrite default config
        print(s, end='')

    if debug == None: # No overwrite, use default
        if config.debug: # Debug modus
            input(s)
    elif debug:
        input(s)

    # Write log if selected
    if log == None:  # No overwrite, use default
        if config.log:
            write_log(s)
    elif log:
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
