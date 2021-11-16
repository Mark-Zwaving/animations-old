# -*- coding: utf-8 -*-
''' File contains a functions wrapper for downloading weather model images
    from the wxcharts.com.'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.1.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'
# Python version > 3.7 (fstring)

import config as cfg # Configuration defaults. See config.py
import sources.anim as anim  # import animation library
import threading, time # Multi processing and time

## Init vars wxcharts.com
# Name wxcharts.com
name_wx = 'wxcharts'
# https://wxcharts.com/charts/ecmwf/nweurope/charts/overview_20211018_00_090.jpg?
base_url  = 'http://wxcharts.com/charts/' # http will work, is oke
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

# Which weather model # Options for name: GFS, ECM2
name    = gfs

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

# Options for area
area          = europe_atlantic
option        = overview
run           = '00' # EXE TIMES times for execution runs of models
start_time    = 0    # START     time of first calculation (image)
step_time = 6    # INTERVAL  times in between (images)
end_time      = 240  # END  end  Stime of last calculation (immage)

## WXCHARTS specific fn
# Main wxcharts function wrapper what makes animations from wxcharts.com images
def model(
        name            = name,    # Which weather model
        option          = option,  # Option output temp, overview
        area            = area,    # Options for area eg. euratl europe france germany low_countries
        date            = '',      # Date of run format yyyymmdd
        run             = run,     # Options for time eg. 00, 06, 12, 18
        start_time      = start_time,  # Start image
        step_time       = step_time,   # Step images
        end_time        = end_time,    # End image
        animation_time  = cfg.animation_time,  # Animation interval time for gif animation
        download_map    = cfg.download_dir,    # Map for downloading the images too
        animation_map   = cfg.animation_dir,   # Map for the animations
        remove_download = cfg.remove_download, # Remove the downloaded images
        gif_compress    = cfg.gif_compress,    # Compress the size of the animation
        date_submap     = cfg.date_submap,     # Set True to create extra date submaps
        date_subname    = cfg.date_subname,    # Set True to create extra date in files
    ):
    '''Function creates and saves a gif animation based on weather model output
       type and time options. Data is from wxcharts.com'''
    anim.log('Start make wxcharts animation', True)
    anim.log(f'Model is {name} | Option is {option} | Area is {area}', True)
    anim.log(f'Run is {run} with images from {start_time} to {end_time} with a step of {step_time}', True)

    # Make a download map
    download_map = anim.handle_map(name_wx, name, download_map, date_submap)

    # Make the paths and uries for downloading the model images
    url   = f'{base_url}{name}/{area}/charts/' # Base url first part
    base  = f'{option}_{anim.validate_yyyymmdd(date)}_{run}' #
    ext   = anim.validate_extension( image_ext ) # Handle dot. Add one if . not exists
    times = range(start_time, end_time+1, step_time) # List times for images
    names = [f'{base}_{anim.leading_zero(tms,3)}{ext}' for tms in times] # Create list with image names
    paths = [anim.mk_path(download_map, f'{name}_{area}_{n}') for n in names] # Create full paths lst
    uries = [anim.mk_path(url, n) for n in names] # Create download web url list

    # Download all images from an uries list
    uries, paths = anim.download_list(uries, paths)

    # Make path animation file
    fname = f'{name}_{area}_{base}_{start_time}-{end_time}' # Base animation file name    # Make a download map
    animation_map = anim.handle_map(name_wx, name, animation_map, date_submap)
    fpath = anim.mk_file_path(animation_map, fname, cfg.animation_ext, date_subname) # Make filename

    # Create animation file
    ok = anim.create(fpath, paths, animation_time)

    # Compress animation
    if ok and gif_compress:
        anim.compress_gif(fpath)

    # Remove downloaded images
    if remove_download:
        anim.remove_files_in_list(paths)

    anim.log('End wxcharts animation\n', True)


def download_model( weather_types, # List of weathertypes -> overview, tmep2meter
                    areas,         # List of areas
                    name,          # Name of model
                    date,          # Date of model run
                    run,           # Time of model run
                    start_time,    # Start time of run
                    step_time,     # Interval time of run
                    end_time       # End time of run
    ):
    '''Function downloads from optoins lists with weather types and areas all
       the models run'''
    for option in weather_types: # Which type weather images
        for area in areas: # Which areas
            model( name=name, option=option, area=area, run=run, date=date,
                   start_time=start_time, step_time=step_time, end_time=end_time )


def download_model_icon_eu(date, run):
    '''Function downloads model icon with several options'''
    wtypes = [overview, temp2meter] # ,sum_precip, wind10m, hPa850, winterview, snowdepth
    areas  = [europe, benelux]
    end_time = 120 if run in ['06','18'] else 180
    download_model( weather_types=wtypes, areas=areas, name=icon_eu, date=date,
                    run=run, start_time=0, step_time=3, end_time=end_time )

    # Make extra animations
    download_model( weather_types=wtypes, areas=areas, name=icon_eu, date=date,
                    run=run, start_time=0, step_time=3, end_time=60 )
    download_model( weather_types=wtypes, areas=areas, name=icon_eu, date=date,
                    run=run, start_time=60, step_time=3, end_time=120 )
    if run in ['00','12']:
        download_model( weather_types=wtypes, areas=areas, name=icon_eu, date=date,
                        run=run, start_time=120, step_time=3, end_time=180 )


def download_model_gfs(date, run):
    '''Function downloads model gfs with several options'''
    wtypes = [overview, temp2meter] #, sum_precip, wind10m, hPa850, winterview, snowdepth
    areas  = [europe_atlantic, benelux] # europe

    download_model( weather_types=wtypes, areas=areas, name=gfs, date=date,
                    run=run, start_time=0, step_time=6, end_time=288 )
    # Make extra animations
    download_model( weather_types=wtypes, areas=areas, name=gfs, date=date,
                    run=run, start_time=0, step_time=6, end_time=120 )
    download_model( weather_types=wtypes, areas=areas, name=gfs, date=date,
                    run=run, start_time=120, step_time=6, end_time=240 )
    download_model( weather_types=wtypes, areas=areas, name=gfs, date=date,
                    run=run, start_time=240, step_time=6, end_time=384 )


def download_model_ec(date, run):
    '''Function downloads model ecmwf with seceral options'''
    wtypes = [overview, temp2meter] #, sum_precip, wind10m, hPa850 , winterview, snowdepth
    areas  = [europe_atlantic, benelux] # europe,

    download_model( weather_types=wtypes, areas=areas, name=ecmwf, date=date,
                    run=run, start_time=0, step_time=6, end_time=240 )
    # Make extra animations
    download_model( weather_types=wtypes, areas=areas, name=ecmwf, date=date,
                    run=run, start_time=0, step_time=6, end_time=120 )
    download_model( weather_types=wtypes, areas=areas, name=ecmwf, date=date,
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
            gfs_time = anim.hh_mm_ss_add_hour(stime, 2) # Add two hours
            ecm_time = anim.hh_mm_ss_add_hour(stime, 3) # Add three hours

            # Get dates
            wait_date, model_date = anim.yyyymmdd_now(), anim.yyyymmdd_now()
            # For the 18 hour we need to wait for the next day
            if run == '18': wait_date = anim.yyyymmdd_next_day()

            # ICON, first
            anim.pause( stime, wait_date, f'download model run {run} ICON at' )
            download_model_icon_eu(model_date, run)

            # GFS, one hour later
            anim.pause( gfs_time, wait_date, f'download model run {run} GFS at' )
            download_model_gfs(model_date, run)

            # ECMWF, only 00 and 12 run and three hours later
            if run in ['00','12']:
                anim.pause( ecm_time, wait_date, f'download model run {run} ECMWF at' )
                download_model_ec(model_date, run)


if __name__ == "__main__":
    '''
    # WXCHARTS EXAMPLES
    '''
    # EXAMPLE ECMWF
    # model(  name            = ecmwf,               # Which weather model
    #         option          = overview,            # Option output temp, overview
    #         area            = europe_atlantic,     # Options for area eg. euratl europe france germany low_countries
    #         date            = anim.yyyymmdd_now(), # Date of run format yyyymmdd
    #         run             = '00',                # Options for time eg. 00, 06, 12, 18
    #         start_time      = 0,                   # Start image
    #         step_time       = 24,                  # Step time between images
    #         end_time        = 240,                 # End image
    #         animation_time  = cfg.animation_time,  # Animation interval time for gif animation
    #         download_map    = cfg.download_dir,    # Map for downloading the images too
    #         animation_map   = cfg.animation_dir,   # Map for the animations
    #         remove_download = cfg.remove_download, # Remove the downloaded images
    #         gif_compress    = cfg.gif_compress,    # Compress the size of the animation
    #         date_submap     = cfg.date_submap,     # Set True to create extra date submaps
    #         date_subname    = cfg.date_subname,    # Set True to create extra date in files
    # )

    # model( icon_eu, overview,   europe,  anim.yyyymmdd_now(), '12', 0, 3, 120 )
    # model( icon_eu, temp2meter, benelux, anim.yyyymmdd_now(), '12', 0, 3, 120 )

    ############################################################################
    # Example daily repeating download_
    # Download everyday the same run at the same time

    download_daily()
