'''Library contains functions for validation'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.0.7'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import datetime, os
import config as cfg
import model.ymd as ymd
import view.console as cnsl
from PIL import Image

def image(path, verbose=False):
    '''Function validates an image'''
    ok, verbose = False, cnsl.verbose(verbose)
    cnsl.log(f'Start validate image at {ymd.now()}', verbose)
    cnsl.log(f'Image {path}', verbose)
    try:
        if os.path.exists(path):
            if os.path.isfile(path):
                if image_corrupt(path):
                    raise Exception(f'Image is corrupt')
            else:
                raise Exception(f'Image is not a file')
        else:
            raise Exception(f'Image does not exist')
    except Exception as e:
        cnsl.log(f'Validation error: {e}', verbose)
    else:
        cnsl.log('Image seems to be ok', verbose)
        ok = True
    cnsl.log(f'End validate image', verbose)
    return ok

def image_corrupt(path, verbose=False):
    '''Function checks is a file is corrupt returns True if it is else False'''
    corrupt = False
    try: Image.open(path).verify() # Open and verify
    except Exception as e:
        cnsl.log(f'Error file {path} is corrupt', verbose)
        corrupt = True
    return corrupt

# Function checks extensions
def extension(
        ext  # Extension of image to validate
    ):
    '''Function checks extensions for validity and adds a dot if needed'''
    if ext:
        if ext[0] != '.':
            ext = f'.{ext}'
    return ext

def float( val ):
    ok = True
    try:
        if val is None:
            ok = False
        elif is_nan(val):
            ok = False
        else:
            f = float(val)
    except Exception as e:
        cnsl.log(f'Digit {val} is no float.', cfg.error)
        ok = False

    return ok

def date( dt ):
    try:
        datetime.datetime.strptime(dt, '%Y%m%d')
    except ValueError:
        return False
    else:
        return True

def yyyymmdd(
        yyyymmdd, # Date
        verbose = False
    ):
    '''Function validates a date with format yyyymmdd for existence'''
    ok, verbose, symd = False, cnsl.verbose(verbose), str(yyyymmdd)
    cnsl.log(f'Start validate date at {ymd.now()}', verbose)
    cnsl.log(f'Date - {symd} - format <yyyymmdd>', verbose)
    if len(symd) != 8:
        cnsl.log('Date has wrong length. Correct length must be 8', verbose)
    elif not symd.isdigit():
        cnsl.log('Date must only contain digits', verbose)
    elif int(symd) > int(ymd.yyyymmdd_now()):
        cnsl.log('Date is in the future. Try again later... ;-)', verbose)
    else:
        try:
            y, m, d = ymd.split_yyyymmdd(symd)
            d = datetime.datetime( int(y), int(m), int(d) )
        except Exception as e:
            cnsl.log(f'Error in date\n{e}', verbose)
        else:
            cnsl.log('Validate date success', verbose)
            ok = True
    cnsl.log('End validate date', verbose)
    return ok

def is_nan( val ):
    ok = False
    try:
        if val != val:
            ok = True
        elif val == np.isnan:
            ok = True
        elif np.isnan(val):
            ok = True
        elif math.isnan(val):
            ok = True
    except Exception as e:
        pass
    return ok
