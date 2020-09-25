#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from thread import TickerThread, all_data, averages, oversold_data, undersold_data
from threading import Lock

from pandas.core.common import flatten
from tabulate import tabulate
import matplotlib

def print_data(name, data):
    print(name)
    print()
    print(tabulate(data, headers=flatten([
        'Stock', 'Price', [str(x) + " MA" for x in averages], "RSI", "chart"])))
    print()


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

    print_data('All data', all_data)
    print_data('Oversold stocks', oversold_data)
    print_data('Undersold stocks', undersold_data)
