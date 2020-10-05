#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module in charge of managing the stock and its analystic values
"""
from pandas_datareader.data import get_data_yahoo
from pandas import DataFrame

from csv_manager import get_data
from macd import calculate_macd, calculate_macd_predictions, macd_trend
from rsi import calculate_rsi, calculate_rsi_predictions
from sma import calculate_sma

def get_stock_data(ticker):
    """
    Get stock data, catching an exception if there's a ConnectionError
    """
    stock_file = 'csvs/history/{}.csv'.format(ticker)
    return get_data(stock_file, get_data_yahoo, ticker)

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

    def __init__(self, ticker):
        """
        Different sources for pulling data can be found here:
        https://readthedocs.org/projects/pandas-datareader/downloads/pdf/latest/
        """
        stock_data = get_stock_data(ticker)

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
        try:
            return macd_trend(self.macd[-2], self.macd[-1], self.signal[-2], self.signal[-1])
        except IndexError:
            return False, False
