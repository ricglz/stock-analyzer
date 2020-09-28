#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with only the function to calculate the rsi
"""
from numpy import array, diff, zeros_like
from pandas import DataFrame

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

def divide(numerator, denominator):
    """
    Divide function to avoid errors by dividing over zero
    """
    return 0 if denominator == 0 else numerator / denominator

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
    sensitivity = 0
    specificity = 0
    accuracy = 0
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
    sensitivity_denominator = true_positive + false_negative
    specificity_denominator = true_negative + false_positive
    sensitivity = divide(true_positive, sensitivity_denominator)
    specificity = divide(true_negative, specificity_denominator)
    accuracy = divide(
        true_positive + true_negative,
        sensitivity_denominator + specificity_denominator
    )
    tpr = sensitivity  # Calculate the true positive rate
    fpr = 1 - specificity  # Calculate the false positive rate
    return accuracy, tpr, fpr
