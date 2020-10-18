#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module with functions for the analysis and further display
of the tickers
"""
from requests.exceptions import ConnectionError

from pandas.core.common import flatten
from tabulate import tabulate

from stock import Stock
from utils import bought_status

all_data = []
overbought_data = []
oversold_data = []

def print_data(name, data):
    """
    Print in a certain format the data passed as an argument,
    alongside the associated name of the data
    """
    headers = flatten([
        'Stock', 'Price', 'RSI', 'Accuracy', 'MACD', 'Accuracy',
        'SMA9 vs SMA180'
    ])
    print(name)
    print()
    print(tabulate(data, headers=headers, numalign="right"))
    print()

def print_datas():
    """
    Print all the data in addition of those stocks that are
    overbought and oversold
    """
    by_name = lambda data_row: data_row[0]
    by_price = lambda data_row: data_row[1]

    all_data.sort(key=by_name)
    overbought_data.sort(key=by_price)
    oversold_data.sort(key=by_price)
    print_data('All data', all_data)
    print_data('Overbought stocks', overbought_data)
    print_data('Oversold stocks', oversold_data)

def format_accuracy(accuracy_value):
    """
    Formats a float accuracy value with percentage value In
    addition if the accuracy is more than 50% then it has a
    check. Else if is less than 50% then it should be added a
    cross.
    """
    accuracy = f'{accuracy_value:.0%}'
    accuracy += ' ✅' if accuracy_value > 0.5 else \
                ' ❌' if accuracy_value < 0.5 else ' ❔'
    return accuracy

def analyse_rsi(stock, data):
    """
    Performs analysis over the rsi of the stock and add the
    results in the analysis
    """
    current_rsi = f'{stock.rsi:.2f}'
    is_overbought, is_oversold = bought_status(stock.rsi)

    current_rsi += ' 🔥' if is_overbought else \
                   ' 🧊' if is_oversold else ' ❔'
    data.append(current_rsi)

    data.append(format_accuracy(stock.rsi_accuracy))

    return is_overbought, is_oversold

def format_trend(trend):
    """
    Formats trend to instead add special text to notice it easier
    @arg trend. A tuple with the format of (upwards, downwards)
    @return text. Text with the formatted text
    """
    upwards, downwards = trend
    return 'UP 🔥' if upwards else 'DW 🧊' if downwards else 'NE ❔'

def analyse_macd(stock, data):
    """
    Performs analysis over the macd of the stock and add the
    results in the analysis
    """
    data.append(format_trend(stock.macd_trend))
    data.append(format_accuracy(stock.macd_accuracy))

def analyse_sma(stock, data):
    """
    Analyses and adds text based if the sma indicator shows an
    upwards trend
    """
    data.append(format_trend(stock.sma_trend))

def analyse_ticker(ticker):
    """
    Performs reader for the corresponding ticker and checks
    if it's an actual rsi value for oversold or overbought
    """
    data = []

    stock = None
    try:
        stock = Stock(ticker)
        data.append(ticker.upper())
        data.append(float(f'{stock.closes:.2f}'))
        is_overbought, is_oversold = analyse_rsi(stock, data)
        analyse_macd(stock, data)
        analyse_sma(stock, data)
        if is_oversold:
            oversold_data.append(data)
        elif is_overbought:
            overbought_data.append(data)
        else:
            all_data.append(data)
    except ConnectionError as error:
        print(error, ticker)
    except IndexError as error:
        print(error, ticker)
