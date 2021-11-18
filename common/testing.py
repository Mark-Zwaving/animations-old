# -*- coding: utf-8 -*-
'''Common library with references to all the functions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.0.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import common, time
import config as cfg
import model.ymd as ymd
from view.console import log, log_r
import view.txt as txt
from model import util, animation
from control.fio import file_lst
import control.fio as fio
import model.animation as animation
################################################################################
# Playground test hard work
# common.model.utils.pause('04:42:00', '20211114')
#
# lmod = file_lst( cfg.dir_model, extensions = '',  keywords = 'ut', case_insensitive = True)
# log(lmod, True)
#
# lints = range(1000)
# for i in range(10):
#     log(util.rnd_el_lst(lints), True)
#     rnd = util.rnd_digit(1,3)
#     log(f'Wait for {rnd} seconds...', True)
#     time.sleep(rnd)
# lymd = ymd.yyyymmdd_range_lst(20211101, 20221100, True)
# old = '12:00:00'
# hms = ymd.hh_mm_ss_plus_second(old, second=7230 + 120)
# print(f'{old} -> {hms}')
# answ = common.control.ask.question('Hello whats your name?')
# print(f'Answer {answ}')
# util.pause('22:47:00', verbose = True)
#
# lst = range(1,100)
# lst = util.fisher_yates_shuffle_lst(lst, level=3)
# t = txt.lst_columms(lst, align='center', sep=' ', col=10, spaces=5)
# print(t)
# url = 'https://oud.weerplaza.nl/gdata/10min/GMT_TTTT_latest.png'
# paths = fio.download_interval(
#        url,          # Url for the files on the web
#        map           = cfg.dir_images, # Map for the downloads
#        interval      = 10,    # Interval time for downloading Images (minutes)
#        duration      = 1*10,  # Total time for downloading all the images (minutes)
#        date_submap   = True, # Set True to the possible given date submaps
#        date_subname  = True, # Add date and time to downloaded files
#        verbose       = True )
#
# path = util.mk_path(cfg.dir_images, f'{2021}/{11}/{15}/weerplaza')
# paths = imgs = file_lst( path, extensions=['.png'],  keywords = 'GMT',
#                  case_insensitive = True, verbose=False)
# fio.rm_lst(paths, remove_empty=True, verbose=True)
# path  = util.mk_path(cfg.dir_images, f'{2021}/{11}/{15}')
# paths = fio.file_lst( path, extensions=['.png'] )
# ok, path = animation.create(paths, verbose=True)
# if ok: util.compress_gif(path, verbose=True)
# fio.open_file_with_app(path, verbose=True)

#OK

url = 'https://oud.weerplaza.nl/gdata/10min/GMT_TTTT_latest.png'
paths = fio.download_interval(
       url,          # Url for the files on the web
       map           = cfg.dir_images, # Map for the downloads
       interval      = 10,    # Interval time for downloading Images (minutes)
       duration      = 10,    # Total time for downloading all the images (minutes)
       date_submap   = False, # Set True to the possible given date submaps
       date_subname  = False, # Add date and time to downloaded files
       verbose       = True
       )

print(paths)

t = util.process_time( delta_sec = time.time()-cfg.app_start_time)
log(f'\nTotal time app active is:  {t}', True)
