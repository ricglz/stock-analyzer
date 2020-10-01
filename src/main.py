#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
Module in charge of the main process
"""

from thread import TickerThread
from threading import Lock

from time import sleep

from analyse_ticker import print_datas
from utils import chunks

if __name__ == "__main__":
    stocks = [line.rstrip() for line in open('stocks.txt', 'r')]
    print('Analysing {} stock'.format(len(stocks)))
    Lock()
    threads = []

    for chunk in chunks(stocks, 40):
        for ticker in chunk:
            thread = TickerThread(ticker)
            thread.start()
            threads.append(thread)
        sleep(0.5)

    for thread in threads:
        thread.join()

    print_datas()
