#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module with functions for the analysis and further display
of the tickers
"""

from datetime import date, timedelta
from pandas.core.common import flatten
from tabulate import tabulate

from stock import Stock
from rsi import calculate_bought_status

# Time frame you want to pull data from
end = date.today()
start = end - timedelta(days=365)

all_data = []
averages = [20, 200]
overbought_data = []
oversold_data = []

def print_data(name, data):
    """
    Print in a certain format the data passed as an argument,
    alongside the associated name of the data
    """
    headers = flatten(['Stock', 'Price', 'RSI', 'Accuracy', 'MACD', 'Accuracy'])
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
    accuracy = "{:.0%}".format(accuracy_value)
    if accuracy_value >= 0.50:
        accuracy += " ✅"
    else:
        accuracy += " ❌"
    return accuracy

def analyse_rsi(stock, data):
    """
    Performs analysis over the rsi of the stock and add the
    results in the analysis
    """
    current_rsi = "{:.2f}".format(stock.rsi[-1])
    is_overbought, is_oversold = calculate_bought_status(float(current_rsi))

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

def analyse_ticker(ticker):
    """
    Performs reader for the corresponding ticker and checks
    if it's an actual rsi value for oversold or overbought
    """
    try:
        data = []

        stock = Stock(ticker, start, end)
        data.append(ticker.upper())
        data.append(float("{:.2f}".format(stock.closes[-1])))
        is_overbought, is_oversold = analyse_rsi(stock, data)
        analyse_macd(stock, data)

        if is_oversold:
            oversold_data.append(data)
            return stock
        if is_overbought:
            overbought_data.append(data)
        else:
            all_data.append(data)
        return None

    except Exception as error:
        print('Error: ', str(error), ticker)
