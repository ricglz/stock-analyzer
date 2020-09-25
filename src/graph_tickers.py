#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Pool
from sys import argv, exit
from thread import averages, run_ticker_thread

def graph_stock(ticker):
    stock = run_ticker_thread(ticker)
    if stock is not None:
        stock.graph(averages)


if __name__ == "__main__":
    if len(argv) < 2:
        exit('This command must have at least one argument')
    Pool().map(graph_stock, argv[1:])
