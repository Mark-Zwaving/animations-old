# -*- coding: utf-8 -*-
'''Library for handling (easy) questions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.1.0'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import view.console as cnsl
import view.txt as txt
import model.util as util

question_mark = '\n  ?  '

def question(t='', spacer=True):
    t = f'{t}{question_mark}'
    answ = txt.remove_dumb_whitespace(input(t)) # Remove excessive whitespace
    if spacer: print(' ')
    return answ

def not_empty( t = '' ):
    while True:
        answ = question(t)
        if not answ:
            cnsl.log('Please type in something\n', True)
        else:
            break
    return answ

def is_quit( t = 'Press "q" to quit the programm' ):
    answ = not_empty(t).lower()
    if answ in txt.quit:
        return True
    else:
        return False

def exit( t = 'Press "q" to exit the programm' ):
    if is_quit(t):
        exit(0)

def open_with_app(path, verbose=False):
    cnsl.log(f'\n{txt.line_hashtag}', verbose)
    cnsl.log(f'File: {path}', verbose)
    t = 'Do you want to open the file with an (default) application'
    if is_yess(t):
        util.open_file_with_app(path, verbose)

def yess_or_no( t='' ):
    while True:
        answ = not_empty(t).lower()
        if answ in txt.yess:
            return answ
        elif answ in txt.no:
            return answ
        else:
            cnsl.log('Type in "y" for yess or "n" for no\n', True)

def is_yess( t=''):
    ln = '\n' if t else ''
    answ = not_empty(f'{t}{ln}Press a key to continue or press "y" for yess').lower()
    if answ in txt.yess:
        return True
    else:
        return False

def is_no( t='' ):
    ln = '\n' if t else ''
    answ = not_empty(f'{t}{ln}Press a key to continue or press "n" for no').lower()
    if answ in txt.no:
        return True
    else:
        return False

def number( t='Give a number'):
    while True:
        answ = not_empty( t )
        if answ.isdigit():
            return answ
        else:
            cnsl.log(f'Please type in a number', True)

def letter( t='Give a letter from a..z'):
    while True:
        answ = not_empty( t )
        if answ.isalpha():
            return answ
        else:
            cnsl.log(f'Please type in a letter', True)

def continue_on(t='Press a key to continue'):
    question(t)

def pause(t='Programm paused. Press a key to continue'):
    question(t)

def continue_or_quit( t='Press a key to continue or press "q" to quit' ):
    if question(t) in txt.quit:
        exit(0)
    return True


# END
