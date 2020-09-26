#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
from datetime import datetime, timedelta

from stock import Stock

# Time frame you want to pull data from
end = datetime.now()
start = end - timedelta(days=365)

all_data = []
averages = [20, 200]
oversold_data = []
undersold_data = []

class TickerThread(Thread):
    """Thread for checking the ticker data in parallel"""
    def __init__(self, ticker):
        Thread.__init__(self)
        self.ticker = ticker

    def run(self):
        run_ticker_thread(self.ticker)


def rsi_analysis(stock, data):
    current_rsi = float("{:.2f}".format(stock.rsi[-1]))
    is_oversold = current_rsi > 66
    is_undersold = current_rsi < 33

    if is_oversold:
        data.append(str(current_rsi) + " 🔥")
    elif is_undersold:
        data.append(str(current_rsi) + " 🧊")
    else:
        data.append(current_rsi)
    return is_oversold, is_undersold


def run_ticker_thread(ticker):
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
