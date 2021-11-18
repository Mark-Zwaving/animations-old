# -*- coding: utf-8 -*-
'''Library contains functions for converting elements'''
__author__     = 'Mark Zwaving'
__email__      = 'markzwaving@gmail.com'
__copyright__  = 'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    = 'MIT License'
__version__    = '0.4.5'
__maintainer__ = 'Mark Zwaving'
__status__     = 'Development'

import config as cfg

# Convert temperatures
celsius_to_fahrenheit = lambda c:   float(c) * 1.8 + 32.0
celsius_to_kelvin     = lambda c:   float(c) + 273.15
fahrenheit_to_celsius = lambda f: ( float(f) - 32.0 ) / 1.8
fahrenheit_to_kelvin  = lambda f: ( float(f) + 459.67 ) / 1.8
kelvin_to_celsius     = lambda k:   float(k) - 273.15
kelvin_to_fahrenheit  = lambda k:   float(k) * 1.8 - 459.67

# Convert distance/length
inch_to_cm     = lambda i:   float(i) * 2.54
cm_to_inch     = lambda c:   float(c) / 2.54
feet_to_cm     = lambda f:   float(f) * 30.48
cm_to_feet     = lambda c:   float(c) / 30.48
inc_to_feet    = lambda i:   float(i) / 12.0
feet_to_inch   = lambda f:   float(f) * 12.0
yard_to_feet   = lambda y:   float(y) * 3.0
feet_to_yard   = lambda y:   float(y) / 3.0
mile_to_km     = lambda m:   float(m) * 1.60930
km_to_mile     = lambda k:   float(k) / 1.60930
nautmile_to_km = lambda s:   float(s) * 1.85  # Nautical miles/seamiles
km_to_nautmile = lambda f:   float(f) / 1.85
yard_to_cm     = lambda y:   float(y) * 91.44
cm_to_yard     = lambda c:   float(c) / 91.44

# Default dpi in matplotlib is 100. See cfg.py
pixel_to_inch = lambda pixel, dpi=100.0: float(pixel) / float(dpi)

bytes_ascii_to_str = lambda b: bytes_to_str(b, 'ascii', 'ignore')
bytes_utf8_to_str  = lambda b: bytes_to_str(b, 'utf-8', 'ignore')

def str_to_bytes( s, charset, errors ):
    try:
        b = s.encode(encoding=charset, errors=errors)
    except Exception as e:
        console.log(f'Error convert string to bytes charset {charset}\n{e}', cfg.error)
    else:
        return b
    return s

def bytes_to_str( b, charset, errors ):
    try:
        s =  b.decode(encoding=charset, errors=errors)
    except Exception as e:
        console.log(f'Error convert bytes to string charset {charset}\n{e}', cfg.error)
    else:
        return s
    return b

def ms_to_bft( ms ):
    i = int(ms)
    if   i <   3: return '0'
    elif i <  16: return '1'
    elif i <  34: return '2'
    elif i <  55: return '3'
    elif i <  80: return '4'
    elif i < 108: return '5'
    elif i < 139: return '6'
    elif i < 172: return '7'
    elif i < 208: return '8'
    elif i < 245: return '9'
    elif i < 285: return '10'
    elif i < 327: return '11'
    else: return '12'

def octa_to_txt(octa):
    i = int(octa)
    if   0 == i: return 'Onbewolkt'
    elif 1 == i: return 'Vrijwel onbewolkt'
    elif 2 == i: return 'Licht bewolkt'
    elif 3 == i: return 'Half bewolkt'
    elif 4 == i: return 'Half bewolkt'
    elif 5 == i: return 'Half tot zwaar bewolkt'
    elif 6 == i: return 'Zwaar bewolkt'
    elif 7 == i: return 'Vrijwel geheel bewolkt'
    elif 8 == i: return 'Geheel bewolkt'
    elif 9 == i: return 'Bovenlucht onzichtbaar'
    else: return ''

def deg_to_txt(deg):
    i = int(deg)
    if   i ==  0:  return 'quiet'
    elif i  < 22:  return 'north'
    elif i  < 30:  return 'north-north-east'
    elif i  < 67:  return 'north-east'
    elif i  < 112: return 'east'
    elif i  < 157: return 'south-east'
    elif i  < 202: return 'south'
    elif i  < 247: return 'south-west'
    elif i  < 292: return 'west'
    elif i  < 337: return 'north-west'
    elif i  < 360: return 'north'
    elif i == 990: return 'variable'
    else: return ''

def ms_to_txt( ms ): # TODO
    i = int(ms)
    if   i <   3: return 'windstil'
    elif i <  16: return 'zwakke wind'
    elif i <  34: return 'zwakke wind'
    elif i <  55: return 'matige wind'
    elif i <  80: return 'matige wind'
    elif i < 108: return 'vrij krachtige wind'
    elif i < 139: return 'krachtige wind'
    elif i < 172: return 'harde wind'
    elif i < 208: return 'stormachtige wind'
    elif i < 245: return 'storm'
    elif i < 285: return 'zware storm'
    elif i < 327: return 'zeer zware storm'
    else: return 'orkaan'

def vvn_to_txt( vvn ):
    i = int(vvn)
    if   i <= 49: return f'{i*100} - {(i+1)*100} meter' # 1:100-200 m ... 49:4900-5000 m
    elif i == 50: return '5 - 6 km' # 50:5-6 km
    elif i <= 79: return f'{i-50} - {i-49} km' # 56:6-7 km ... 79:29-30 km
    elif i  < 89: return f'{(i-80)*5+30} - {(i-79)*5+30} km' #  80:30-35 km ... 87:65-70 km
    elif i == 89: return '< 70 km' # 89: >70 km
    return vvn

def timespan1hour(h):
    i = int(h)
    return f'{i-1} - {i} hour'

def timespan6hour(u):
    i = int(u)
    if   i ==  6: s = '0 - 6'
    elif i == 12: s = '6 - 12'
    elif i == 18: s = '12 - 18'
    elif i == 24: s = '18 - 24'
    else: s = u
    return f'{s} hour'
