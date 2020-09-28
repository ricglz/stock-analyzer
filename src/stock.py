#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module in charge of managing the stock and its analystic values
"""
from datetime import date, timedelta
from os import stat

import matplotlib.dates as mdates
from pandas_datareader.data import get_data_yahoo
from pandas import DataFrame, read_csv

from ema import calculate_ema
from macd import calculate_macd
from rsi import calculate_rsi
from sma import calculate_sma

def get_stock_data(ticker, start, end):
    last_modified = None
    stock_file = 'csvs/history/{}.csv'.format(ticker)
    today = date.today()
    try:
        last_modified = date.fromtimestamp(stat(stock_file).st_mtime)
    except FileNotFoundError:
        last_modified = today - timedelta(days=1)
    stock_data = None
    if last_modified < today:
        stock_data = get_data_yahoo(ticker, start, end)
        stock_data.to_csv(stock_file)
    else:
        stock_data = read_csv(stock_file)
    return stock_data

class Stock:
    closes = None
    macd = None
    rsi = None
    signal_line = None


    def __init__(self, ticker, start, end):
        """
        Different sources for pulling data can be found here:
        https://readthedocs.org/projects/pandas-datareader/downloads/pdf/latest/
        """
        stock_data = get_stock_data(ticker, start, end)

        self.ticker = ticker
        self.closes = stock_data['Close'].tolist()
        self.closes_dt = DataFrame(self.closes)

        self.macd = calculate_macd(self.closes_dt).values.flatten().tolist()
        self.rsi = calculate_rsi(self.closes)
        self.signal_line = calculate_ema(self.closes_dt, 9).values.flatten().tolist()

    def sma(self, period):
        """
        Calculates the sma of the closes based on a period
        """
        return calculate_sma(self.closes, period)

    def is_currently_bullish(self):
        return self.macd[-1] > self.signal_line[-1]
