#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
without_file.py
Module similar to the main module with the exception that the
tickers are sent as arguments
"""

from sys import argv
from thread import run_threads
from analyse_ticker import print_datas

if __name__ == "__main__":
    stocks = argv[1:]
    threads = run_threads(stocks)

    for thread in threads:
        thread.join()

    print_datas()
