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
    """Gets stock data"""
    stock_file = 'csvs/history/{}.csv'.format(ticker)
    return get_data(stock_file, get_data_yahoo, ticker)

def get_rsi_data(ticker, closes):
    """
    Gets the data of the rsi being by calculating it or using
    the storage data. And later on return the current rsi value
    and the accuracy of the indicator for the stock
    """
    rsi_file = 'csvs/rsi/{}.csv'.format(ticker)
    rsi = get_data(rsi_file, calculate_rsi, closes)['rsi'].tolist()
    return [rsi[-1], calculate_rsi_predictions(closes, rsi)[0]]

class Stock:
    """
    Class for representing the stock and its technical indicators
    based on the close values of the last 5 years.
    """
    def __init__(self, ticker):
        """
        Different sources for pulling data can be found here:
        https://readthedocs.org/projects/pandas-datareader/downloads/pdf/latest/
        """
        stock_data = get_stock_data(ticker)

        self.closes = stock_data['Close'].tolist()
        self.closes_dt = DataFrame(self.closes)

        self.rsi, self.rsi_accuracy = get_rsi_data(ticker, self.closes)

        macd, signal = calculate_macd(self.closes)
        self.macd_accuracy = calculate_macd_predictions(self.closes, macd, signal)[0]
        if len(macd) < 2 or len(signal) < 2:
            self.macd_trend = [False, False]
        else:
            self.macd_trend = macd_trend(macd[-2], macd[-1], signal[-2], signal[-1])

        sma_9 = calculate_sma(self.closes, 9)
        sma_180 = calculate_sma(self.closes, 180)
        self.sma_is_trending = sma_9[-1] > sma_180[-1]
