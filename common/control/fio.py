# -*- coding: utf-8 -*-
'''Functions for io file handling.
   Creating, writing, deleting, downloading, unzipping a file'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright (C) Mark Zwaving. All rights reserved.'
__license__    =  'MIT License'
__version__    =  '0.1.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg
import view.console as cnsl
import model.ymd as ymd
import model.validate as validate
import model.util as util
import threading, urllib, json, os, time, zipfile, subprocess, sys, webbrowser
import datetime, requests, socket, shutil

def check(fname, verbose=False):
    '''Function checks a file for existence'''
    ok, verbose = False, cnsl.verbose(verbose)
    cnsl.log(f'Start check a file {ymd.now()}', verbose)
    cnsl.log(f'File {fname}', verbose)
    with threading.Lock():
        try:
            if os.path.exists(fname):  # Check if is there file
                ok = True
        except Exception as e:
            cnsl.log(f'Error check\n{e}', cfg.error)
        else:
            if ok:
                cnsl.log('File exists', verbose)
            else:
                cnsl.log('File does not exist', verbose)
    cnsl.log('End check file', verbose)
    return ok

def write(path='dummy.txt', content='', prefix='w', encoding='utf-8', verbose=False):
    '''Function writes content to a file'''
    ok, verbose = False, cnsl.verbose(verbose)
    cnsl.log(f'Start write a file {ymd.now()}', verbose)
    cnsl.log(f'File {path}', verbose)
    with threading.Lock():
        try:
            mk_dir(os.path.dirname(path), verbose) # Make maps
            with open(path, prefix, encoding=encoding) as f:
                f.write(content)
        except Exception as e:
            cnsl.log(f'Error writing file\n{e}', cfg.error)
        else:
            cnsl.log('Write file success', verbose)
            ok = True
    cnsl.log(f'End write a file', verbose)
    return ok

def save(fname='dummy.txt', content='', prefix='w', encoding='utf-8', verbose=False):
    '''Function writes content to a file'''
    return write(fname, content, prefix, encoding, verbose)

def read(fname, verbose=False):
    '''Function reads the content in a file'''
    ok, verbose, t = False, cnsl.verbose(verbose), ''
    cnsl.log(f'Start read a file {ymd.now()}', verbose)
    cnsl.log(f'File {fname}', verbose)
    with threading.Lock():
        if check(fname):
            try:
                with open(fname, 'r') as f:
                    t = f.read()
            except Exception as e:
                cnsl.log(f'Error reading a file\n{e}', cfg.error)
            else:
                cnsl.log('Read file success', verbose)
                ok = True
    cnsl.log('End read a file', verbose)
    return ok, t

def delete(fname, verbose=False):
    '''Function deletes a file if exists'''
    ok, verbose = False, cnsl.verbose(verbose)
    cnsl.log(f'Start delete a file {ymd.now()}', verbose)
    cnsl.log(f'File {fname}', verbose)
    with threading.Lock():
        if check(fname):
            try:
                os.remove(fname)  # Remove file
            except Exception as e:
                cnsl.log(f'Error deleting a file\n{e}', cfg.error)
            else:
                cnsl.log('Delete file success', verbose)
                ok = True
        else:
            cnsl.log(f'Cannot delete. File does not exist', verbose)
    cnsl.log('End delete a file', verbose)
    return ok

def rm_file(fname, verbose=False):
    '''Function removes a file if exists (canonical) for delete()'''
    return delete(fname, verbose)

def rm_files_from_lst( lst = [], empty_dir=True, verbose=False):
    '''Function tries to remove all downloaded images in the list.
       Removes a direcory if empty too.'''
    ok, verbose = False, cnsl.verbose(verbose)
    cnsl.log(f'Start remove files from list {ymd.now()}', verbose)
    lst = list(set(lst)) # Make list unique
    for p in lst: # Walkthrough paths
        if delete(p): # Remove file from disk
            # Remove only empty maps (recursive)
            map = os.path.dirname(p) # Get map from path
            while empthy_dir: # Remove only empthy maps
                if is_map_empty(map): # Remove only empty maps
                    rm_dir(map) # Remove map
                    map = os.path.dirname(map) # Go to upper dir
                else:
                    break
    cnsl.log('End remove files from list', verbose)

def mk_dir(path, verbose=False):
    '''Function makes a map if not already exists'''
    ok, verbose = False, cnsl.verbose(verbose)
    cnsl.log(f'Start make a directory {ymd.now()}', verbose)
    cnsl.log(f'Map {path}', verbose)
    with threading.Lock():
        try:
            if os.path.isdir(path):
                cnsl.log('Map not made because it already exists.')
                ok = True
            else:
                os.makedirs(path)
        except Exception as e:
            cnsl.log(f'Error make directory{e}', cfg.error)
        else:
            cnsl.log('Make directory success', verbose)
            ok = True
    cnsl.log(f'End make a directory', verbose)
    return ok

# Function removes a map, empthy or not
def rm_dir(
        map, # Map to remove
        verbose=False
    ):
    '''Function deletes an directory empty or not'''
    ok, verbose = False, cnsl.verbose(verbose)
    cnsl.log(f'Start remove a directory {ymd.now()}', verbose)
    cnsl.log(f'Map {map}', verbose)
    with threading.Lock():
        if os.path.exists( map ):
            try:
                shutil.rmtree(map)
            except Exception as e:
                cnsl.log(f'Error removing map\n{e}', cfg.error)
            else:
                cnsl.log('Remove map succes', verbose)
                ok = True
        else:
            cnsl.log('Cannot remove map. Map does not exist.', verbose)
    cnsl.log('End remove a directory', verbose)
    return ok

def is_dir_empthy(dir, verbose=False):
    ok, verbose = False, cnsl.verbose(verbose)
    cnsl.log(f'Start check for an empty map {ymd.now()}', verbose)
    if os.path.exists(dir):
        ok = True if len(os.listdir(dir)) == 0 else False
    else:
        cnsl.log('Map does not exist.', verbose)
        ok = True
    cnsl.log('End check for an empty map', verbose)
    return ok

def unzip(zip, txt, verbose=False):
    '''Function unzips a zipfile'''
    ok, verbose = False, cnsl.verbose(verbose)
    cnsl.log(f'Start unzip a file {ymd.now()}', verbose)
    cnsl.log(f'From {zip}\nTo {txt}') # TODO force to txt file
    with threading.Lock():
        try:
            dir_txt = os.path.dirname(txt)
            with zipfile.ZipFile(zip, 'r') as z:
                z.extractall(dir_txt)
        except Exception as e:
            cnsl.log(f'Error unzip\n{e}', cfg.error)
        else:
            cnsl.log('Unzip success', verbose)
            ok = True
    cnsl.log('End unzip a file', verbose)
    return ok

def download(
        url,  # Url to download
        path, # Path to download the file to
        check   = True,  # <optional> Check file True will not overwrite the file if exists
        verbose = False  # <optional> Overwrite default value verbose -> see config.py
    ):
    '''Function downloads a file from an internet url'''
    ok, verbose = False, cnsl.verbose(verbose)
    cnsl.log(f'Start download {ymd.now()}', verbose)
    cnsl.log(f'From {url}\nTo {path}', verbose)

    # Check if image is already downloaded
    if check and os.path.exists(path):
        cnsl.log(f'Download skipped, file already exists', verbose)
        ok = True
    else:
        with threading.Lock():
            if url_exists(url): # Check if a url exists
                try:
                    mk_dir(os.path.dirname(path)) # Make map if not exists
                    urllib.request.urlretrieve( url, path ) # Download file
                except Exception as e:
                    cnsl.log(f'Error in download {e}', cfg.error)
                else:
                    cnsl.log('Download success', verbose)
                    ok = True
            else:
                cnsl.log(f'Url {url} does not exist', True)
        # Do not flood server protection
        wait = cfg.download_interval_time
        time.sleep(0.2 if wait < 0.2 else wait)

    cnsl.log(f'End download a file', verbose)
    return ok

def download_read_file(url, file, verbose=False):
    '''Function downloads a file, read the file and return the content of the file'''
    ok, verbose, t = False, cnsl.verbose(verbose), ''
    cnsl.log(f'Start download and read a file {ymd.now()}', verbose)
    if has_internet():
        ok = download( url, file )
        if ok: ok, t = read(file)
    else:
        t = 'Cannot download file. There is no internet connection'
        console.log(t, cfg.error)
    cnsl.log('End download and read a file', verbose)
    return ok, t

def request(url, type='txt', verbose=False):
    '''Function makes the request based on the url given as parameter
       The return values are: ok, True if success else False... And the text From
       the request.'''
    ok, verbose, t = False, cnsl.verbose(verbose), ''
    cnsl.log(f'Start a - {type} - request from an url {ymd.now()}', verbose)
    cnsl.log(f'Url {url}', verbose)
    with threading.Lock():
        try:
            resp = urllib.request.urlopen( url )
            data = resp.read()
            if type == 'text':
                t = data
            elif type == 'json':
                t = json.loads(data)
        except Exception as e:
            cnsl.log(f'Error request\n{e}', cfg.error)
        else:
            cnsl.log('Request success', verbose)
            ok = True
    cnsl.log('End request from an url', verbose)
    return ok, t

def request_text(url, verbose=False):
    '''Function makes an online request for a text file'''
    return request(url, 'txt', verbose)

def request_json( url, verbose=False):
    '''Function makes an online request for a json file'''
    return request(url, 'json', verbose)

def has_internet(verbose=False):
    '''Function checks if there is a internet connection available'''
    ok = False
    cnsl.log(f'Start check internet connection {ymd.now()}', verbose)
    cnsl.log(f'Url {url}', verbose)
    with threading.Lock():
        try:
            sock = socket.create_connection(("1.1.1.1", 53))
            if sock: sock.close()
        except Exception as e:
            cnsl.log(f'Check failed\n{e}', cfg.error)
        else:
            cnsl.log('Check succes', verbose)
            ok = True
    cnsl.log('End check internet connection', verbose)
    return ok

# Function checks if a url exists
def url_exists(url, verbose=False):
    '''Function checks if a url exists. Return True or False'''
    cnsl.log(f'Start check url for existence {ymd.now()}', verbose)
    cnsl.log(f'Url {url}', verbose)
    with threading.Lock():
        try:
            resp = requests.head(url)
            ok = True if resp.status_code == 200 else False
        except Exception as e:
            cnsl.log(f'Error url exist\n{e}', cfg.error)
        else:
            cnsl.log('Url exists', verbose)
            ok = True
    cnsl.log('End check internet connection', verbose)
    return ok

# Function get files in a dir. Filering can be done based on keywords and extenions
def file_lst(
        map,             # Map to search for files
        extensions = '', # <optional> List of extensions or one string ext to search the map for
        keywords   = '', # <optional> List of keyword or one string to search the directory for
        case_insensitive = True, # <optional> Search case insensitive. True by default.
        verbose = False  # <optional> Overwrite verbose option
    ):
    '''Function list files in a directory. The list can be filtered by keywords
       and extensions.'''
    verbose = False, cnsl.verbose(verbose)
    cnsl.log(f'Start list files directory {ymd.now()}', verbose)
    cnsl.log(f'Search map {map}', verbose)
    results = [] # List with found paths

    if not os.path.exists(map): # Check map
        cnsl.log(f'Path {map} does not exist', verbose)
    else:
        # Check types and add to an (empty) list element if needed
        if type(keywords)   is list: keywords   = keywords   if keywords   else ''
        if type(extensions) is list: extensions = extensions if extensions else ''
        if type(keywords)   is str:  keywords   = [keywords]
        if type(extensions) is str:  extensions = [extensions]
        len_key = len(keywords)   if keywords[0]   else 0 # Count keywords
        len_ext = len(extensions) if extensions[0] else 0 # Count extensions
        filter_on = True if (len_key + len_ext) > 0 else False # Filter on ?
        if len_key > 0: cnsl.log(f'Search words \'{",".join(keywords)}\'', verbose)
        if len_ext > 0: cnsl.log(f'Search extensions \'{",".join(extensions)}\'', verbose)

        # Validate extensions, add point if needed
        if len_key > 0: extensions = [validate.extension(ext) for ext in extensions]

        # Get all the files in the directory
        files = [f for f in os.listdir(map) if os.path.isfile( util.mk_path(map,f) )]

        # Make search lists case in-sensitive if set
        if case_insensitive:
            extensions = [el.lower() for el in extensions]
            keywords   = [el.lower() for el in keywords]

        # Filter files based on extensions and keywordsfname =
        for f in files:
            # Get name and extension
            fname, ext =  os.path.splitext(f)

            # Make case insensitive if needed
            if case_insensitive: fname, ext = fname.lower(), ext.lower()

            found = True # True by defaults
            if filter_on: # We need to check for words
                found_word, found_ext = False, False # Found is False by default
                # Check words and extensions
                if len_key > 0: # Check only if there are words to check
                    # Check if keywords are in name
                    if len([w for w in keywords if w in fname]) > 0:
                        found_word = True # Part word is found
                else: # All words are True
                    found_word = True

                if len_ext > 0: # Check only if there are extensions to check
                    # Check if extension is found
                    if len([e for e in extensions if e == ext]) > 0:
                        found_ext = True # Extension is found
                else: # All extensions are True
                    found_ext = True

                # Both must True
                found = found_word and found_ext

            if found: # If found add file path to results
                p = util.mk_path(map, f)
                cnsl.log(f'File found {p}', verbose)
                results.append(p)

    cnsl.log(f'End list files directory', verbose)
    return results


# Function downloads in interval for a period of time and returns a list with
# the images
def download_interval(
       url,          # Url for the files on the web
       map           = cfg.dir_download, # Map for the downloads
       interval      = 10,    # Interval time for downloading Images (minutes)
       duration      = 1*60,  # Total time for downloading all the images (minutes)
       date_submap   = False, # Set True to the possible given date submaps
       date_subname  = False, # Add date and time to downloaded files
       check         = True,  # No double downloads check
       verbose       = False  # With output to screen
    ):
    '''Download files from the web in interval for a period of time.
       Returns a list with the names of the downloaded files.'''
    verbose = cnsl.verbose(verbose)
    # Update map
    base_map, submap = map, util.url_name(url)
    y, m, d = ymd.yyyy_mm_dd_now()
    map = util.mk_path(base_map, f'{y}/{m}/{d}/{submap}') if date_submap else base_map
    cnsl.log(f'Start interval download {ymd.now()}', verbose)
    cnsl.log(f'Internet url is {url}', verbose)
    cnsl.log(f'Download map is {map}', verbose)
    cnsl.log(f'Interval time is {interval} minutes', verbose)
    cnsl.log(f'Duration time is {duration} minutes', verbose)

    num_act   = 1 # This is used to number the files
    num_max   = 10000 # Maximum number files for interval downloads
    fail_cnt  = 1  # Count failures
    fail_try  = 10 # How many tries
    fail_next = 60 # Wait for next try
    lpaths    = [] # List for the downloaded files with their name

    # Get name and extension of downloaded file
    name, ext = os.path.splitext(os.path.basename(url))
    ext = validate.extension(ext) # Check extension

    # Calculate end time (in seconds) for downloading files
    time_end = int(round(duration * 60)) + time.time()
    time_interval = int(round(interval * 60)) # Calculate interval seconds
    time_download = 0 # Epoch seconds. Set to 0 to always start a download for the first time

    cnsl.log(' ', verbose) # Spacer
    # Start download loop
    while True:
        time_act = time.time() # Get current time (epoch seconds)

        # Extern time shift (eg. wintertime). Wait untill we are at last time
        while time_download > time_act: time_act = time.time()

        y, m, d, hh, mm, ss = ymd.y_m_d_h_m_s_now() # Get current date and time
        yyyymmdd_act = f'{y}{m}{d}' # Make current date

        # Update map only if date_submaps is True
        map = util.mk_path(base_map, f'{y}/{m}/{d}/{submap}') if date_submap else base_map

        # Make a download file name
        fname = f'{name}_{num_act}'
        if date_subname: fname += f'_{y}{m}{d}_{hh}{mm}{ss}'
        fpath = util.mk_path(map, f'{fname}{ext}') # Download path

        # Try to download image
        while fail_cnt <= fail_try:
            ok = download(url, fpath, check, verbose) # Download image and always show
            if ok: # If download is a succes
                lpaths.append(fpath) # Add image to downloaded images list
                num_act += 1 # Update num for next file only if download is a success
                break
            else: # Download failed.
                for i in range(fail_next):
                    t  = f'Download failed {fail_cnt} time(s), '
                    t += f'next try in {fail_next-i} seconds'
                    if cfg.timer: cnsl.log_r(t, cfg.error)
                    elif i == 0: cnsl.log(t, cfg.error) # Only once
                    time.sleep(1)

                fail_cnt += 1 # Increase fails

        # Check time to stop or too much files reached
        if time_act >= time_end or num_act >= num_max: break  # Done

        # Update vars
        time_download = time_act # Update last_download time
        fail_cnt = 1 # Try next image, next time

        # Wait untill next download
        dt = datetime.datetime.fromtimestamp(time_download + time_interval)
        util.pause( dt.strftime('%H:%M:%S'), dt.strftime('%Y%m%d'),
                    f'next ({num_act}) download {name} at' )

    cnsl.log('End interval download', verbose)
    return lpaths

def rm_lst(lst = [], remove_empty=False, verbose = False):
    '''Function tries to remove all files in the list.'''
    verbose = cnsl.verbose(verbose)
    cnsl.log(f'Start remove files in list {ymd.now()}', verbose)
    for path in list(set(lst)): # Make list unique and walkthrough paths
        if delete(path, verbose): # Remove file from disk
            dir = os.path.dirname(path) # Get map from path
            # Remove maps only empty maps and remove_empty is True
            while is_dir_empthy(dir, verbose) and remove_empty:
                rm_dir(dir, verbose) # Remove empty map
                dir = os.path.dirname(dir) # Go to upper dir
    cnsl.log('End remove files from list', verbose)

# Function downloads a list of files uries on the web to a local path list
def download_lst(
        uries,         # List with download urls
        paths = [],    # <optional> List with names for the files from the download urls
        check = True,  # Already download check. Do not overwrite download file
        verbose = False # Output to screen
    ):
    '''Downloads images based on two lists. It combines an uries list with a path list'''
    verbose = cnsl.verbose(verbose)
    cnsl.log(f'Start downloading images from list {ymd.now()}', verbose)
    if uries:
        if not paths: # If no paths, make them based on the uries
            for url in uries:
                locnet = util.url_name(url) # Get name url
                name, ext = util.name_ext(path) # Get name and extension
                ext = validate.extension(ext) # Handle dot.
                path = mk_path(cfg.dir_download, f'{locnet}_{name}{ext}') # Make image path
                paths.append(path) # Add to list

        res_urie, res_path, max = [], [], cfg.download_max_num
        # Combine/zip the two lists (with download paths and web urls) into one list
        for path, url in tuple(zip(paths[:max], uries[:max])): # Loop through img and url objects
            ok = download(url, path, check, verbose) # Download file
            if ok: # Success add to lists
                res_urie.append(url)
                res_path.append(path)
    else:
        cnsl.log('List uries is empty', verbose)

    cnsl.log('End downloading images from list', verbose)
    return res_urie, res_path # Return correct paths
