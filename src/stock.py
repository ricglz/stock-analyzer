#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module in charge of managing the stock and its analystic values
"""
from os import makedirs, path
from pandas_datareader.data import get_data_yahoo
from stockstats import StockDataFrame

from csv_manager import get_data
from utils import macd_trend, sma_trend
from predictions import macd_predictions, rsi_predictions

StockDataFrame.MACD_EMA_SHORT = 12
StockDataFrame.MACD_EMA_LONG = 26

base_dir = path.join('csvs', 'history')

def organized_data_yahoo(ticker):
    """Organizes data of the yahoo information"""
    columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    try:
        return get_data_yahoo(ticker).reindex(columns=columns)
    except Exception as error:
        print(error, ticker)
        return None

def get_stock_data(ticker):
    """Gets stock data"""
    makedirs(base_dir, exist_ok=True)
    stock_file = path.join(base_dir, f'{ticker}.csv')
    return StockDataFrame.retype(get_data(stock_file, organized_data_yahoo, ticker))

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

        rsi_list = stock_data['rsi_20'].tolist()
        self.rsi = rsi_list[-1]
        self.rsi_accuracy = rsi_predictions(closes_list, rsi_list)[0]

        macd = stock_data['macd'].tolist()
        signal = stock_data['macds'].tolist()
        self.macd_accuracy = macd_predictions(closes_list, macd, signal)[0]
        self.macd_trend = macd_trend(macd, signal)

        sma_9 = stock_data['close_9_sma'].tolist()
        sma_180 = stock_data['close_180_sma'].tolist()
        self.sma_trend = sma_trend(sma_9[-1], sma_180[-1])
