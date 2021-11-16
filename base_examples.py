# -*- coding: utf-8 -*-
''' File contains examples for how to use the function from the anim library'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.7'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

# Python version > 3.7 (fstring)

################################################################################
# SEE BELOW USAGE OF REAL WORLD CODE EXAMPLES
# EG. Copy/paste the examples of the code.
# See config.py for the base configuration options
# See knmi.py for knmi code examples
# See wetterzentrale.py for wetterzentrale code examples
# See wxcharts.py for wxcharts code examples

################################################################################
# SYNOPSIS function create()
# Description: Makes an animation.
#              It will create the path of the animation image if it doesn't
#              exists.
# create(
#         fname,     # File name for the animation image
#         lpaths,    # List with all the images for the animation
#         duration   # <optional> Interval time for the image.
#                    # If not there it will use the default value.
#                    # See config.py -> animation_time
# )
#
# Code example
import config as cfg # import configuration file
import sources.anim as anim # import library with animation functions

# Ceate path to animation file.
# Get the directory of this map from config -> cfg.root_dir
mainmap = cfg.app_dir

# Use function mk_path() from config to create a real path
path_animation = anim.mk_path(mainmap, 'test/animation.gif' )

# Create a list with images for the animation
list_images = [
    anim.mk_path(mainmap, 'test/bird-0.JPG'),
    anim.mk_path(mainmap, 'test/bird-1.JPG'),
    anim.mk_path(mainmap, 'test/bird-2.JPG')
]

# Interval time in seconds
interval_time = 0.8

# Make/create the animation
anim.create( path_animation, list_images, interval_time )
################################################################################

################################################################################
# SYNOPSIS function download()
# Description: Dowloads a file/image if not already exists.
#               It will create the path/directories if it doesn't exist.
# download(
#    url,        # The download internet url.
#    path,       # Path/name of the downloaded file.
#    check_file  # <optional> Checks if a file already exists. Default is True
# )
#
# Code example
import config as cfg # import configuration file
import sources.anim as anim # import library with animation functions

# Get the directory of this map from config
mainmap = cfg.app_dir

# The file to download
url = 'http://www.spronck.net/pythonbook/pythonbook.pdf'

# Function (from config) to create a real path
path = anim.mk_path(mainmap, 'books/pythonbook.pdf')

# Download the file to path
anim.download(url, path, True)
################################################################################

################################################################################
# SYNOPSIS function pause()
# Description: Execution of programm will be paused untill a certain date/time
# pause(
#         untill_time,  # Time to pause untill. If omitted 00:00:00 wiil be used
#         untill_date   # Date to start. Format <yyyymmdd>
#                       # If omitted current date will be used.
# )
#
# Code example
import sources.anim as anim  # import library with animation functions

yyyy = '2023' # Start year
mm   = '01'   # Start month
dd   = '01'   # Start day
HH   = '00'   # Start hour
MM   = '00'   # Start minute
SS   = '00'   # Start seconds

untill_date = f'{yyyy}{mm}{dd}'
untill_time = f'{HH}:{MM}:{SS}'

anim.pause( untill_time, untill_date ) # Progamm paused untill 2023 01 01 00:00:00
print('Happy New Year !')
################################################################################

################################################################################
# CODE EXAMPE INTERVAL DOWNLOAD IMAGE
# Make an animation of current temperature card of weerplaza.nl
import config as cfg # import configuration file
import sources.anim as anim  # import library with animation functions

# Init start DATE TIME
# Make a start date and time to start download  <optional>
start_time = '12:00:00' # Start time format <hh:mm:ss>
start_date = '20211021' # Start date format <yyyymmdd>

# Init DOWNLOAD
# Download url of current temp image weerplaza.
download_url = 'https://oud.weerplaza.nl/gdata/10min/GMT_TTTT_latest.png'
# Map for downloading the images to, cfg.root_dir is current map.
download_map = anim.mk_path(cfg.app_dir, 'downloads/weerplaza')
# Time in between downloads (minutes)
download_interval_time = 10 # Download every 10 minutes!
# Total time for downloading the images (minutes)
download_duration_time = 60 # Download images for 60 minutes!

# Init image ANIMATION
# File name and path of the animation image to create
animation_path = anim.mk_path(cfg.app_dir, 'animations/weerplaza/weerplaza_anim.gif')
# Time to show the images (seconds)
animation_interval = 0.7  # = 0.7 seconds
# Compress animation image. True or False
# To use this: programm gifsicle needs to be installed on your system
animation_compress = False

# Start executing functions
# Wait untill start date and time <optional>
anim.pause(start_time, start_date)

# Start interval download of images.
# Function returns the paths of the downloaded images
image_paths = anim.download_interval( download_url,
                                      download_map,
                                      download_interval_time,
                                      download_duration_time )

# Function creates an image animation
anim.create( animation_path, image_paths, animation_interval, animation_compress )
################################################################################

################################################################################
# SHORT CODE EXAMPE INTERVAL DOWNLOAD IMAGE
# Make an animation of current temperature card of weerplaza.nl
import config as cfg # import configuration file
import sources.anim as anim  # import library with animation functions

anim.pause('12:30:00', '20211021') # Wait untill start date and time
download_map = anim.mk_path(cfg.app_dir, 'downloads/weerplaza') # Download map for the images

# Start interval download of images. Function returns the list of downloaded files/images
paths = anim.download_interval( 'https://oud.weerplaza.nl/gdata/10min/GMT_TTTT_latest.png',
                                download_map, # Download map
                                10,           # Time in between downloads (minutes)
                                12*60 )       # Download images for 12*60 (minutes)
# Make animation image name
path = anim.mk_path(cfg.app_dir, 'animations/weerplaza/weerplaza_anim.gif')
# Create an animation. Function returns the name of the animation
ok = anim.create( animation_file, # Animation file
                    paths,          # List with images for the animation file
                    0.7  )          # Interval time to show the images (seconds)
# Compress image works only if - gifsicle - is installed
if ok: anim.gif_compress(path)
# Remove downloaded images (save diskspace)
anim.remove_files_in_list(path)
################################################################################
