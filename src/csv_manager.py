#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
csv_manager.py

Module to store data or read from csv if the file is older than
a day.
"""
from datetime import date, timedelta
from os import stat

from pandas import read_csv

def get_data(path, complex_func, *args):
    """
    @arg path. The file's path for storing or reading
    @arg complex_func. Function to get the data
    @arg args. Arguments for the complex_func function

    Stores data or read from csv based if the file is older than
    a day. In addition it returns the data pulled or read.
    """
    last_modified = None
    today = date.today()
    try:
        last_modified = date.fromtimestamp(stat(path).st_mtime)
    except FileNotFoundError:
        last_modified = today - timedelta(days=1)
    data = None
    if last_modified < today:
        data = complex_func(*args)
        data.to_csv(path)
    else:
        data = read_csv(path)
    return data
