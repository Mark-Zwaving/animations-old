# -*- coding: utf-8 -*-
''' File contains examples for how to use the function from the anim library
    for downloading images from knmi.nl'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'
# Python version > 3.7 (fstring)

import config as cfg # Configuration defaults. See config.py
import sources.anim as anim  # import animation library
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
        url,                       # Download image url
        start_time = '09:00:00',   # Start time to download an image (every day)
        duration   = 8*60,         # Time to download images
        start_date = '',           # <Optional> Start date for downloading images format yyyymmdd
        stop_date  = ''            # <Optional> Give an end date format: yyyymmdd
    ):
    '''Function handles repetative daily downloads and makes the animations'''
    # Get the current start date if not given
    if not start_date: start_date = anim.yyyymmdd_now()

    # Start loop
    name, _ = anim.basename_extension(url)
    while True:
        # Wait untill start time and start date
        anim.pause(start_time, start_date, f'start download {name} at')

        # Start interval download for url
        anim.interval_download_animation(
            download_url      = url,      # Give a download image url
            name_submap       = 'knmi',   # Name of subdirectory in the maps download and animation
            interval_download = 10,       # Interval time for downloading Images (minutes)
            duration_download = duration, # Total time for downloading all the images (minutes)
            animation_time    = cfg.animation_time,  # Animation interval time for gif animation
            download_map      = cfg.download_dir,    # Map for downloading the images too
            animation_map     = cfg.animation_dir,   # Map for the animations
            remove_download   = False,    # Remove the downloaded images
            gif_compress      = True,     # Compress the size of the animation
            date_submap       = True,     # Set True to create extra date submaps
            date_subname      = True      # Set True to create extra date in files
        )

        # Make a new correct new date
        y, m, d, hh, _, _ = anim.ymd_hms_now() # Get current date and time
        act_date = f'{y}{m}{d}' # Current date
        if int(act_date) > int(start_date): # Next day is there
            hours = int(start_time.split(':')[0])
            if hours > int(hh): # Passed the start_time
                start_date = anim.yyyymmdd_next_day() # Get the next day
            else:
                start_date = anim.yyyymmss_now() # Get the current day
        else: # We are still on the same day 
           start_date = anim.yyyymmdd_next_day() # Get the next day

        # Check end date if there
        if stop_date: # Check to stop
            if int(start_date) > int(stop_date): # Last day is passed
                break # Break loop


if __name__ == "__main__":
    ############################################################################
    # Example: 10 minutes refresh images base example

    # Temp 2 meter
    # anim.interval_download_animation(
    #     download_url      = url_temperature, # Give a download image url
    #     name_submap       = 'knmi', # Give a name of a subdirectory for the maps download and animation
    #     interval_download = 10,     # Interval time for downloading Images (minutes)
    #     duration_download = 13*60,  # Total time for downloading all the images (minutes)
    #     animation_time    = 0.5,    # Animation interval time for gif animation
    #     download_map      = cfg.download_dir,  # Map for downloading the images too
    #     animation_map     = cfg.animation_dir, # Map for the animations
    #     remove_download   = False,  # Remove the downloaded images
    #     gif_compress      = True,   # Compress the size of the animation
    #     date_submap       = True,   # Set True to create extra date submaps
    #     date_subname      = True    # Set True to create extra date in files
    # )

    ############################################################################
    # Example: multiple downloads at the same time usings threads
    cfg.timer = False # No multiple clocks at the same time, cannot

    date = anim.yyyymmdd_now() # Start date today
    duration = 14 * 60 # Duration time download (minutes), 14 hours

    # Start 4 threads with different urls and on different times/date
    # Interval download morning (day) temperature animation
    threading.Thread( target=daily_interval_knmi_10min,
                      args=(url_temperature, '06:09:50', duration, date, )
                      ).start()

    time.sleep(1)

    # Interval download evening (night) temperature animation
    threading.Thread( target=daily_interval_knmi_10min,
                      args=(url_temperature, '18:09:51', duration, date, )
                      ).start()

    time.sleep(1)

    # Interval download morning (day) wind animation
    threading.Thread( target=daily_interval_knmi_10min,
                      args=(url_windforce, '06:09:52', duration, date, )
                      ).start()

    time.sleep(1)

    # Interval download evening (night) wind animation
    threading.Thread( target=daily_interval_knmi_10min,
                      args=(url_windforce, '18:09:53', duration, date, )
                      ).start()
