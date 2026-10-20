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


def customers_for(amount, net_contribution):
    """Customers needed to earn `amount` a month; None when no number of customers does."""
    if net_contribution <= 0:
        return None
    return math.ceil(round(amount / net_contribution, 9))


def share(customers, market):
    if customers is None or market <= 0:
        return None
    return customers / market


def metrics(model, v, target):
    revenue = revenue_per_customer(model, v)
    contribution = revenue * v["gross_margin"]
    net = contribution - v["monthly_churn"] * v["cac"]
    ltv = contribution / v["monthly_churn"] if v["monthly_churn"] > 0 else None
    m = {
        "revenue": revenue,
        "contribution": contribution,
        "net_contribution": net,
        "ltv": ltv,
        "ltv_cac": ltv / v["cac"] if ltv is not None and v["cac"] > 0 else None,
        "payback_months": v["cac"] / contribution if contribution > 0 else None,
        "customers_break_even": customers_for(v["fixed_costs"], net),
        "customers_target": customers_for(v["fixed_costs"] + target, net),
    }
    m["share_break_even"] = share(m["customers_break_even"], v["reachable_market"])
    m["share_target"] = share(m["customers_target"], v["reachable_market"])
    return m


def scenario_values(spec, scenario):
    return {name: r[scenario] for name, r in spec["inputs"].items()}


def closes(m, max_share):
    return m["share_target"] is not None and m["share_target"] <= max_share


def sensitivity(spec, base):
    """Each input except the market at pessimistic, the rest at base, ranked by customers added.

    An input that leaves no number of customers enough ranks first, with no customers and no change.
    """
    if base["customers_target"] is None:
        return []
    rows = []
    for name in spec["inputs"]:
        if name == "reachable_market":
            continue
        v = scenario_values(spec, "base")
        v[name] = spec["inputs"][name]["pessimistic"]
        customers = metrics(spec["model"], v, spec.get("target", 0))["customers_target"]
        change = None if customers is None else customers - base["customers_target"]
        rows.append({"input": name, "customers": customers, "change": change})
    return sorted(rows, key=lambda row: math.inf if row["change"] is None else row["change"], reverse=True)


def compute(spec):
    validate(spec)
    target = spec.get("target", 0)
    max_share = spec.get("max_share", DEFAULT_MAX_SHARE)
    scenarios = {s: metrics(spec["model"], scenario_values(spec, s), target) for s in SCENARIOS}
    ranking = sensitivity(spec, scenarios["base"])
    deciding = ranking[0]["input"] if ranking else None
    if not closes(scenarios["base"], max_share):
        result = "doesn't close"
    elif closes(scenarios["pessimistic"], max_share):
        result = "closes comfortably"
    else:
        result = f"closes, but hinges on {deciding}"
    return {
        "model": spec["model"],
        "currency": spec.get("currency", ""),
        "target": target,
        "max_share": max_share,
        "scenarios": scenarios,
        "sensitivity": ranking,
        "deciding": deciding,
        "result": result,
    }
