# -*- coding: utf-8 -*-
''' File contains examples for how to use the function from the anim library'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.0.8'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'
# Python version > 3.7 (fstring)

################################################################################
# USAGE OF CODE EXAMPLES

################################################################################
# SYNOPSIS function create()
# Description: Makes an animation.
#              It will create the path of the animation image if it doesn't exists.
# Source: common.sources.animation
# def create(
#     lst          = [],       # List with all the images for the animation
#     path         = '',       # <optional> File path for the animation image
#     interval     = interval, # <optional> Interval time for the image
#     verbose      = False     # <optional> Overwrite default value verbose -> see config.py
# )
# Return: ok<boolean>, path<path>
# Code example
import common.config as cfg # import configuration file
import common.view.console as cnsl
import common.sources.animation as anim # import library with animation functions
import common.sources.util as util # import library with animation functions
import common.sources.fio as fio # import library with animation functions

# Use function mk_path() from config to create a real path
path = util.mk_path(cfg.dir_animation, 'test_animation.gif' )

# Create a list with the (test) images for the animation
lst_img = [
    util.mk_path(cfg.dir_images, 'test/bird-0.JPG'),
    util.mk_path(cfg.dir_images, 'test/bird-1.JPG'),
    util.mk_path(cfg.dir_images, 'test/bird-2.JPG')
]

# Interval time in seconds
interval_time = 1.0

# Make/create the animation
ok, path = anim.create( list_img, path, interval_time )

# Open file with a default app
if ok: ask.open_with_app(path)
################################################################################

################################################################################
# SYNOPSIS function download()
# Description: Dowloads a file/image if not already exists.
#               It will create the path/directories if it doesn't exist.
# Source: common.control.fio
# download(
#     url,  # Url to download
#     path, # Path to download the file to
#     check   = True,  # <optional> Check file True will not overwrite the file if exists
#     verbose = False  # <optional> Overwrite default value verbose -> see config.py
# )
# Return: <boolean> ok (True or False)
# Code example
import common.config as cfg # import configuration file
import common.sources.animation as anim # import library with animation functions

# Get the directory of this map from config
map = cfg.dir_app

# The file to download
url = 'http://www.spronck.net/pythonbook/pythonbook.pdf'

# Function (from config) to create a real path
path = util.mk_path(map, 'pdf/books/pythonbook.pdf')

# Init parameter for download fn
check, verbose = True, True

# Download the file to path
fio.download(url, path, check, verbose)
################################################################################

################################################################################
# SYNOPSIS function pause()
# Description: Execution of programm will be paused untill a certain date/time
# pause(
#     hh_mm_ss,      # Time with format <HH:MM:SS> to pause untill to.
#     yyyymmdd = '', # <optional> Date to start. Format <yyyymmdd> If omitted current date will be used.
#     output   = 'programm will continue at', # <optional> Output text second substring
#     verbose = False # <optional> overwrite default value verbose -> see config.py
# )
# Source: common.model.util
# Code example
import common.model.util as util  # import library with animation functions

yy = '2023' # Start year
mm = '01'   # Start month
dd = '01'   # Start day
HH = '00'   # Start hour
MM = '00'   # Start minute
SS = '00'   # Start seconds

untill_date = f'{yy}{mm}{dd}'
untill_time = f'{HH}:{MM}:{SS}'

# Progamm paused untill 2023 01 01 00:00:00
util.pause( untill_time, untill_date )
cnsl.log('Happy New Year !', True)
################################################################################

################################################################################
# SYNOPSIS function download_interval()
# Description: Execution of programm will be paused untill a certain date/time
# download_interval(
#     url,          # Url for the files on the web
#     map           = cfg.dir_download, # Map for the downloads
#     interval      = 10,    # Interval time for downloading Images (minutes)
#     duration      = 1*60,  # Total time for downloading all the images (minutes)
#     date_submap   = False, # Set True to the possible given date submaps
#     date_subname  = False, # Add date and time to downloaded files
#     check         = True,  # No double downloads check
#     verbose       = False  # With output to screen
# )
# Source: common.model.fio
# Return: path<list>
# Make an animation of current temperature card of weerplaza.nl
import common.config as cfg # import configuration file
import common.control.fio as fio  # import library with fio (file io) functions
import common.model.animation as anim  # import library with animation functions

# Init DOWNLOAD
# Download url of current temp image weerplaza.
download_url = 'https://oud.weerplaza.nl/gdata/10min/GMT_TTTT_latest.png'
# Map for downloading the images to, cfg.root_dir is current map.
download_map = util.mk_path(cfg.dir_download, 'weerplaza')
# Time in between downloads (minutes)
download_interval_time = 10 # Download every 10 minutes!
# Total time for downloading the images (minutes)
download_duration_time = 60 # Download images for 60 minutes!

# Init image ANIMATION
# File name and path of the animation image to create
animation_path = util.mk_path(cfg.dir_animation, 'weerplaza/weerplaza_anim.gif')
# Time to show the images (seconds)
animation_interval = 0.7  # = 0.7 seconds
# Compress animation image. True or False
# To use this: programm gifsicle needs to be installed on your system
animation_compress = False

# Init start DATE TIME
# Make a start date and time to start download  <optional>
start_time = '12:00:00' # Start time format <hh:mm:ss>
start_date = '202205021' # Start date format <yyyymmdd>

# Start executing functions
# Wait untill start date and time <optional>
util.pause(start_time, start_date)

# Start interval download of images.
# Function returns the paths of the downloaded images
image_paths = fio.download_interval( download_url,
                                     download_map,
                                     download_interval_time,
                                     download_duration_time )

# Function creates an image animation
anim.create( image_paths, animation_path, animation_interval, animation_compress )
################################################################################

################################################################################
# SHORT CODE EXAMPE INTERVAL DOWNLOAD IMAGE
# Make an animation of current temperature card of weerplaza.nl
import common.config as cfg # import configuration file
import common.model.animation as anim  # import library with animation functions
import common.model.util as util  # import library util
import common.control.fio as fio  # import file io fn
# Wait untill start date and time
util.pause('19:18:00', '20211116')
# Download map for the images
download_map = util.mk_path(cfg.dir_download, 'weerplaza')
# Start interval download of images. Function returns the list of downloaded files/images
paths = fio.download_interval( 'https://oud.weerplaza.nl/gdata/10min/GMT_TTTT_latest.png',
                                download_map, # Download map
                                10,           # Time in between downloads (minutes)
                                14*60 )       # Download images for 12*60 (minutes)
# Make animation image name
path = util.mk_path(cfg.dir_animation, 'weerplaza/weerplaza_anim.gif')
# Create an animation. Function returns the name of the animation
ok, path = anim.create( path, # Animation file
                        paths,          # List with images for the animation file
                        0.7 )           # Interval time to show the images (seconds)
# Compress image works only if - gifsicle - is installed
if ok: util.gif_compress(path)
# Remove downloaded images (save diskspace)
fio.rm_files(path)
################################################################################
## TODO
## See the files util.py, fio.py, animation.py for more functions
