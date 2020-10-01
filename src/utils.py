#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py
Module containing util general functions
"""

def divide(numerator, denominator):
    """
    Divide function to avoid errors by dividing over zero
    """
    return 0 if denominator == 0 else numerator / denominator

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

def chunks(lst, amount):
    """
    Returns chunks of lst containing an amount of elements of lst.
    """
    return [lst[i:i + amount] for i in range(0, len(lst), amount)]
