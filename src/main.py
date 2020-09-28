#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from thread import TickerThread
from threading import Lock
from analyse_ticker import print_datas

if __name__ == "__main__":
    stocks = [line.rstrip() for line in open('stocks.txt', 'r')]
    Lock()
    threads = []

    for ticker in stocks:
        thread = TickerThread(ticker)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print_datas()
