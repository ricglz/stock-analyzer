#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module in charge of managing the stock and its analystic values
"""
from datetime import datetime

import matplotlib.dates as mdates
import pandas_datareader.data as web

from ema import calculate_ema
from macd import calculate_macd
from rsi import calculate_rsi
from sma import calculate_sma


class Stock:
    closes = None
    dates = None
    macd = None
    rsi = None
    signal_line = None


    def __init__(self, ticker, start, end=datetime.now()):
        """
        Different sources for pulling data can be found here:
        https://readthedocs.org/projects/pandas-datareader/downloads/pdf/latest/
        """
        stock_data = web.DataReader(ticker, 'yahoo', start, end)

        self.ticker = ticker
        self.dates = [mdates.date2num(d) for d in stock_data.index]
        self.closes = stock_data['Close']

        self.macd = calculate_macd(self.closes)
        self.rsi = calculate_rsi(self.closes)
        self.signal_line = calculate_ema(self.closes, 9)

    def sma(self, period):
        """
        Calculates the sma of the closes based on a period
        """
        return calculate_sma(self.closes, period)

    def is_currently_bullish(self):
        return self.macd[-1] > self.signal_line[-1]
