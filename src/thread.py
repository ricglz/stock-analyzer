#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
thread.py
Module containing the logic to threading
"""

from threading import Thread, Lock

from time import sleep

from analyse_ticker import analyse_ticker
from utils import chunks

class TickerThread(Thread):
    """Thread for checking the ticker data in parallel"""
    def __init__(self, ticker):
        Thread.__init__(self)
        self.ticker = ticker

    def run(self):
        analyse_ticker(self.ticker)

def run_threads(stocks):
    """
    Function that runs a ticker thread based on the element
    of the stocks array.

    All of this by avoiding a possible connection error by
    creating chunks of elements and sleeping after each chunk
    was processed
    """
    print(f'Analysing {len(stocks)} stock')

    Lock()
    threads = []

    for chunk in chunks(stocks, 50):
        for ticker in chunk:
            thread = TickerThread(ticker)
            thread.start()
            threads.append(thread)
        sleep(0.1)

    return threads
