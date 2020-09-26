#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with only the function to calculate the sma
"""
from numpy import convolve, repeat

def calculate_sma(values, period=50):
    """
    Simple Moving Average. Periods are the time frame. For
    example, a period of 50 would be a 50 day moving average.
    Values are usually the stock closes but can be passed
    any values

    Returns numpy array
    """

    weigths = repeat(1.0, period)/period
    smas = convolve(values, weigths, 'valid')
    return smas
