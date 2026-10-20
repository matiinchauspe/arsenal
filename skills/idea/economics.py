#!/usr/bin/env python3
"""Unit economics for an idea's map: three scenarios, a sensitivity pass and a result.

Usage: python3 economics.py <inputs.json>
The input format is in ECONOMICS-FORMAT.md. Standard library only.
"""
import json
import math
import sys

SCENARIOS = ("pessimistic", "base", "optimistic")
COMMON = ("gross_margin", "cac", "monthly_churn", "fixed_costs", "reachable_market")
MODELS = {
    "subscription": ("price",),
    "transactional": ("volume", "take_rate"),
    "one-time": ("price", "months_between_purchases"),
    "ads": ("ad_arpu",),
}
FRACTIONS = ("gross_margin", "monthly_churn", "take_rate")
POSITIVE = ("months_between_purchases",)
DEFAULT_MAX_SHARE = 0.10


class InputError(ValueError):
    pass


def required_inputs(model):
    if model not in MODELS:
        raise InputError(f"unknown model {model!r}; expected one of: {', '.join(MODELS)}")
    return MODELS[model] + COMMON


def validate(spec):
    names = required_inputs(spec.get("model"))
    inputs = spec.get("inputs", {})
    for name in inputs:
        if name not in names:
            raise InputError(f"unexpected input {name!r} for model {spec['model']!r}")
    for name in names:
        if name not in inputs:
            raise InputError(f"missing input {name!r}")
        for scenario in SCENARIOS:
            if scenario not in inputs[name]:
                raise InputError(f"{name!r} has no {scenario!r} value")
            value = inputs[name][scenario]
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise InputError(f"{name!r} {scenario} must be a number")
            if value < 0:
                raise InputError(f"{name!r} {scenario} must not be negative")
            if name in FRACTIONS and value > 1:
                raise InputError(f"{name!r} {scenario} must be between 0 and 1")
            if name in POSITIVE and value == 0:
                raise InputError(f"{name!r} {scenario} must be above 0")
    target = spec.get("target", 0)
    if not isinstance(target, (int, float)) or target < 0:
        raise InputError("target must be a number, 0 or more")
    max_share = spec.get("max_share", DEFAULT_MAX_SHARE)
    if not isinstance(max_share, (int, float)) or not 0 < max_share <= 1:
        raise InputError("max_share must be above 0 and at most 1")


def revenue_per_customer(model, v):
    if model == "subscription":
        return v["price"]
    if model == "transactional":
        return v["volume"] * v["take_rate"]
    if model == "one-time":
        return v["price"] / v["months_between_purchases"]
    return v["ad_arpu"]
