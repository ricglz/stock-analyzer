#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with only the function to calculate the ema
"""
from numpy import convolve, exp, linspace

def calculate_ema(values, period=50):
    """
    Exponential Moving Average. Periods are the time frame. For
    example, a period of 50 would be a 50 day moving average.
    Values are usually the stock closes but can be passed any
    values
    """

    weights = exp(linspace(-1., 0., period))
    weights /= weights.sum()
    ema = convolve(values, weights, mode='full')[:len(values)]
    ema[:period] = ema[period]
    return ema
