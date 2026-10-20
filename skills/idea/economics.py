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
MAX_VALUE = 1e12


class InputError(ValueError):
    pass


def required_inputs(model):
    if not isinstance(model, str):
        raise InputError(f"model must be a string; expected one of: {', '.join(MODELS)}")
    if model not in MODELS:
        raise InputError(f"unknown model {model!r}; expected one of: {', '.join(MODELS)}")
    return MODELS[model] + COMMON


def is_number(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:  # an int too large for a float
        return False


def validate(spec):
    if not isinstance(spec, dict):
        raise InputError("the input must be a JSON object")
    names = required_inputs(spec.get("model"))
    inputs = spec.get("inputs", {})
    if not isinstance(inputs, dict):
        raise InputError("inputs must be an object")
    for name in inputs:
        if name not in names:
            raise InputError(f"unexpected input {name!r} for model {spec['model']!r}")
    for name in names:
        if name not in inputs:
            raise InputError(f"missing input {name!r}")
        if not isinstance(inputs[name], dict):
            raise InputError(f"{name!r} must be an object with pessimistic, base and optimistic values")
        for scenario in SCENARIOS:
            if scenario not in inputs[name]:
                raise InputError(f"{name!r} has no {scenario!r} value")
            value = inputs[name][scenario]
            if not is_number(value):
                raise InputError(f"{name!r} {scenario} must be a finite number")
            if value < 0:
                raise InputError(f"{name!r} {scenario} must not be negative")
            if value > MAX_VALUE:
                raise InputError(f"{name!r} {scenario} must be at most 1e12")
            if name in FRACTIONS and value > 1:
                raise InputError(f"{name!r} {scenario} must be between 0 and 1")
            if name in POSITIVE and value == 0:
                raise InputError(f"{name!r} {scenario} must be above 0")
    target = spec.get("target", 0)
    if not is_number(target) or target < 0:
        raise InputError("target must be a finite number, 0 or more")
    if target > MAX_VALUE:
        raise InputError("target must be at most 1e12")
    max_share = spec.get("max_share", DEFAULT_MAX_SHARE)
    if not is_number(max_share) or not 0 < max_share <= 1:
        raise InputError("max_share must be a finite number above 0 and at most 1")


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


def money(x):
    return f"{x:.2f}"


def ratio(x):
    return "n/a" if x is None else f"{x:.1f}"


def percent(x):
    return "n/a" if x is None else f"{x * 100:.2f}%"


def count(x):
    return "never" if x is None else str(x)


ROWS = (
    ("Revenue per customer / month", "revenue", money),
    ("Contribution / month", "contribution", money),
    ("Net contribution / month", "net_contribution", money),
    ("LTV", "ltv", lambda x: "unbounded" if x is None else money(x)),
    ("LTV / CAC", "ltv_cac", ratio),
    ("CAC payback (months)", "payback_months", lambda x: "never" if x is None else f"{x:.1f}"),
    ("Customers for break-even", "customers_break_even", count),
    ("Customers for the target", "customers_target", count),
    ("Market share for break-even", "share_break_even", percent),
    ("Market share for the target", "share_target", percent),
)


def render(r):
    lines = [
        f"Model: {r['model']} · Currency: {r['currency']} · Target: {money(r['target'])}/month"
        f" · Plausible share: up to {percent(r['max_share'])}",
        "",
        "| Output | Pessimistic | Base | Optimistic |",
        "| --- | --- | --- | --- |",
    ]
    for label, key, fmt in ROWS:
        cells = " | ".join(fmt(r["scenarios"][s][key]) for s in SCENARIOS)
        lines.append(f"| {label} | {cells} |")
    lines.append("")
    if r["sensitivity"]:
        lines += [
            "Sensitivity (each input at pessimistic, the rest at base; customers for the target):",
            "",
            "| Input | Customers | Change vs base |",
            "| --- | --- | --- |",
        ]
        for row in r["sensitivity"]:
            change = "never closes" if row["change"] is None else f"{row['change']:+d}"
            lines.append(f"| {row['input']} | {count(row['customers'])} | {change} |")
        lines += ["", f"Deciding variable: {r['deciding']}"]
    else:
        lines.append("Deciding variable: none (the base scenario never reaches the target)")
    lines.append(f"Result: {r['result']}")
    return "\n".join(lines)


def main(argv):
    if len(argv) != 2:
        print("usage: economics.py <inputs.json>", file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as f:
            spec = json.load(f)
        print(render(compute(spec)))
    except UnicodeDecodeError:
        print(f"economics.py: {argv[1]} is not UTF-8 text", file=sys.stderr)
        return 2
    except (RecursionError, OverflowError):
        print(f"economics.py: {argv[1]}: a value is too large or the JSON too deeply nested", file=sys.stderr)
        return 2
    except (OSError, json.JSONDecodeError, InputError) as e:
        print(f"economics.py: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
