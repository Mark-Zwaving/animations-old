# -*- coding: utf-8 -*-
''' File contains examples for how to use the function from the anim library
    for downloading images from weerplaza.nl'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.0.7'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'
# Python version > 3.7 (fstring

import common.config as cfg # Configuration defaults. See config.py
import common.model.animation as anim  # import animation library
import threading, time # Multi processing and time

# Example download image urls from weerplaza
url_base_10min =  'https://oud.weerplaza.nl/gdata/10min' # Base url 10min
url_t10cm      = f'{url_base_10min}/GMT_T10C_latest.png' # Temp 10cm
url_weerbeeld  = f'{url_base_10min}/nl_10min.jpg'        # Weerbeeld
url_t2meter    = f'{url_base_10min}/GMT_TTTT_latest.png' # Temp 2 meter

def weerplaza_10min(url, verbose=None):
    '''Easy wrapper fn. For interval downloading images. With default values
       from config.py.'''
    interval_download_animation( url, # Give a downloadurl
        download_map      = cfg.dir_download,  # Map for downloading the images too
        animation_map     = cfg.dir_animation, # Map for the animations
        animation_name    = '',    # The path/name of the animation file
        interval_download = 10,    # Interval time for downloading Images (minutes)
        duration_download = 60,    # Total time for downloading all the images (minutes)
        animation_time    = 0.7,   # Animation interval time for gif animation
        remove_download   = False, # Remove the downloaded images
        gif_compress      = True,  # Compress the size of the animation
        date_submap       = True,  # Set True to create extra date submaps
        date_subname      = True,  # Set True to create extra date in files
        check             = False, # No double downloads check
        verbose           = False  # Overwrite verbose -> see config.py
    )

if __name__ == "__main__":
    ############################################################################
    # Weerplaza eg: 10 minutes refresh images
    # EG. Temp 2 meter
    # interval_download_animation( url_t2meter, # Give a downloadurl
    #     download_map      = cfg.dir_download,  # Map for downloading the images too
    #     animation_map     = cfg.dir_animation, # Map for the animations
    #     animation_name    = '',    # The path/name of the animation file
    #     interval_download = 10,    # Interval time for downloading Images (minutes)
    #     duration_download = 60,    # Total time for downloading all the images (minutes)
    #     animation_time    = 0.7,   # Animation interval time for gif animation
    #     remove_download   = False, # Remove the downloaded images
    #     gif_compress      = True,  # Compress the size of the animation
    #     date_submap       = True,  # Set True to create extra date submaps
    #     date_subname      = True,  # Set True to create extra date in files
    #     check             = True,  # No double downloads check
    #     verbose           = None   # Overwrite verbose -> see config.py
    # )

    # See above
    # anim time, rm downloads, compress gif, date submap, date subname, check download, verbose
    at, rm, cp, ds, dn, ck, vb = 0.7, False, True, True, True, True, True
    dm, am = cfg.dir_download, cfg.dir_animation # Base maps (shortened)
    nm = 'wp_animation_temp.gif' # Name file
    it = 10  # interval time (minutes)
    du = 10  # duration time (minutes)
    anim.interval_download_animation(url_t2meter, dm, am, nm, it, du, at, rm, cp, ds, dn, ck, vb)

    # ############################################################################
    # # Example multi processing. Download multiple images at the same time
    #
    # # Clock timer set to False. Cannot have multiple timers at the same time
    # cfg.timer = False  # Timer is off (=false)
    #
    # # Start 3 threads for downloading three images at the same time
    # for url in [ url_t10cm, url_weerbeeld, url_t2meter ]: # Three images for downloading
    #     threading.Thread( target=weerplaza_10min, args=(url,) ).start() # Start new process
    #     time.sleep(30) # Start another thread after 20 seconds
