#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module with functions for the analysis and further display
of the tickers
"""
from datetime import date
from requests.exceptions import ConnectionError

from pandas.core.common import flatten
from tabulate import tabulate

from stock import Stock
from rsi import calculate_bought_status

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
    accuracy = "{:.0%}".format(accuracy_value)
    if accuracy_value > 0.5:
        accuracy += " ✅"
    elif accuracy_value < 0.5:
        accuracy += " ❌"
    return accuracy

def analyse_rsi(stock, data):
    """
    Performs analysis over the rsi of the stock and add the
    results in the analysis
    """
    current_rsi = "{:.2f}".format(stock.rsi)
    is_overbought, is_oversold = calculate_bought_status(stock.rsi)

    if is_overbought:
        current_rsi += " 🔥"
    elif is_oversold:
        current_rsi += " 🧊"
    data.append(current_rsi)

    data.append(format_accuracy(stock.rsi_accuracy))

    return is_overbought, is_oversold

def analyse_macd(stock, data):
    """
    Performs analysis over the macd of the stock and add the
    results in the analysis
    """
    current_macd = "{:.2f}".format(stock.macd[-1])
    upwards, downwards = stock.macd_trend()
    if upwards:
        current_macd += " 🔥"
    elif downwards:
        current_macd += " 🧊"
    data.append(current_macd)
    data.append(format_accuracy(stock.macd_accuracy))

def analyse_sma(stock, data):
    """
    Analyses and adds text based if the sma indicator shows an
    upwards trend
    """
    if stock.sma_is_trending():
        data.append(" 🔥")
    else:
        data.append(" 🧊")

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
        data.append(float("{:.2f}".format(stock.closes[-1])))
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
