# -*- coding: utf-8 -*-
''' File contains examples for how to use the function from the anim library
    for downloading images from knmi.nl'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.0.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'
# Python version > 3.7 (fstring)

import common.config as cfg # Configuration defaults. See config.py
import common.model.animation as anim  # import animation library
import common.model.ymd as ymd
import common.model.util as util
import common.control.fio as fio
import common.view.console as cnsl
import threading, time # Multi processing and time

# Base knmi download url for 10 min images
base_url_10min  = 'https://cdn.knmi.nl/knmi/map/page/weer/actueel-weer/'

# KNMI download image urls
url_windforce   = f'{base_url_10min}windkracht.png'
url_windspeed   = f'{base_url_10min}windsnelheid.png'
url_windmax     = f'{base_url_10min}maxwindkm.png'
url_temperature = f'{base_url_10min}temperatuur.png'
url_rel_moist   = f'{base_url_10min}relvocht.png'
url_view        = f'{base_url_10min}zicht.png'

def daily_interval_knmi_10min(
        download_url      = url_temperature, # Download image url
        start_time        = '09:00:00', # Start time to download an image (every day)
        duration          = 8*60,  # Time to download images
        interval          = 10,    # Interval time for downloading Images (minutes)
        start_date        = '',    # <optional> Start date for downloading images format yyyymmdd
        stop_date         = '',    # <optional> Give an end date format: yyyymmdd
        download_map      = cfg.dir_download,  # <optional> Map for downloading the images too
        animation_map     = cfg.dir_animation, # <optional> Map for the animations
        animation_name    = '',    # <optional> The path/name of the animation file
        animation_time    = 0.7,   # <optional> Animation interval time for gif animation
        remove_download   = False, # <optional> Remove the downloaded images
        gif_compress      = True,  # <optional> Compress the size of the animation
        date_submap       = True,  # <optional> Set True to create extra date submaps
        verbose           = None  # <optional> Overwrite verbose -> see config.py
    ):
    '''Function handles repetative daily downloads and makes the animations'''
    ok, st = False, time.time()
    web_name = util.url_name(download_url)
    cnsl.log(f'Start {web_name} daily interval download {ymd.now()}', verbose)

    if not start_date: # Get the current start date if not given
        start_date = ymd.yyyymmdd_now()

    # Start loop
    name, _ = util.name_ext(download_url)
    while True:
        # Wait untill start time and start date
        util.pause(start_time, start_date, f'start download {name} at')

        # Start interval download for url
        anim.interval_download_animation(
                download_url, download_map, animation_map, animation_name, interval,
                duration, animation_time, remove_download, gif_compress, date_submap,
                True,  # Date subname always True
                True,  # Dont download double
                verbose )

        # Make a new correct new date
        y, m, d, hh, _, _ = ymd.y_m_d_h_m_s_now() # Get current date and time
        act_date = f'{y}{m}{d}' # Current date
        if int(act_date) > int(start_date): # Next day is there
            hours = int(start_time.split(':')[0])
            if hours > int(hh): # Passed the start_time
                start_date = ymd.yyyymmdd_plus_day() # Get the next day
            else:
                start_date = ymd.yyyymmss_now() # Get the current day
        else: # We are still on the same day
           start_date = ymd.yyyymmdd_plus_day() # Get the next day

        # Check end date if there
        if stop_date: # Check to stop
            if int(start_date) > int(stop_date): # Last day is passed
                break # Break loop

    cnsl.log(f'End {web_name} daily interval download', verbose)


if __name__ == "__main__":
    ############################################################################
    # Example: 10 minutes refresh images base example
    # Temp 2 meter
    # interval_download_animation( url_temperature,     # Give a downloadurl
    #     download_map      = cfg.dir_download,    # Map for downloading the images too
    #     animation_map     = cfg.dir_animation,   # Map for the animations
    #     animation_name    = '',    # The path/name of the animation file
    #     interval_download = 10,    # Interval time for downloading Images (minutes)
    #     duration_download = 60,    # Total time for downloading all the images (minutes)
    #     animation_time    = 0.7,   # Animation interval time for gif animation
    #     remove_download   = False, # Remove the downloaded images
    #     gif_compress      = True,  # Compress the size of the animation
    #     date_submap       = True,  # Set True to create extra date submaps
    #     date_subname      = True,  # Set True to create extra date in files
    #     verbose           = None  # Overwrite verbose -> see config.py
    # )

    ############################################################################
    # Example: multiple downloads at the same time usings threads
    # cfg.timer = False # No multiple clocks at the same time, cannot
    #
    # date = ymd.yyyymmdd_now() # Start date today
    # duration = 1 * 20 # Duration time download (minutes), 14 hours

    daily_interval_knmi_10min(
        url_temperature,  # Fill in download image url
        start_time        = '09:29:40', # Start time to download an image (every day)
        duration          = 10*60,  # Time to download images
        interval          = 10,     # Interval time for downloading Images (minutes)
        start_date        = ymd.yyyymmdd_now(), # <optional> Start date for downloading images format yyyymmdd
        stop_date         = '',     # <optional> Give an end date format: yyyymmdd
        download_map      = cfg.dir_download,  # <optional> Map for downloading the images too
        animation_map     = cfg.dir_animation, # <optional> Map for the animations
        animation_name    = '',    # <optional> The path/name of the animation file
        animation_time    = 0.5,   # <optional> Animation interval time for gif animation
        remove_download   = False, # <optional> Remove the downloaded images
        gif_compress      = True,  # <optional> Compress the size of the animation
        date_submap       = True,  # <optional> Set True to create extra date submaps
        verbose           = True   # <optional> Output to screen
    )

    # # Start 4 threads with different urls and on different times/date
    # # Interval download morning (day) temperature animation
    # threading.Thread( target=daily_interval_knmi_10min,
    #                   args=(url_temperature, '06:09:50', duration, date, )
    #                   ).start()
    #
    # time.sleep(1)
    #
    # # Interval download evening (night) temperature animation
    # threading.Thread( target=daily_interval_knmi_10min,
    #                   args=(url_temperature, '18:09:51', duration, date, )
    #                   ).start()
    #
    # time.sleep(1)
    #
    # # Interval download morning (day) wind animation
    # threading.Thread( target=daily_interval_knmi_10min,
    #                   args=(url_windforce, '06:09:52', duration, date, )
    #                   ).start()
    #
    # time.sleep(1)
    #
    # # Interval download evening (night) wind animation
    # threading.Thread( target=daily_interval_knmi_10min,
    #                   args=(url_windforce, '18:09:53', duration, date, )
    #                   ).start()
