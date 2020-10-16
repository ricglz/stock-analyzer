#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with only the function to calculate the macd
"""
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
