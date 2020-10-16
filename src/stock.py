#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module in charge of managing the stock and its analystic values
"""
from pandas_datareader.data import get_data_yahoo
from stockstats import StockDataFrame

from csv_manager import get_data
from utils import macd_trend
from predictions import macd_predictions, rsi_predictions

def get_stock_data(ticker):
    """Gets stock data"""
    stock_file = 'csvs/history/{}.csv'.format(ticker)
    return StockDataFrame.retype(get_data(stock_file, get_data_yahoo, ticker))

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
        closes_list = stock_data.close.tolist()
        self.closes = closes_list[-1]

        rsi_list = stock_data['rsi_6'].tolist()
        self.rsi = rsi_list[-1]
        self.rsi_accuracy = rsi_predictions(closes_list)

        macd = stock_data['macd'].tolist()
        signal = stock_data['macds'].tolist()
        self.macd_accuracy = macd_predictions(closes_list, macd, signal)
        self.macd_trend = macd_trend(macd, signal)
