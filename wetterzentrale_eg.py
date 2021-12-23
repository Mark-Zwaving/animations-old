# -*- coding: utf-8 -*-
''' File contains a functions wrapper for downloading weather model images
    from the wetterzentrale.de.'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.1.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'
# Python version > 3.7 (fstring)

import common.config as cfg # Configuration defaults. See config.py
import common.model.animation as anim  # import animation library
import common.model.util as util
import common.model.validate as validate
import common.model.ymd as ymd
import common.view.console as cnsl
import common.view.txt as txt
import common.control.fio as fio
import common.control.ask as ask
import os, threading, time # Multi processing and time

# Base url model images
base_url  = 'https://www.wetterzentrale.de/maps'

# Available models and their names at wetterzentrale
gfs, ecmwf, wrf, icon = 'GFS', 'ECM', 'WRF', 'ICO'
harmonie, har_nl, arpege, gem = 'HAR40', 'HAR', 'ARPEGE', 'GEM'

# Model options. Not all models support all the options. TODO
model_options = {
    '1': 'hpa500',
    '2': 'temp850',
    '4': 'precipiation',
    '5': 'temp2meter',
    '9': 'wind10meter',
   '10': 'dewpoint',
   '25': 'snow_cover',  # GFS
   '18': 'precipiation_sum',
   '38': 'temp2meter_HD',
   '43': 'precipiation_HD',
   '49': 'precipiation_sum_HD',
   '50': 'snow_HD',
   '51': 'snowsum_HD'
}

# Download image extension
image_ext   = '.png'

# Process options for url
def options(option):
    '''Function select specific id for for download image url. See weather options'''
    # init vars
    o = str(option).lower()

    # Walkthrough dictionary
    for k, v in model_options.items():
        k, v = k.lower(), v.lower()
        if o in [k,v]:
            return k, v

    # Not programmed yet. Return number only. Map names will be numbers
    if o.isdigit():
        return o, o
    else:
        return '1', 'hpa500' # Error

# Main wetterzentrale.de function what makes animations from wetterzentrale images
def model(
        name             = 'gfs',    # Options for which model: GFS,ECM,WRF,ICO, HAR40,ARPEGE, GEM
        option           = 'hpa500', # Options for type, weather name or num. See model_options
        member           = 'OP', # Options for member: OP, AVG, PARA, SPR
        area             = 'EU',   # Options for area: EU, ME, NL, BE, SC
        run              = '00',    # Options for run: 00, 06, 12, 18
        start_time       = 0,      # Start image
        step_time        = 12,     # Interval step for images
        end_time         = 240,    # End image
        download_map     = cfg.dir_download,    # Map for downloading the images too
        animation_map    = cfg.dir_animation,   # Map for the animations
        animation_time   = 0.7,    # Animation interval time for gif animation
        remove_download  = False, # Remove the downloaded images
        gif_compress     = True,  # Compress the size of the animation
        date_submap      = True,  # Set True to create extra date submaps
        date_subname     = True,  # Set True to create extra date in files
        check            = True,  # No double downloads check
        with_animation   = True,  # Make an animation
        verbose          = None   # Overwerite default verbose -> see config.py
    ):
    '''Function creates and saves a gif animation based on weather model output
       type and time options. Data is from wetterzentrale.de'''

    ok, st = False, time.time()
    web_name = util.url_name(base_url)
    cnsl.log(f'Start {web_name} animation {ymd.now()}', verbose)

    # Get image nam and num (for url)
    num, typ = options( option )
    if num: # Check if num exists
        cnsl.log(f'Model name is {name}', verbose)
        cnsl.log(f'Area {area} | Option {option} | Member {member} | Run {run}', verbose)
        cnsl.log(f'Time from {start_time} to {end_time} step is {step_time}\n', verbose)

        # Extra map specific for this run and model
        sub_map = f'{web_name}/{name}/{run}'.lower()
        # Make download path
        if date_submap: # Update download map
            y, m, d, hh, mm, ss = ymd.y_m_d_h_m_s_now()
            download_map = util.mk_path(download_map, f'{y}/{m}/{d}')
        download_map = util.mk_path(download_map, sub_map)

        # Create local images paths and correct web uries list based on selected model
        # and selected frames times. Url eg: https://www.wetterzentrale.de/maps/GFSOPEU18_0_1.png
        urie   = f'{name}{member}{area}{run}'.upper() # String for model options. ie GFSOPEU12
        fname  = f'{web_name}_{name}_{area}_{option}_{member}_{run}' # Base file name
        ext    = validate.extension( image_ext ) # Handle dot. Add one if . not exists
        times  = range(start_time, end_time+1, step_time) # List times for images
        unames = [f'{urie}_{tms}_{num}{ext}' for tms in times] # Create list with image names for uries
        fnames = [f'{fname}_{tms}{ext}' for tms in times] # Create the list with the files names
        paths  = [util.mk_path(download_map, n.lower()) for n in fnames] # Create full paths lst
        uries  = [util.mk_path(base_url, n) for n in unames] # Create download web url list

        # Download all images
        uries, paths = fio.download_lst(uries, paths, check, verbose)

        if with_animation:
            # Animation map
            if date_submap: # Update animation map with dates
                y, m, d, hh, mm, ss = ymd.y_m_d_h_m_s_now()
                animation_map = util.mk_path(animation_map, f'{y}/{m}/{d}')
            animation_map = util.mk_path(animation_map, sub_map)

            # Animation file
            fname = f'{web_name}_{name}_{area}_{option}_{member}_{run}_{start_time:0>3}-{end_time:0>3}'
            if date_submap: # Add date to file name
                y, m, d, hh, mm, ss = ymd.y_m_d_h_m_s_now()
                fname = f'{fname}_{y}-{m}-{d}_{hh}-{mm}-{ss}'

            # Animation path
            path = util.mk_path(animation_map, f'{fname}.gif'.lower())

            # Create animation file
            ok, path = anim.create( paths, path, animation_time, verbose)

            # Compress animation
            if ok and gif_compress: util.compress_gif(path, verbose)

            # Remove downloaded images
            if remove_download: fio.rm_lst(paths, verbose)

            # Open file with a default app
            # ask.open_with_app(path)
    else:
        cnsl.log('Error: weather type name not found', verbose)
        cnsl.log('Check model_options for an (correct) name', verbose)

    util.time_passed(st, f'Model {name} {member} {area} {option} downloaded and animation made in', verbose)
    cnsl.log(f'End {web_name} animation', verbose)
    return ok, path

def download_models_daily( ):
    '''Function downloads daily several models at different times'''
    d = ymd.yyyymmdd_now() # Start today
    iv, rm, cp, ds, dn, ck, wa, vb = 0.7, False, True, True, True, True, True, True
    dm, am = cfg.dir_download, cfg.dir_animation # Base maps (shortened)
    # Eternal loop
    while True:
        # Download GFS  models run 00, 12, 18 at given times
        for run, stime in { #'00': '06:00:00', '06': '12:00:00',
                            '12': '18:00:00', '18': '00:00:00'
                            }.items():
            har40_time = ico_time = gfs_time = stime # Start time models harmony and icon, gfs
            ecm_time = ymd.hh_mm_ss_plus_hour(stime, 2) # Two hours later

            # Get correct date. For the 18 hour run we need the next day to wait for
            d = ymd.yyyymmdd_plus_day() if run == '18' else ymd.yyyymmdd_now()

            # HARMONIE NL
            util.pause( har40_time, d, f'download models HARMONIE & ICON for run {run} at' )
            # model( harmonie, 'temp850',             'OP', 'ME', run, 0, 1, 48, 0.7, dm, am, False, True, True, True, True, True )
            model( harmonie, 'temp2meter_HD', 'OP', 'NL', run, 0, 1, 48, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
            # model( harmonie, 'precipiation_sum_HD', 'OP', 'NL', run, 0, 1, 48, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
            model( harmonie, 'snowsum_HD', 'OP', 'NL', run, 0, 1, 48, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )

            # ICON
            model( icon, 'hpa500',     'OP', 'EU', run, 0, 1, 120, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
            model( icon, 'temp2meter', 'OP', 'ME', run, 0, 1, 120, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
            model( icon, 'snow_cover', 'OP', 'ME', run, 0, 1, 120, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )

            # GFS
            util.pause( gfs_time, d, f'download model GFS for run {run} at' ) # Update time for GFS, One hour later
            model( gfs, 'hpa500', 'OP', 'EU', run,   0, 1,  92, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
            model( gfs, 'hpa500', 'OP', 'EU', run,  92, 1, 288, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
            model( gfs, 'hpa500', 'OP', 'EU', run, 288, 3, 384, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
            model( gfs, 'temp2meter', 'OP', 'ME', run,   0, 1, 120, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
            model( gfs, 'temp2meter', 'OP', 'ME', run, 120, 3, 384, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
            model( gfs, 'snow_cover', 'OP', 'ME', run,   0, 1, 240, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
            model( gfs, 'snow_cover', 'OP', 'ME', run, 240, 3, 384, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )

            # ECMWF
            if run in ['00', '12']: # Only 00 and 12 run @ 02 & 20
                util.pause( ecm_time, d, f'download model ECMWF run {run} ECMWF at' )
                for member in ['OP', 'AVG', 'PARA']: # Download two members
                    model( ecmwf, 'hpa500', member, 'EU', run, 0, 24, 240, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )

def daily_processes():
    '''Function start two daily processess/threads.'''
    # Start multiple threads
    threading.Thread( target=download_models_daily ).start()
    # Remove downloads after 3 days (testing). Start thread
    # Thread( target=anim.remove_downloads_after_day, argv=(3,)).start()

# nohup command >/dev/null 2>&1
if __name__ == "__main__":
    # # Update download and animation dir for webserver
    # dir_www = os.path.abspath('/var/www/html/weather/images')
    # cfg.dir_download  = util.mk_path(dir_www, 'download')
    # cfg.dir_animation = util.mk_path(dir_www, 'animation')

    ############################################################################
    # Examples model animations
    #daily_processes()

    ############################################################################
    # Function model
    # Description: downloads images and makes an animation
    # model(
    #     name             = gfs,    # Options for which model: GFS,ECM,WRF,ICO, HAR40,ARPEGE, GEM
    #     option           = 'hpa500', # Options for type, weather name or num. See model_options
    #     member           = 'OP', # Options for member: OP, AVG, PARA, SPR
    #     area             = 'EU',   # Options for area: EU, NL, ME
    #     run              = '12',    # Options for run: 00, 06, 12, 18
    #     start_time       = 0,      # Start image
    #     step_time        = 1,     # Interval step for images
    #     end_time         = 384,    # End image
    #     download_map     = cfg.dir_download,    # Map for downloading the images too
    #     animation_map    = cfg.dir_animation,   # Map for the animations
    #     animation_time   = 0.7,    # Animation interval time for gif animation
    #     remove_download  = False, # Remove the downloaded images
    #     gif_compress     = True,  # Compress the size of the animation
    #     date_submap      = True,  # Set True to create extra date submaps
    #     date_subname     = True,  # Set True to create extra date in files
    #     check            = True,  # No double downloads check
    #     with_animation   = True,  # Make an animation
    #     verbose          = True   # With output to screen
    # )

    ############################################################################
    # Examples models
    run, dm, am = '00', cfg.dir_download, cfg.dir_animation # Base maps (shortened)
    # Options: gif_interval, remove_download, gif_compress, date_map, date_name,
    # download_check, with_animation, verbose
    iv, rm, cp, ds, dn, ck, wa, vb = 0.5, False, True, True, True, True, True, True
    st, dt, et = 40, 1, 102 # Start time, diff time, end time
    # model( gfs,      'snow_cover',        'OP', 'ME', run, 120,  1, 288, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( gfs,      'hpa500',            'OP', 'EU', run, 96,  1, 288, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )

    model(gfs, 'temp2meter', 'OP', 'NL', run, st, dt, et, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    model(gfs, 'snow_cover', 'OP', 'NL', run, st, dt, et, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    model(gfs, 'precipiation', 'OP', 'NL', run, st, dt, et, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )


    # model(har_nl, 'dewpoint',   'OP', 'NL', run, 30,  1, 48, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model(har_nl, 'snow_cover', 'OP', 'NL', run, 30,  1, 48, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )

    # model( gfs,      'hpa500',            'OP', 'EU', run,  92,  1, 288, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( gfs,      'hpa500',            'OP', 'EU', run, 288,  3, 384, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( gfs,      'hpa500',            'OP', 'EU', run,   0,  1,  96, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( gfs,      'hpa500',            'OP', 'EU', run,  96,  1, 192, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( gfs,      'hpa500',            'OP', 'EU', run, 192,  3, 384, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( gfs,      'temp2meter',        'OP', 'ME', run,   0,  1, 144, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( gfs,      'temp2meter',        'OP', 'ME', run, 144,  1, 384, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( gfs,      'snow_cover',        'OP', 'ME', run,   0,  1, 384, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( gfs,      'snow_cover',        'OP', 'ME', run, 192,  1, 384, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( harmonie, 'temp850',           'OP', 'ME', '18',  0,  1,  48, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( harmonie, 'temp2meter_HD',     'OP', 'NL', '18',  0,  1,  48, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( gfs,      'precipiation_sum',  'OP', 'ME', '18',  0,  3, 288, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( icon,     'temp2meter',        'OP', 'ME', '18',  0,  3, 180, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( ecmwf,    'hpa500',           'AVG', 'EU', '12',  0, 24, 240, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )
    # model( icon,     'temp2meter',        'OP', 'SC', '12',  0,  1, 180, dm, am, iv, rm, cp, ds, dn, ck, wa, vb )

    util.app_time()
