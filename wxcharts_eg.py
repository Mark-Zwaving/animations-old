# -*- coding: utf-8 -*-
''' File contains a functions wrapper for downloading weather model images
    from the wxcharts.com.'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.1.2'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'
# Python version > 3.7 (fstring)

import common.config as cfg # Configuration defaults. See config.py
import common.model.animation as anim  # import animation library
import common.model.util as util
import common.model.validate as validate
import common.model.ymd as ymd
import common.view.console as cnsl
import common.control.fio as fio
import common.control.ask as ask
import threading, time # Multi processing and time

# Init vars wxcharts.com
# http://wxcharts.com/charts/ecmwf/nweurope/charts/overview_20211018_00_090.jpg
# http://wxcharts.com/charts/gfs/euratl/charts/snowdepth_20211116_12_000.jpg?
base_url  = 'http://wxcharts.com/charts' # http will work
image_ext = 'jpg' # Image extension for download images

# Default model options wxcharts.com
# Available models
gfs     = 'gfs'
gefs    = 'gefs'
ukmo    = 'ukmo'
ecmwf   = 'ecmwf'
icon_eu = 'icon_eu'
gdps    = 'gdps'
arpege  = 'ARPEGE'
gem     = 'GEM'

# Weather cards options
overview   = 'overview'
winterview = 'winteroverview'
hPa850     = '850temp'
temp2meter = '2mtemp'
snowdepth  = 'snowdepth'
wind10m    = 'wind10mkph'
sum_precip = 'accprecip'

# Areas (depends on model)
# euratl, europe, nweurope, neeurope, seeurope, uk, eng, sco, france, germany,
# italy, spain, poland, turkey, alps, denmark
nord_west_europe = 'nweurope'
nord_east_europe = 'neeurope'
europe_atlantic  = 'euratl'
europe           = 'europe'
germany          = 'germany'
benelux          = 'low_countries'

# Date today
ymd_now = ymd.yyyymmdd_now()

# WXCHARTS specific fn
# Main wxcharts function wrapper what makes animations from wxcharts.com images
def model(
        name            = 'gfs',       # Options model: gfs, gefs, ukmo, ecmwf, icon_eu, gdps, ARPEGE, GEM
        option          = 'snowdepth', # Options type: overview, winteroverview, 850temp, 2mtemp, snowdepth, wind10mkph, accprecip
        area            = 'euratl',    # Options for area eg. euratl europe france germany low_countries
        yyyymmdd        = ymd_now, # Date of run format: yyyymmdd
        run             = '12',        # Options time: 00, 06, 12, 18
        start_time      = 0,           # Start image
        step_time       = 3,           # Step image
        end_time        = 384,         # End image
        animation_time  = 0.7,         # Animation interval time for gif animation
        download_map    = cfg.dir_download,  # Map for downloading the images too
        animation_map   = cfg.dir_animation, # Map for the animations
        remove_download = False,       # Remove the downloaded images
        gif_compress    = True,        # Compress the size of the animation
        date_submap     = True,        # Set True to create extra date submaps
        date_subname    = True,        # Set True to add a date in the filename
        verbose         = True         # Overwrite verbose -> see config.py
    ):
    '''Function creates and saves a gif animation based on weather model output
       type and time options. Data is from wxcharts.com'''
    ok, path, verbose = False, '', cnsl.verbose(verbose)
    web_name = util.url_name(base_url)
    cnsl.log(f'Start {web_name} animation {ymd.now()}', verbose)
    cnsl.log(f'Model is {name} | Option is {option} | Area is {area} | Date is {yyyymmdd}', verbose)
    cnsl.log(f'Run is {run} with images from {start_time} to {end_time} with a step of {step_time}', verbose)

    if validate.yyyymmdd(yyyymmdd, verbose):
        # Extra map specific for this run and model
        sub_map = f'{web_name}/{name}/{run}'.lower()

        # Make download path
        if date_submap: # Update download map
            y, m, d, hh, mm, ss = ymd.y_m_d_h_m_s_now()
            download_map = util.mk_path(download_map, f'{y}/{m}/{d}')
        download_map = util.mk_path(download_map, sub_map)

        # Make the paths and uries for downloading the model images
        url   = f'{base_url}/{name}/{area}/charts/' # Base url first part
        base  = f'{option}_{yyyymmdd}_{run}' #
        ext   = validate.extension( image_ext ) # Handle dot. Add one if . not exists
        times = range(start_time, end_time+1, step_time) # List times for images
        names = [f'{base}_{ts:0>3}{ext}' for ts in times] # Create list with image names
        paths = [util.mk_path(download_map, f'{web_name}_{name}_{area}_{n}') for n in names] # Create full paths lst
        uries = [util.mk_path(url, n) for n in names] # Create download web url list

        # Download all images from an uries list
        uries, paths = fio.download_lst(uries, paths, True, verbose)

        # Animation map
        if date_submap: # Update animation map with dates
            y, m, d, hh, mm, ss = ymd.y_m_d_h_m_s_now()
            animation_map = util.mk_path(animation_map, f'{y}/{m}/{d}')
        animation_map = util.mk_path(animation_map, sub_map)

        # Animation file
        fname = f'{web_name}_{name}_{area}_{option}_{run}_{start_time:0>3}-{end_time:0>3}'
        if date_submap: # Add date to file name
            y, m, d, hh, mm, ss = ymd.y_m_d_h_m_s_now()
            fname = f'{fname}_{y}-{m}-{d}_{hh}-{mm}-{ss}'

        # Animation path
        path = util.mk_path( animation_map, f'{fname}.gif'.lower() )

        # Create animation file
        ok = anim.create(paths, path, animation_time, verbose)

        # Compress animation
        if ok and gif_compress: util.compress_gif(path, verbose)

        # Remove downloaded images
        if remove_download: fio.rm_lst(paths)

        # Open file with a default app
        # ask.open_with_app(path)
    else:
        cnsl.log(f'Error in date {yyyymmdd}', cfg.error)

    cnsl.log(f'End {web_name} animation', verbose)
    return ok, path


def download_model( weather_types, # List of weathertypes -> overview, tmep2meter
                    areas,         # List of areas
                    name,          # Name of model
                    yyyymmdd,          # Date of model run
                    run,           # Time of model run
                    start_time,    # Start time of run
                    step_time,     # Interval time of run
                    end_time       # End time of run
    ):
    '''Function downloads from optoins lists with weather types and areas all
       the models run'''
    for option in weather_types: # Which type weather images
        for area in areas: # Which areas
            model( name=name, option=option, area=area, run=run, yyyymmdd=yyyymmdd,
                   start_time=start_time, step_time=step_time, end_time=end_time )

def download_model_icon_eu(yyyymmdd, run):
    '''Function downloads model icon with several options'''
    wtypes = [overview, temp2meter, snowdepth] # ,sum_precip, wind10m, hPa850, winterview, snowdepth
    areas  = [europe, benelux]
    download_model( weather_types=wtypes, areas=areas, name=icon_eu, yyyymmdd=yyyymmdd,
                    run=run, start_time=0, step_time=3, end_time=60 )
    download_model( weather_types=wtypes, areas=areas, name=icon_eu, yyyymmdd=yyyymmdd,
                    run=run, start_time=60, step_time=3, end_time=120 )

def download_model_gfs(yyyymmdd, run):
    '''Function downloads model gfs with several options'''
    wtypes = [overview, temp2meter, snowdepth] #, sum_precip, wind10m, hPa850, winterview, snowdepth
    areas  = [europe_atlantic, benelux] # europe
    download_model( weather_types=wtypes, areas=areas, name=gfs, yyyymmdd=yyyymmdd,
                    run=run, start_time=0, step_time=6, end_time=120 )
    download_model( weather_types=wtypes, areas=areas, name=gfs, yyyymmdd=yyyymmdd,
                    run=run, start_time=120, step_time=6, end_time=240 )
    download_model( weather_types=wtypes, areas=areas, name=gfs, yyyymmdd=yyyymmdd,
                    run=run, start_time=240, step_time=6, end_time=360 )

def download_model_ec(yyyymmdd, run):
    '''Function downloads model ecmwf with seceral options'''
    wtypes = [overview, temp2meter, snowdepth] #, sum_precip, wind10m, hPa850 , winterview, snowdepth
    areas  = [europe_atlantic, benelux] # europe,
    download_model( weather_types=wtypes, areas=areas, name=ecmwf, yyyymmdd=yyyymmdd,
                    run=run, start_time=0, step_time=6, end_time=120 )
    download_model( weather_types=wtypes, areas=areas, name=ecmwf, yyyymmdd=yyyymmdd,
                    run=run, start_time=120, step_time=6, end_time=240 )

def download_daily():
    '''Function downloads daily several models at different times'''
    while True: # Eternal loop
        # Download models run 00, 12, 18 at given times
        for run, stime in { '00': '06:00:00',
                            '06': '12:00:00',
                            '12': '18:00:00',
                            '18': '00:00:00'
                            }.items():
            # Make download model times
            gfs_time = ymd.hh_mm_ss_plus_hour(stime, 2) # Add two hours
            ecm_time = ymd.hh_mm_ss_plus_hour(stime, 3) # Add three hours

            # Get dates
            wait_date = model_date = ymd.yyyymmdd_now()
            # For the 18 hour we need to wait for the next day
            if run == '18': wait_date = ymd.yyyymmdd_next_day()

            # ICON, first
            util.pause( stime, wait_date, f'download model run {run} ICON at' )
            download_model_icon_eu(model_date, run)

            # GFS, one hour later
            util.pause( gfs_time, wait_date, f'download model run {run} GFS at' )
            download_model_gfs(model_date, run)

            # ECMWF, only 00 and 12 run and three hours later
            if run in ['00','12']:
                util.pause( ecm_time, wait_date, f'download model run {run} ECMWF at' )
                download_model_ec(model_date, run)


if __name__ == "__main__":
    ''' WXCHARTS EXAMPLES '''
    # EXAMPLE MODEL
    model(
        name            = 'gfs',       # Options model: gfs, gefs, ukmo, ecmwf, icon_eu, gdps, ARPEGE, GEM
        option          = 'snowdepth', # Options type: overview, winteroverview, 850temp, 2mtemp, snowdepth, wind10mkph, accprecip
        area            = 'euratl',    # Options for area eg. euratl europe france germany low_countries
        yyyymmdd        = '20211117',  # Date of run format: yyyymmdd
        run             = '12',        # Options time: 00, 06, 12, 18
        start_time      = 0,           # Start image
        step_time       = 6,           # Step image
        end_time        = 384,         # End image
        animation_time  = 0.7,         # Animation interval time for gif animation
        download_map    = cfg.dir_download,  # Map for downloading the images too
        animation_map   = cfg.dir_animation, # Map for the animations
        remove_download = False,       # Remove the downloaded images
        gif_compress    = True,        # Compress the size of the animation
        date_submap     = True,        # Set True to create extra date submaps
        date_subname    = True,        # Set True to add date in filename
        verbose         = True         # Overwrite verbose -> see config.py
    )

    # model( icon_eu, overview,   europe,  anim.yyyymmdd_now(), '12', 0, 3, 120 )
    # model( icon_eu, temp2meter, benelux, anim.yyyymmdd_now(), '12', 0, 3, 120 )

    ############################################################################
    # Example daily repeating download_
    # Download everyday the same run at the same time
    # download_daily()

    util.app_time()
