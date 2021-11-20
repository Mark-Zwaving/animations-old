# -*- coding: utf-8 -*-
'''Functions date time base handling'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.0.7'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import datetime, time
import view.console as cnsl

def now():
    '''Function returns a date time string'''
    y, m, d, h, mi, s = y_m_d_h_m_s_now()
    return f'{y}-{m}-{d} {h}:{mi}:{s}'

def yyyymmdd_now():
    '''Function gets current year, month and day in string format <yyyymmdd>.'''
    return datetime.datetime.now().strftime('%Y%m%d')

def hhmmss_now():
    '''Function gets current time in hours, minutes and seconds format <hhmmss>'''
    return datetime.datetime.now().strftime('%H%M%S')

def yyyy_mm_dd_now():
    '''Function gets current year, month and day in string format yyyy, mm, dd .'''
    return split_yyyymmdd( yyyymmdd_now() )

def hh_mm_ss_now():
    '''Function returns the current time in hours, minutes and seconds format hh, mm, ss
       with leading seconds'''
    return split_hhmmss( hhmmss_now() )

def split_yyyymmdd(
        yyyymmdd # Format yyyymmdd
    ):
    '''Function will slice the string the three parts yyyy, mm and dd'''
    ymd = str(yyyymmdd)
    return ymd[:4], ymd[4:6], ymd[6:8]

def split_yyyy_mm_dd(
        yyyy_mm_dd # Format yyyy-mm-dd
    ):
    '''Function will split the string the three parts yyyy, mm and dd'''
    return yyyy_mm_dd.split('-')

def split_hhmmss(
        hhmmss # Format hhmmss
    ):
    '''Function will slice the string in three parts hh, mm and dd'''
    hms = str(hhmmss)
    return hms[:2], hms[2:4], hms[4:6]

def split_hh_mm_ss(
        hh_mm_ss # Format hh:mm:ss
    ):
    '''Function will split the timestring by : in three parts hh, mm and dd'''
    return hh_mm_ss.split(':')

def split_yyyymmdd_hhmmss(
        yyyymmdd,
        hhmmss
    ):
    hh, mm, ss = split_hhmmss(hhmmss) # Format hhmmss
    y, m, d = split(yyyymmdd)
    return y, m, d, hh, mm, ss

def split_yyyymmdd_hh_mm_ss(
        yyyymmdd,
        hh_mm_ss
    ):
    hh, mm, ss = split_hh_mm_ss(hh_mm_ss) # Format hhmmss
    y, m, d = split_yyyymmdd(yyyymmdd)
    return y, m, d, hh, mm, ss

def yyyy_mm_dd_now():
    '''Function gets current year, month and day in string format with a
       leading zero for month and day.'''
    return split_yyyymmdd( yyyymmdd_now() ) # Return current year, month and day

def hh_mm_ss_now():
    '''Function gets current time in hours, minutes and seconds with a leading zero'''
    return split_hhmmss( hhmmss_now() ) # Return current hours, minutes, seconds (with a leading zero)

def y_m_d_h_m_s_now():
    '''Function returns current yyyy year, month mm, day dd, hour hh,
       minutes mi, seconds ss, with leading zeros'''
    y, m, d = yyyy_mm_dd_now()
    hh, mm, ss = hh_mm_ss_now()
    return y, m, d, hh, mm, ss

def hh_mm_ss_plus_second(
        hh_mm_ss = '', # Time string format hh:mm:ss
        second = 1     # Seconds to add
    ):
    '''Function adds seconds to time string, format hh:mm:ss'''
    # if time hh_mm_ss not given get current time
    hh, mm, ss = hh_mm_ss.split(':') if hh_mm_ss else hh_mm_ss_now()
    y, m, d = yyyy_mm_dd_now()
    dt = datetime.datetime(int(y),int(m),int(d),int(hh),int(mm),int(ss))+datetime.timedelta(seconds=second)
    return dt.strftime('%H:%M:%S')

def hh_mm_ss_minus_second(
        hh_mm_ss = '', # Time string format hh:mm:ss
        second = 1     # Seconds to substract
    ):
    '''Function substract seconds of time string, format hh:mm:ss'''
    return hh_mm_ss_plus_second( hh_mm_ss, -second) # Just make seconds negative

def hh_mm_ss_plus_minute(
        hh_mm_ss = '', # Time string format hh:mm:ss
        minute = 1 # Minutes to add
    ):
    '''Function adds minutes to time string, format hh:mm:ss'''
    return hh_mm_ss_plus_second(hh_mm_ss, minute * cfg.sec_minute)

def hh_mm_ss_minus_minute(
        hh_mm_ss = '', # Time string format hh:mm:ss
        minute = 1 # Minutes to substract
    ):
    '''Function substract minutes of time string, format hh:mm:ss'''
    return hh_mm_ss_plus_minute( hh_mm_ss, -minute)

def hh_mm_ss_plus_hour(
        hh_mm_ss = '', # Time string format hh:mm:ss
        hour = 1 # Hours to add
    ):
    '''Function adds hours to time string, format hh:mm:ss'''
    return hh_mm_ss_plus_second(hh_mm_ss, hour * cfg.sec_hour)

def hh_mm_ss_minus_hour(
        hh_mm_ss = '', # Time string format hh:mm:ss
        hour = 1  # Hours to substract
    ):
    '''Function substracts hours of time string, format hh:mm:ss'''
    return hh_mm_ss_plus_hour(hh_mm_ss, -hour)

def yyyymmdd_plus_second(
        yyyymmdd = '',  # Date to add the seconds to
        second  = 0    # Seconds to add/substract seconds to date
    ):
    '''Functions adds or substracts one or more seconds to a given date'''
    yyyymmdd = yyyymmdd if yyyymmdd else yyyymmdd_now() # If empty get current date
    y, m, d = split_yyyymmdd( yyyymmdd ) # Split date
    dt_new = datetime.datetime(int(y),int(m),int(d)) + datetime.timedelta(seconds=second)
    return dt_new.strftime('%Y%m%d') # Return new yyyymmmdd string

def yyyymmdd_minus_sec(
        yyyymmdd = '',  # Date to add the seconds to
        second  = 0    # Seconds to substract seconds to date
    ):
    return yyyymmdd_plus_second(yyyymmdd, -second)

def yyyymmdd_plus_hour(
        yyyymmdd = '',  # String date format is <yyyymmdd>
        hour = 1       # Integer/float add hours to a current day,
    ):
    '''Add or substract one or more days from date format <yyyymmdd>.
       If date is not given is uses current date.'''
    return yyyymmdd_plus_second(yyyymmdd, hour * cfg.sec_hour)  # Add the hours seconds to date

def yyyymmdd_minus_hour(
        yyyymmdd = '',  # String date format is <yyyymmdd>
        hour = 1       # Integer/float substract hours from current day,
    ):
    return yyyymmdd_plus_hour(yyyymmdd, -hour)

def yyyymmdd_plus_day(
        yyyymmdd = '', # String date format is <yyyymmdd>
        day = 1        # Integer/float add if positive and substract if negative days from current day,
    ):
    '''Add or substract one or more days from date format <yyyymmdd>.
       If date is not given is uses current date.'''
    return yyyymmdd_plus_second(yyyymmdd, day * cfg.sec_day)  # Add the day seconds to date

def yyyymmdd_minus_day(
        yyyymmdd = '', # String date format is <yyyymmdd>
        day = 1        # Integer/float add if positive and substract if negative days from current day,
    ):
    return yyyymmdd_plus_day(yyyymmdd, -day)

def yyyymmdd_plus_week(
        yyyymmdd = '', # String date format is <yyyymmdd>
        week = 1       # Integer/float add if positive and substract if negative days from current day,
    ):
    '''Add or substract one or more days from date format <yyyymmdd>.
       If date is not given is uses current date.'''
    return yyyymmdd_plus_second(yyyymmdd, week * cfg.sec_week)  # Add the week seconds to date

# Short fn for adding a day to date
def yyyymmdd_next_day( yyyymmdd = '' ):
    '''Get date of next day in format <yyyymmdd>'''
    return yyyymmdd_plus_day(yyyymmdd, 1)

def yyymmdd_previous_day( yyyymmdd = '' ):
    '''Get date of next day in format <yyyymmdd>'''
    return yyyymmdd_minus_day(yyyymmdd, 1)

def yyyymmdd_next_week( yyyymmdd = '' ):
    '''Get date of next week in format <yyyymmdd>'''
    return yyyymmdd_plus_week(yyyymmdd, 1)

def yyymmdd_previous_week( yyyymmdd = '' ):
    '''Get date of previous week in format <yyyymmdd>'''
    return yyyymmdd_minus_week(yyyymmdd, 1)

def yyyymmdd_range_lst(ymds, ymde, verbose=None): # Probably slow fn
    '''Function makes a ordered list of dates with format yyyymmdd'''
    ok = False
    cnsl.log(f'Start make a range date list {now()}', verbose)
    cnsl.log(f'From {ymds} to {ymde}', verbose)
    res, iymds, iymde = [], int(ymds), int(ymde) # Make int to compare
    reverse = True if iymds > iymde else False # Check reverse order
    if reverse: imem = iymds; iymds = iymde; iymde = imem # Swap start, end if reverse
    while iymds <= iymde: # Make a list with ordered dates
        cnsl.log_r(f'{iymds} - {iymde}', verbose)
        res.append(iymds)
        iymds = int( yyyymmdd_plus_day(iymds) ) # Get next day
    if reverse: result.reverse() # Reverse list, if True
    cnsl.log(f'End make a range date list', verbose)
    return result

def epoch_act():
    '''Function returns current epoch seconds (integer)'''
    return int(time.time())

# Functions gets the epoch seconds for a date and time
def dt_to_epoch(
        yyyymmdd, # String date format <yyyymmdd>
        hh_mm_ss  # String time format <HH:MM:SS>
    ):
    '''Function converts a date time string with the format 'yyyymmdd-HH:MM'
       to epoch seconds'''
    y, m, d, hh, mm, ss = split_yyyymmdd_hh_mm_ss(yyyymmdd, hh_mm_ss )
    dt = datetime.datetime.fromisoformat(f'{y}-{m}-{d} {hh}:{mm}:{ss}.000')
    return int( dt.timestamp() ) # Return integer epoch seconds

def epoch_to_yyyymmdd(
        epoch = 0 # Epoch seconds
    ):
    '''Function translate epoch seconds to ymd with format: yyyymmdd'''
    return datetime.datetime.fromtimestamp(epoch).strftime('%Y%m%d')

# Function checks if there is a (minute) time shift
def is_time_shift(
        epoch_1, # First time (seconds)
        epoch_2, # Second time (seconds)
        diff=cfg.sec_minute # Difference in time to check for (seconds)
    ):
    '''Function check if there is a timeshift of default one minute'''
    return True if abs(epoch_1 - epoch_2) >= diff else False
