#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module that will calculate the accuracy of the indicator of the
stock
"""

from numpy import array

from utils import bought_status, divide, macd_trend

def calculate_predictions(true_positive, false_positive, true_negative, false_negative):
    """
    Calculate predictions based on the number of true/false positive/negative's
    """
    sens_denom = true_positive + false_negative
    spec_denom = true_negative + false_positive
    sensitivity = divide(true_positive, sens_denom)
    specificity = divide(true_negative, spec_denom)
    accuracy = divide(true_positive + true_negative, sens_denom + spec_denom)
    tpr = sensitivity  # Calculate the true positive rate
    fpr = 1 - specificity  # Calculate the false positive rate
    return accuracy, tpr, fpr

def macd_predictions(prices, macd, signal):
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
        avg_closing = array(prices[days_observed + 1: days_observed + 4]).mean()
        days_observed += 1
        upwards, downwards = macd_trend(macd, signal)
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

def rsi_predictions(prices, rsi):
    """
    Calculate prediction metrics of the rsi
    """
    days_observed = 14
    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0
    try:
        while days_observed < len(prices) - 5:
            change = array(prices[days_observed + 1: days_observed + 6]).mean()
            is_overbought, is_oversold = bought_status(rsi[days_observed])
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
    except IndexError as error:
        print(error, len(rsi), len(prices))
        return 0.5, 0.5, 0.5
