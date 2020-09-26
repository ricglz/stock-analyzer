#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module with functions for the analysis and further display
of the tickers
"""

from datetime import datetime, timedelta
from pandas.core.common import flatten
from tabulate import tabulate

from stock import Stock

# Time frame you want to pull data from
end = datetime.now()
start = end - timedelta(days=365)

all_data = []
averages = [20, 200]
oversold_data = []
undersold_data = []


def print_data(name, data):
    headers = flatten([
        'Stock', 'Price', [str(x) + ' MA' for x in averages], 'RSI', 'chart'
    ])
    print(name)
    print()
    print(tabulate(data, headers=headers))
    print()


def print_datas():
    print_data('All data', all_data)
    print_data('Oversold stocks', oversold_data)
    print_data('Undersold stocks', undersold_data)



def rsi_analysis(stock, data):
    """
    Performs analysis over the rsi of the stock and add the
    results in the analysis
    """
    current_rsi = float("{:.2f}".format(stock.rsi[-1]))
    is_oversold = current_rsi > 70
    is_undersold = current_rsi < 30
    current_rsi = str(current_rsi)

    if is_oversold:
        current_rsi += " 🔥"
    elif is_undersold:
        current_rsi += " 🧊"
    data.append(current_rsi)
    return is_oversold, is_undersold


def analyse_ticker(ticker):
    """
    Performs reader for the corresponding ticker and checks
    if it's an actual rsi value for undersold or oversold
    """
    try:
        data = []

        print("Pulling data for " + ticker)

        stock = Stock(ticker, start, end)

        data.append(ticker.upper())

        data.append(stock.closes[-1])

        for average in averages:
            computed_sma = stock.sma(period=average)
            data.append(computed_sma[-1])

        is_oversold, is_undersold = rsi_analysis(stock, data)

        chart_link = "https://finance.yahoo.com/quote/{0}/chart?p={0}".format(ticker)

        data.append(chart_link)

        if is_undersold:
            undersold_data.append(data)
            return stock
        if is_oversold:
            oversold_data.append(data)
        else:
            all_data.append(data)
        return None

    except Exception as error:
        print('Error: ', str(error), ticker)
