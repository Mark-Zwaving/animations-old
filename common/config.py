# -*- coding: utf-8 -*-
'''Variables for the base configuration of the bfn module'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.1.0'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import os, sys, time

verbose = True   # Print more (say everything) to screen
log     = False   # Write output to screen to log file. Will make a new log file everyday
debug   = False  # Programm wait after every output to screen
error   = True   # Show errors/exceptions on screen
timer   = True  # Refresh every second for timers

# Name log file. Default logs a new file for every day
log_name = '' # If empty '', default name for log file is used -> log_common_yyyymmdd.log

# Config base maps
dir_app       = os.path.dirname(os.path.abspath(__file__))
dir_view      = os.path.join(dir_app, 'view')
dir_model     = os.path.join(dir_app, 'model')
dir_control   = os.path.join(dir_app, 'control')
dir_images    = os.path.join(dir_app, 'images')
dir_www       = os.path.abspath('/var/www/html/weather/images') # Webserver
dir_up        = os.path.dirname(dir_app)
dir_log       = os.path.join(dir_up, 'logs')
dir_download  = os.path.join(dir_www, 'download')
dir_animation = os.path.join(dir_www, 'animation')
# dir_download  = os.path.join(dir_app, 'download')
# dir_animation = os.path.join(dir_app, 'animation')

# De(fault line width from console
txt_line_width = 80

# No download flooding from a server.
# Time to wait after downloading a file. Always min = 0.2 seconds
download_interval_time = 0.3 # Seconds.
download_max_num = 10000 # Max number downloads, flood protection

# THe webpage for checking if there is a internet connection
check_internet_url = 'https://www.google.com/'

################################################################################
# Vars below do not change
hour_day     =  24
day_week     =   7
sec_minute   =  60
sec_hour     =  sec_minute * sec_minute
sec_day      =  hour_day * sec_hour
sec_week     =  day_week * sec_day
hour_minute  =  sec_minute
day_minute   =  hour_day * hour_minute

# Startup time for running this app (!more or less)
app_start_time = time.time()

# Add common library to system path.
if dir_app not in sys.path:
    sys.path.append(dir_app)
