#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with only the function to calculate the ema
"""

def calculate_ema(values, period=50):
    """
    Exponential Moving Average. Periods are the time frame. For
    example, a period of 50 would be a 50 day moving average.
    Values are usually the stock closes but can be passed any
    values
    """

    return values.ewm(span=period).mean()
