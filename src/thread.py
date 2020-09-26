#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
from analyse_ticker import analyse_ticker

class TickerThread(Thread):
    """Thread for checking the ticker data in parallel"""
    def __init__(self, ticker):
        Thread.__init__(self)
        self.ticker = ticker

    def run(self):
        analyse_ticker(self.ticker)
