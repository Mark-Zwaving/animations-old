# -*- coding: utf-8 -*-
''' File contains functions for downloading files from the internet and
    making gif animations based on files (images)'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.1.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'
# Python version > 3.7 (fstring)

# Import libraries
import config as cfg
import os, imageio, requests, urllib.request, datetime, time, shutil
import threading, time
import control.ask  as ask
import control.fio  as fio
import view.console as cnsl
import model.util   as util
import model.ymd    as ymd
import model.validate as validate

# Function creates an image animation
def create(
        lst          = [],  # List with all the images for the animation
        path         = '',   # File path for the animation image
        interval     = 0.7,  # Interval time for the image
        verbose      = None # Optional overwrite default value verbose -> see config.py
    ):
    '''Function create an anmiation file, using python library imageio'''
    ok = False
    cnsl.log(f'Start make animation {ymd.now()}', verbose)
    cnsl.log(f'Animation interval time is {interval} seconds', verbose)
    if lst:
        # Make path
        if path:
            dir = os.path.dirname(path)
            name, _ = util.name_ext(path)
        else: # Make a name and get default map
            y, m, d, hh, mm, ss = ymd.y_m_d_h_m_s_now()
            dir, name = cfg.dir_animation, f'animation_{y}-{m}-{d}_{hh}-{mm}-{ss}'

        path = util.mk_path(dir, f'{name}.gif')
        cnsl.log(f'Animation path is {path}', verbose)

        try: # Read list image data, only existing file
            cnsl.log(f'Process and verify images for animation', verbose)
            data = [imageio.imread(p) for p in lst if validate.image(p, verbose)]
            if data:
                fio.mk_dir(dir, verbose) # Always make path before saving
                cnsl.log(f'Start make animation\nPath {path}', verbose)
                imageio.mimsave(path, data, duration=interval) # Make animation
            else:
                raise Exception('List data images is empty. File paths incorrect or files corrupt?')
        except Exception as e:
            cnsl.log(f'Error making an animation\n{e}', cfg.error)
        else:
            cnsl.log('Make animation success', verbose)
            ok = True
    else:
        cnsl.log('Cannot create an animation. List images are empty.', cfg.error)
    cnsl.log('End make animation', verbose)
    return ok, path

# Makes a animation of downloaded images

def interval_download_animation(
        download_url,     # Give a downloadurl
        download_map      = cfg.dir_download,    # Map for downloading the images too
        animation_map     = cfg.dir_animation,   # Map for the animations
        animation_name    = '',    # The path/name of the animation file
        interval_download = 10,    # Interval time for downloading Images (minutes)
        duration_download = 60,    # Total time for downloading all the images (minutes)
        animation_time    = 0.7,   # Animation interval time for gif animation
        remove_download   = False, # Remove the downloaded images
        gif_compress      = True,  # Compress the size of the animation
        date_submap       = True,  # Set True to create extra date submaps
        date_subname      = True,  # Set True to create extra date in files
        check             = True,  # No double downloads check
        verbose           = None  # With output to screen
    ):
    '''Function downloads images for a given time and creates a animation from
       the downloaded images'''
    ok = False
    cnsl.log(f'Start interval download and make an animation {ymd.now()}', verbose)
    cnsl.log(f'Url is {download_url}', verbose)
    cnsl.log(f'Download interval {interval_download} minutes', verbose)
    cnsl.log(f'Download duration {duration_download} minutes', verbose)
    cnsl.log(f'Compress animation {gif_compress}', verbose)
    cnsl.log(f'With date submaps {date_submap}', verbose)
    cnsl.log(f'With date subname {date_subname}', verbose)
    cnsl.log(f'Animation time {animation_time} seconds', verbose)
    cnsl.log(f'Remove downloaded images {remove_download}\n', verbose)

    # Start interval downloads
    paths = fio.download_interval(
                    download_url, download_map, interval_download,
                    duration_download, date_submap, date_subname,
                    check, verbose )

    # Make animation name
    web_name = util.url_name(download_url)
    id_name, _  = util.name_ext(download_url)
    if not animation_name:
        animation_name = f'animation_{web_name}_{id_name}'
    else:
        animation_name, _ = util.name_ext(animation_name)
    if date_subname: # Add date time to animation name
        y, m, d, hh, mm, ss = ymd.y_m_d_h_m_s_now()
        animation_name += f'_{y}-{m}-{d}_{hh}-{mm}-{ss}'

    # Make animation map
    if date_submap: # Add date to aninmation map
        y, m, d = ymd.yyyy_mm_dd_now()
        animation_map = util.mk_path(animation_map, f'{y}/{m}/{d}')
    animation_map = util.mk_path(animation_map, web_name) # Add web id to path

    # Animation path
    path = util.mk_path(animation_map, f'{animation_name}.gif')

    # Make animation
    ok, path = create(paths, path, animation_time, verbose)

    # Compress animation
    if ok and gif_compress: util.compress_gif(path)

    # Remove downloaded images
    if remove_download: fio.rm_lst(paths)

    cnsl.log('End download images and make an animation', verbose)
    return ok, path
