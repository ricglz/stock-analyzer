#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module in charge of managing the stock and its analystic values
"""
from datetime import date, timedelta
from os import stat

from pandas_datareader.data import get_data_yahoo
from pandas import DataFrame, read_csv

from csv_manager import get_data
from macd import calculate_macd, calculate_macd_predictions, macd_trend
from rsi import calculate_rsi, calculate_rsi_predictions
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
    """
    Class to manage the stock import values for decision making
    """
    closes = None
    macd = None
    macd_accuracy = None
    rsi = None
    rsi_accuracy = None
    signal = None

    def __init__(self, ticker, start, end):
        """
        Different sources for pulling data can be found here:
        https://readthedocs.org/projects/pandas-datareader/downloads/pdf/latest/
        """
        stock_file = 'csvs/history/{}.csv'.format(ticker)
        stock_data = get_data(stock_file, get_data_yahoo, ticker, start, end)

        self.closes = stock_data['Close'].tolist()
        self.closes_dt = DataFrame(self.closes)

        rsi_file = 'csvs/rsi/{}.csv'.format(ticker)
        self.rsi = get_data(rsi_file, calculate_rsi, self.closes)['rsi'].tolist()
        self.rsi_accuracy = calculate_rsi_predictions(self.closes, self.rsi)[0]

        self.macd, self.signal = calculate_macd(self.closes)
        self.macd_accuracy = calculate_macd_predictions(self.closes, self.macd, self.signal)[0]

    def sma(self, period):
        """
        Calculates the sma of the closes based on a period
        """
        return calculate_sma(self.closes, period)

    def macd_trend(self):
        """
        Calculates if the trend is bullish or not based on the
        macd value and the signal line
        """
        return macd_trend(self.macd[-2], self.macd[-1], self.signal[-2], self.signal[-1])
