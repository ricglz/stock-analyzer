#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with only the function to calculate the sma
"""
from numpy import convolve, repeat

def calculate_sma(values, period):
    """
    Simple Moving Average. Period is the timeframe to calculate
    the average

    Returns numpy array
    """

    weigths = repeat(1.0, period)/period
    smas = convolve(values, weigths, 'valid')
    return smas
