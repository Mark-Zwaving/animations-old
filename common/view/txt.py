# -*- coding: utf-8 -*-
'''Library contains texts for output to screen or to a file'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.1.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import math, re, config

# Answers option lists
quit = ['q','quit','stop']
yess = ['y','yes','yess','j','ja','ok','oke','oké','yee','jee', 'yep', 'yup', 'oui']
no   = ['n','no','nope','nee','nada','nein','non','neet', 'not']

line_hashtag = '#' * config.txt_line_width
line_hyphen  = '-' * config.txt_line_width

# Quick txt date lists
lst_m    = [str(i) for i in range(1,13)]
lst_mm   = [f'{m:0>2}' for m in lst_m]
lst_mmmm = ['january','februari','march','april','mai','june','july',
            'august','september','oktober','november','december']
lst_mmm  = [m[:3] for m in lst_mmmm]
lst_months_all = lst_m + lst_mm + lst_mmm + lst_mmmm

def month_name_to_num (name):
    ndx = 0
    for mmm, mmmm in zip(lst_mmm, lst_mmmm):
        if name in [mmm,mmmm]:
            return ndx
        ndx += 1
    else:
        return -1 # Name not found

# Short date related fn
m_to_mmmm  = lambda   i: lst_mmmm[int(i)-1] if str(i) in lst_m else -1
m_to_mmm   = lambda   i: lst_mmm[ int(i)-1] if str(i) in lst_m else -1
mm_to_mmmm = lambda  mm: lst_mmmm[int(mm)-1] if mm in lst_mm else -1
mm_to_mmm  = lambda  mm: lst_mmm[ int(mm)-1] if mm in lst_mm else -1
mmm_to_m   = lambda mmm: str(month_name_to_num(name))
mmm_to_mm  = lambda mmm: f'{month_name_to_num(name):0>2}'

def remove_dumb_whitespace( t ):
    '''Function removes excessive whitespaces from a text string'''
    t = re.sub('\n|\r|\t', '', str(t))
    t = re.sub('\s+', ' ', t)
    return t.strip()

def strip_all_whitespace(t):
    '''Function removes all whitespace from a text string'''
    return re.sub( '\t|\r|\n| |\s', '', str(t) )

def cleanup_whitespaces( t ):
    '''Function civilizes long text output with too much enters e.g.'''
    t = re.sub(r'\n+', '\n\n', t)
    t = re.sub('\t+|\s+', ' ', t)
    return t.strip()

def padding(t, align='center', spaces=0):
    '''Function aligns text on the screen'''
    t = str(t)
    if   align == 'center': t = f'{t:^{spaces}}'
    elif align == 'left':   t = f'{t:<{spaces}}'
    elif align == 'right':  t = f'{t:>{spaces}}'
    return t

def line_spacer( cnt=1 ):
    '''Function print enters to the screen'''
    t = ''
    while cnt >= 0: t += '\n'; cnt -= 1
    return t

def lst_columms(l, align='center', sep=' ', col=5, spaces=5):
    '''Function puts the elements in a list in colums'''
    t, lst = '', list(l)
    cnt = len(lst)
    for i in range(1,cnt):
        t += padding(l[i-1], align, spaces)
        t += '\n' if i % col == 0 and i != cnt else sep
    return t

def style( t='', type='none'):
    t = tr.t( t.strip().replace('  ', ' '))
    if   type in ['c','cap','capitalize']: t = t.capitalize()
    elif type in ['u','up','upper']: t = t.upper()
    elif type in ['l','low','lower']: t = t.lower()
    elif type in ['t','tit', 'title']: t = t.title()
    return t
