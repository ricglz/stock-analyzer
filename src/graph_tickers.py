#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv, exit
from thread import averages, run_ticker_thread

if __name__ == "__main__":
    if len(argv) < 2:
        exit('This command must have at least one argument')
    for ticker in argv[1:]:
        stock = run_ticker_thread(ticker)
        if stock is not None:
            stock.graph(averages)
