#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import random
import time
from urllib.request import urlopen

import matplotlib
import pandas_datareader.data as web
from pandas.core.common import flatten
from tabulate import tabulate

from stock import Stock

matplotlib.rcParams.update({'font.size': 9})

stocks = [line.rstrip() for line in open("stocks.txt", "r")]

# Time frame you want to pull data from
start = datetime.datetime.now()-datetime.timedelta(days=365)
end = datetime.datetime.now()

if __name__ == "__main__":

    # Array of moving averages you want to get
    MAarr = [20, 200]

    allData = []

    for ticker in stocks:

        try:
            stock_data = web.DataReader('{}.MX'.format(ticker), 'yahoo', start, end)
        except Exception as exception:
            continue
        try:
            data = []

            print("Pulling data for " + ticker)

            stock = Stock(ticker, start, end)

            # Append data to array
            data.append(ticker.upper())

            data.append(stock.closes[-1])

            for MA in MAarr:
                computedSMA = stock.SMA(period=MA)
                # print(computedSMA)
                data.append(computedSMA[-1])

            currentRsi = float("{:.2f}".format(stock.rsi[-1]))

            if currentRsi > 70:
                data.append(str(currentRsi) + " 🔥")
            elif currentRsi < 30:
                data.append(str(currentRsi) + " 🧊")
            else:
                data.append(currentRsi)

            chartLink = "https://finance.yahoo.com/quote/{}/chart?p={}".format(ticker, ticker)

            data.append(chartLink)

            allData.append(data)

            # Shows chart only if current RSI is greater than or less than 70 or 30 respectively
            if currentRsi < 30 or currentRsi > 70:

                stock.graph(MAarr)

        except Exception as e:
            print('Error: ', str(e))

    print(tabulate(allData, headers=flatten([
        'Stock', 'Price', [str(x) + " MA" for x in MAarr], "RSI", "chart"])))
