#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py
Module containing util general functions
"""
def bought_status(rsi):
    """
    Check if the rsi is overbought or oversold

    @arg rsi. Number containing the value of the rsi
    @return is_upwards, is_downwards
    """
    return rsi >= 66, rsi <=33

def macd_trend(macd, signal):
    """
    Checks if the current trend is is_upwards or downards

    @arg macd. List containing the macd values
    @arg signal. List containing the signal
    @return is_upwards, is_downward
    """
    is_upwards = signal[-2] > macd[-2] and signal[-1] <= macd[-1]
    is_downward = signal[-2] < macd[-2] and signal[-1] >= macd[-1]
    return is_upwards, is_downward

def sma_trend(fast_sma, slow_sma):
    is_bullish = fast_sma >= slow_sma * 1.01
    is_bearish = fast_sma <= slow_sma * 0.99
    return is_bullish, is_bearish

def divide(numerator, denominator):
    """
    Divide function to avoid errors by dividing over zero
    """
    return 0 if denominator == 0 else numerator / denominator

def chunks(lst, amount):
    """
    Returns chunks of lst containing an amount of elements of lst.
    """
    return [lst[i:i + amount] for i in range(0, len(lst), amount)]
