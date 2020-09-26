#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with only the function to calculate the rsi
"""
from numpy import diff, zeros_like

def calculate_rsi(prices, periods=4):
    """
    Based on the prices of a stock and an amount of periods,
    return the rsi of the stock
    """
    deltas = diff(prices)
    seed = deltas[:periods+1]
    up_prices = seed[seed >= 0].sum() / periods
    down_prices = -seed[seed < 0].sum() / periods
    relative_strength = up_prices/down_prices
    rsi = zeros_like(prices)
    rsi[:periods] = 100. - 100./(1.+relative_strength)

    for i in range(periods, len(prices)):
        delta = deltas[i-1]  # The diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up_prices = (up_prices*(periods-1) + upval)/periods
        down_prices = (down_prices*(periods-1) + downval)/periods

        relative_strength = up_prices/down_prices
        rsi[i] = 100. - 100./(1.+relative_strength)

    return rsi
