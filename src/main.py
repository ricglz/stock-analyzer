#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from thread import TickerThread, allData, averages
from threading import Lock

from pandas.core.common import flatten
from tabulate import tabulate
import matplotlib

if __name__ == "__main__":
    matplotlib.rcParams.update({'font.size': 9})
    stocks = [line.rstrip() for line in open("stocks.txt", "r")]
    Lock()
    threads = []

    for ticker in stocks:
        thread = TickerThread(ticker)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(tabulate(allData, headers=flatten([
        'Stock', 'Price', [str(x) + " MA" for x in averages], "RSI", "chart"])))
