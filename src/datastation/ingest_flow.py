import argparse
import json
import logging
import os, grp
import shutil

import requests
from builtins import all
import stat

file_writeable_to_group = lambda f: os.stat(f).st_mode & stat.S_IWGRP > 0

def start_import(service_baseurl, path, is_batch, continue_previous, is_migration, is_dry_run):
    if not has_dirtree_pred(path, file_writeable_to_group):
        chmod_command = "chmod -R g+w %s" % path
        print("Some files in the import batch do not give the owner group write permissions. Executing '%s' to fix it" % chmod_command)
        status = os.system(chmod_command)
        if status != 0:
            print("Could not give owner group write permissions. Possibly your account is not the owner user of the files.")
            return
    print("Sending start import request to server...")
    command = {
        'inputPath': os.path.abspath(path),
        'batch': is_batch,
        'continue': continue_previous
    }
    if is_dry_run:
        logging.info("Only printing command, not sending it...")
        print(json.dumps(command, indent=2))
    else:
        r = requests.post('%s/%s/:start' % (service_baseurl, "migrations" if is_migration else "imports"), json=command)
        print('Server responded: %s' % r.text)

def has_file_pred(file, pred):
    return pred(file)

def has_dirtree_pred(dir, pred):
    for root, dirs, files in os.walk(dir):
        return pred(root) \
               and all(pred(os.path.join(root, dir)) for dir in dirs) \
               and all(pred(os.path.join(root, file)) for file in files)

def list_events(service_baseurl, params):
    r = requests.get('%s/events' % service_baseurl, headers={'Accept': 'text/csv'}, params=params)
    print(r.text)

def set_permissions(dir, dir_mode, file_mode, group):
    for root, dirs, files in os.walk(dir):
        for d in [root] + dirs:
            p = os.path.join(root, d)
            os.chmod(p, dir_mode)
            shutil.chown(p, group=group)
        for f in files:
            p = os.path.join(root, f)
            os.chmod(p, file_mode)
            shutil.chown(p, group=group)

def is_dir_in_inbox(dir, inboxes):
    return next(filter(lambda p: is_subpath_of(dir, p),  inboxes), None) is not None

def is_subpath_of(dir, parent):
    absolute_parent = os.path.abspath(parent)
    absolute_dir = os.path.abspath(dir)
    return absolute_dir.startswith(absolute_parent)

def progress_report(deposit_dir, ingest_areas):
    # find the ingest area
    # find the relative path (assume first dir is inbox?)
    #
    return ""