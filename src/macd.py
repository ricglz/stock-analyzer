#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with only the function to calculate the macd
"""
from ema import calculate_ema

def calculate_macd(closes, slow=26, fast=12):
    """
    Compute the MACD (Moving Average Convergence/Divergence) using
    a fast and slow exponential moving avg
    """

    emaslow = calculate_ema(closes, slow)
    emafast = calculate_ema(closes, fast)
    return emafast - emaslow
