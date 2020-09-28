#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with only the function to calculate the macd
"""
from numpy import array
from pandas import DataFrame

from ema import calculate_ema
from utils import calculate_predictions

def calculate_macd(prices, slow=26, fast=12):
    """
    Compute the MACD (Moving Average Convergence/Divergence)
    using a fast and slow exponential moving avg
    """

    prices_df = DataFrame(prices)
    fast_ewm = prices_df.ewm(span=fast).mean()
    slow_ewm = prices_df.ewm(span=slow).mean()
    macd = []
    counter = 0
    while counter < (len(fast_ewm)):
        macd.append(fast_ewm.iloc[counter, 0] - slow_ewm.iloc[counter, 0])
        counter += 1
    macd_df = DataFrame(macd)
    signal = macd_df.ewm(span=9).mean().values.tolist()
    return macd, signal

def macd_trend(prev_macd, macd, prev_signal, signal):
    """
    Checks if the current trend is upwards or downards
    """
    upwards = prev_signal > prev_macd and signal <= macd
    downwards = prev_signal < prev_macd and signal >= macd
    return upwards, downwards

def calculate_macd_predictions(prices, macd, signal):
    """
    Calculate the predictions to check how accurate is the macd
    value
    """
    day = 1
    days_observed = 0
    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0
    while day < len(macd) - 5:
        prev_day = day - 1
        avg_closing = array(prices[days_observed + 1: days_observed + 4]).mean()
        days_observed += 1
        upwards, downwards = macd_trend(macd[prev_day], macd[day], signal[prev_day], signal[day])
        if upwards:
            if prices[day] < avg_closing:
                true_positive += 1
            else:
                false_negative += 1

        if downwards:
            if prices[day] > avg_closing:
                true_negative += 1
            else:
                false_positive += 1
        day += 1
    return calculate_predictions(true_positive, false_positive, true_negative, false_negative)
