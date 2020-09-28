#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module with only the function to calculate the rsi
"""

from numpy import array, diff, zeros_like
from pandas import DataFrame

from utils import calculate_predictions

def calculate_rsi(prices, periods=14):
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

    return DataFrame(rsi, columns=['rsi'])

def calculate_bought_status(rsi):
    """
    Calculate if based on the rsi, the stock is overbought or
    oversold
    """
    is_overbought = rsi >= 66
    is_oversold = rsi <= 33
    return is_overbought, is_oversold

def calculate_rsi_predictions(prices, rsi):
    """
    Calculate prediction metrics of the rsi
    """
    days_observed = 14
    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0
    while days_observed < len(prices)-5:
        change = array(prices[days_observed + 1: days_observed + 6]).mean()
        is_overbought, is_oversold = calculate_bought_status(rsi[days_observed])
        if is_oversold:
            if change > prices[days_observed]:
                true_positive += 1
            else:
                false_negative += 1
        elif is_overbought:
            if change <= prices[days_observed]:
                true_negative += 1
            else:
                false_positive += 1
        days_observed += 1
    return calculate_predictions(true_positive, false_positive, true_negative, false_negative)
