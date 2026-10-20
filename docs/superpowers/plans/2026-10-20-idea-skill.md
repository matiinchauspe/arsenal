# `idea` Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `idea` skill to arsenal: it walks a product or startup idea as a map of falsifiable assumptions, researches each one by trying to refute it, runs ranged unit economics through a deterministic script, and issues a dated verdict the user decides on.

**Architecture:** A markdown skill (`skills/idea/`) split like `interview`: `SKILL.md` holds locating, intents, Generate, New and Continue; one format file per artifact (`MAP-FORMAT.md`, `ECONOMICS-FORMAT.md`, `TEST-FORMAT.md`) and `LIFECYCLE.md` for verdict and outcome. Market facts live in `research` topics and are linked; the map's view is drawn by `diagram`. All money arithmetic comes from `skills/idea/economics.py`, a stdlib-only Python script tested with `unittest` from `tests/idea/`.

**Tech Stack:** Markdown (Agent Skills `SKILL.md` format), Python 3 standard library (`json`, `math`, `sys`, `unittest`, `subprocess`), Mermaid through the existing `diagram` skill.

**Spec:** `docs/superpowers/specs/2026-10-20-idea-design.md`

**Repo rules for whoever executes this:**
- Never add `Co-Authored-By` or any AI attribution to commits. Conventional commits only.
- Use `bat`/`rg`/`fd`/`sd`/`eza`, never `cat`/`grep`/`find`/`sed`/`ls`.
- Do not run any build. The only commands are the test runs and `claude plugin validate .` written below.

---

## File structure

| Path | Responsibility |
| --- | --- |
| `skills/idea/economics.py` | Pure calculator: validates an inputs JSON, computes three scenarios, sensitivity and the economics result, renders markdown. CLI `python3 economics.py <inputs.json>` |
| `tests/idea/test_economics.py` | `unittest` suite for `economics.py`, every expected number checked by hand in this plan |
| `skills/idea/SKILL.md` | Frontmatter, locating the idea, intents, where things are written, List, Generate, New, Continue, language, never |
| `skills/idea/MAP-FORMAT.md` | `MAP.md`, `STATUS.md` and `IDEAS.md` templates; zones, IDs, impact, states and transitions, evidence links, competitor table, the view |
| `skills/idea/ECONOMICS-FORMAT.md` | Revenue models, inputs, the JSON contract, formulas, plausibility, running the script, writing a run into `MAP.md`, the result |
| `skills/idea/TEST-FORMAT.md` | Test kinds, interview rules, the test block, Test and Result intents |
| `skills/idea/LIFECYCLE.md` | Verdict (rules, template, what this idea demands), Outcome, stale verdicts |
| `README.md` | New table row and a "where your ideas live" section |
| `CHANGELOG.md` | `0.6.0` entry |
| `.claude-plugin/plugin.json` | Version `0.6.0` |

### Refinements over the spec, fixed here

These came out of turning the spec into code; Task 1 writes them back into the spec so both agree:

1. **Customers needed** use the **net contribution**: `contribution − monthly_churn × CAC`. Keeping a customer base steady means replacing who churns, and that costs CAC every month. Ignoring it overstates every business.
2. **One-time sale** revenue per customer per month is `price ÷ months_between_purchases`; `monthly_churn` is the monthly share of buyers who never buy again. **Ads** revenue per customer is `ad_arpu` (monthly ad revenue per user): a "customer" is a user.
3. **Sensitivity** ranks every input except `reachable_market`, which never changes customers needed; the market is checked through the share instead.
4. **Plausible share** defaults to 10% of the reachable market (`max_share` in the JSON), a rule of thumb the user may change. A scenario **closes** when its net contribution is positive and its share for the target is at most `max_share`.
5. **The view** is one overview with one node per zone (7 nodes), colored by the zone's riskiest assumption, so it stays within `diagram`'s 12-15 node limit.
6. **Economics assumptions wait** for the assumptions their inputs come from (price from Competition, CAC from Channel, reachable market from Market) to be researched.
7. A critical `researched (against)` counts like `mixed` in the verdict rules, and is named first among the assumptions to test and as the best reason not to do it.

---

### Task 1: Sync the spec with the refinements

**Files:**
- Modify: `docs/superpowers/specs/2026-10-20-idea-design.md`

- [ ] **Step 1: Replace the revenue model table**

Replace:

```md
| Subscription | price |
| Transactional (marketplace, commission) | volume × take rate |
| One-time sale | price × repurchase rate ÷ months between purchases |
| Ads / audience | users × ad ARPU |
```

with:

```md
| Subscription | price |
| Transactional (marketplace, commission) | volume × take rate |
| One-time sale | price ÷ months between purchases (churn: the monthly share of buyers who never buy again) |
| Ads / audience | ad ARPU per user (a customer is a user) |
```

- [ ] **Step 2: Replace the outputs list**

Replace the block that starts with `- **LTV** = monthly revenue per customer` and ends with `in the Economics zone if it is not one already.` with:

```md
- **Contribution** = monthly revenue per customer × gross margin
- **Net contribution** = contribution − monthly churn × CAC (what a customer leaves once replacing churned customers is paid for)
- **LTV** = contribution ÷ monthly churn
- **LTV / CAC** (below 3 is a warning; below 1 every customer loses money)
- **CAC payback** = CAC ÷ contribution, in months
- **Customers needed** = (fixed costs + target) ÷ net contribution, rounded up; for break-even, the target is 0
- **Market share needed** = customers needed ÷ reachable market: the reality check. Plausible up to
  `max_share`, 10% by default, a rule of thumb the user may change.
- **Sensitivity:** each input except the reachable market moved to its pessimistic value alone, the
  rest at base; the input that moves customers-needed-for-the-target the most is **the deciding
  variable**, and becomes a `critical` assumption in the Economics zone if it is not one already.
```

- [ ] **Step 3: Replace the economics result list**

Replace the three bullets under `### Economics result` with:

```md
A scenario **closes** when its net contribution is positive and its market share needed for the
target is at most `max_share`.

- **Doesn't close:** the base scenario does not close.
- **Closes, but hinges on X:** base closes, pessimistic does not; X is the deciding variable.
- **Closes comfortably:** even pessimistic closes. Rare; the inputs get a second look.
```

- [ ] **Step 4: Replace the view paragraph**

Replace the paragraph under `### The view` with:

```md
`diagram` draws one overview: one node per zone (7 nodes), labeled with its counts by state and
colored by its riskiest assumption (`dead` > `researched (against)` > `unknown` >
`researched (mixed)` > `in-test` > `researched (for)` > `validated`). It lives in `MAP.md` and is
redrawn when a state changes.
```

- [ ] **Step 5: Add the two Continue and verdict rules**

After the line `3. Set the assumption's state from the facts, link them, redraw the view, log it.` add:

```md

An Economics assumption waits until the assumptions its inputs come from (price from Competition,
CAC from Channel, reachable market from Market) are researched.
```

After the line `Rules are checked top to bottom; the first that matches is the verdict.` add:

```md
A critical `researched (against)` counts as `mixed` in these rules, and is named first among the
assumptions to test and as the best reason not to do it.
```

- [ ] **Step 6: Commit**

```bash
git add docs/superpowers/specs/2026-10-20-idea-design.md
git commit -m "docs: refine the idea skill economics, view and verdict rules"
```

---

### Task 2: `economics.py`: revenue per customer and validation

**Files:**
- Create: `skills/idea/economics.py`
- Test: `tests/idea/test_economics.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/idea/test_economics.py`:

```python
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest

SKILL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "skills", "idea")
sys.path.insert(0, SKILL_DIR)

import economics  # noqa: E402

SCRIPT = os.path.join(SKILL_DIR, "economics.py")


def rng(pessimistic, base, optimistic):
    return {"pessimistic": pessimistic, "base": base, "optimistic": optimistic}


SUBSCRIPTION = {
    "model": "subscription",
    "currency": "USD",
    "target": 1000,
    "inputs": {
        "price": rng(15, 20, 25),
        "gross_margin": rng(0.7, 0.8, 0.85),
        "cac": rng(60, 40, 30),
        "monthly_churn": rng(0.08, 0.05, 0.03),
        "fixed_costs": rng(800, 500, 400),
        "reachable_market": rng(5000, 10000, 15000),
    },
}


def spec(**changes):
    s = copy.deepcopy(SUBSCRIPTION)
    for name, value in changes.items():
        s["inputs"][name] = value
    return s


class RevenuePerCustomer(unittest.TestCase):
    def test_subscription_is_the_price(self):
        self.assertEqual(economics.revenue_per_customer("subscription", {"price": 20}), 20)

    def test_transactional_is_volume_times_take_rate(self):
        v = {"volume": 1000, "take_rate": 0.05}
        self.assertAlmostEqual(economics.revenue_per_customer("transactional", v), 50)

    def test_one_time_spreads_the_price_over_the_months_between_purchases(self):
        v = {"price": 120, "months_between_purchases": 12}
        self.assertAlmostEqual(economics.revenue_per_customer("one-time", v), 10)

    def test_ads_is_the_ad_arpu(self):
        self.assertAlmostEqual(economics.revenue_per_customer("ads", {"ad_arpu": 0.4}), 0.4)


class Validation(unittest.TestCase):
    def test_unknown_model(self):
        s = copy.deepcopy(SUBSCRIPTION)
        s["model"] = "freemium"
        with self.assertRaisesRegex(economics.InputError, "unknown model 'freemium'"):
            economics.validate(s)

    def test_missing_input(self):
        s = copy.deepcopy(SUBSCRIPTION)
        del s["inputs"]["cac"]
        with self.assertRaisesRegex(economics.InputError, "missing input 'cac'"):
            economics.validate(s)

    def test_unexpected_input(self):
        s = spec(prices=rng(1, 2, 3))
        with self.assertRaisesRegex(economics.InputError, "unexpected input 'prices'"):
            economics.validate(s)

    def test_missing_scenario(self):
        s = spec(price={"pessimistic": 15, "base": 20})
        with self.assertRaisesRegex(economics.InputError, "'price' has no 'optimistic' value"):
            economics.validate(s)

    def test_fraction_out_of_range(self):
        s = spec(monthly_churn=rng(1.5, 0.05, 0.03))
        with self.assertRaisesRegex(economics.InputError, "'monthly_churn' pessimistic must be between 0 and 1"):
            economics.validate(s)

    def test_negative_value(self):
        s = spec(cac=rng(-1, 40, 30))
        with self.assertRaisesRegex(economics.InputError, "'cac' pessimistic must not be negative"):
            economics.validate(s)

    def test_months_between_purchases_must_be_positive(self):
        s = {
            "model": "one-time",
            "inputs": {
                "price": rng(100, 120, 150),
                "months_between_purchases": rng(0, 12, 6),
                "gross_margin": rng(0.7, 0.8, 0.9),
                "cac": rng(30, 20, 10),
                "monthly_churn": rng(0.1, 0.05, 0.02),
                "fixed_costs": rng(300, 200, 100),
                "reachable_market": rng(1000, 2000, 3000),
            },
        }
        with self.assertRaisesRegex(economics.InputError, "'months_between_purchases' pessimistic must be above 0"):
            economics.validate(s)

    def test_valid_spec_passes(self):
        economics.validate(copy.deepcopy(SUBSCRIPTION))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests/idea -v`
Expected: ERROR, `ModuleNotFoundError: No module named 'economics'`

- [ ] **Step 3: Write the minimal implementation**

Create `skills/idea/economics.py`:

```python
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests/idea -v`
Expected: `Ran 12 tests` … `OK`

- [ ] **Step 5: Commit**

```bash
git add skills/idea/economics.py tests/idea/test_economics.py
git commit -m "feat(idea): validate economics inputs and compute revenue per customer"
```

---

### Task 3: `economics.py`: scenario metrics

Hand-checked numbers for `SUBSCRIPTION`, target 1000:

| Output | Pessimistic | Base | Optimistic |
| --- | --- | --- | --- |
| Revenue | 15 | 20 | 25 |
| Contribution | 15 × 0.7 = 10.5 | 20 × 0.8 = 16 | 25 × 0.85 = 21.25 |
| Net contribution | 10.5 − 0.08 × 60 = 5.7 | 16 − 0.05 × 40 = 14 | 21.25 − 0.03 × 30 = 20.35 |
| LTV | 10.5 ÷ 0.08 = 131.25 | 16 ÷ 0.05 = 320 | 21.25 ÷ 0.03 = 708.33 |
| LTV / CAC | 131.25 ÷ 60 = 2.1875 | 320 ÷ 40 = 8 | 708.33 ÷ 30 = 23.61 |
| Payback (months) | 60 ÷ 10.5 = 5.714 | 40 ÷ 16 = 2.5 | 30 ÷ 21.25 = 1.412 |
| Customers, break-even | ⌈800 ÷ 5.7⌉ = ⌈140.35⌉ = 141 | ⌈500 ÷ 14⌉ = ⌈35.71⌉ = 36 | ⌈400 ÷ 20.35⌉ = ⌈19.66⌉ = 20 |
| Customers, target | ⌈1800 ÷ 5.7⌉ = ⌈315.79⌉ = 316 | ⌈1500 ÷ 14⌉ = ⌈107.14⌉ = 108 | ⌈1400 ÷ 20.35⌉ = ⌈68.80⌉ = 69 |
| Share, target | 316 ÷ 5000 = 6.32% | 108 ÷ 10000 = 1.08% | 69 ÷ 15000 = 0.46% |

**Files:**
- Modify: `skills/idea/economics.py`
- Test: `tests/idea/test_economics.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/idea/test_economics.py`, above `if __name__ == "__main__":`:

```python
def values(s, scenario):
    return {name: r[scenario] for name, r in s["inputs"].items()}


class Metrics(unittest.TestCase):
    def test_base_scenario(self):
        m = economics.metrics("subscription", values(SUBSCRIPTION, "base"), 1000)
        self.assertAlmostEqual(m["revenue"], 20)
        self.assertAlmostEqual(m["contribution"], 16)
        self.assertAlmostEqual(m["net_contribution"], 14)
        self.assertAlmostEqual(m["ltv"], 320)
        self.assertAlmostEqual(m["ltv_cac"], 8)
        self.assertAlmostEqual(m["payback_months"], 2.5)
        self.assertEqual(m["customers_break_even"], 36)
        self.assertEqual(m["customers_target"], 108)
        self.assertAlmostEqual(m["share_target"], 0.0108)

    def test_pessimistic_scenario(self):
        m = economics.metrics("subscription", values(SUBSCRIPTION, "pessimistic"), 1000)
        self.assertAlmostEqual(m["net_contribution"], 5.7)
        self.assertAlmostEqual(m["ltv"], 131.25)
        self.assertAlmostEqual(m["ltv_cac"], 2.1875)
        self.assertEqual(m["customers_break_even"], 141)
        self.assertEqual(m["customers_target"], 316)
        self.assertAlmostEqual(m["share_target"], 0.0632)

    def test_optimistic_scenario(self):
        m = economics.metrics("subscription", values(SUBSCRIPTION, "optimistic"), 1000)
        self.assertEqual(m["customers_break_even"], 20)
        self.assertEqual(m["customers_target"], 69)

    def test_no_target_means_break_even(self):
        m = economics.metrics("subscription", values(SUBSCRIPTION, "base"), 0)
        self.assertEqual(m["customers_target"], 36)

    def test_negative_net_contribution_never_reaches_customers(self):
        v = values(SUBSCRIPTION, "base")
        v["cac"] = 400  # 16 - 0.05 * 400 = -4
        m = economics.metrics("subscription", v, 1000)
        self.assertAlmostEqual(m["net_contribution"], -4)
        self.assertIsNone(m["customers_break_even"])
        self.assertIsNone(m["customers_target"])
        self.assertIsNone(m["share_target"])

    def test_zero_churn_has_unbounded_ltv(self):
        v = values(SUBSCRIPTION, "base")
        v["monthly_churn"] = 0
        self.assertIsNone(economics.metrics("subscription", v, 1000)["ltv"])

    def test_zero_cac_has_no_ltv_cac(self):
        v = values(SUBSCRIPTION, "base")
        v["cac"] = 0
        self.assertIsNone(economics.metrics("subscription", v, 1000)["ltv_cac"])

    def test_zero_margin_never_pays_back(self):
        v = values(SUBSCRIPTION, "base")
        v["gross_margin"] = 0
        self.assertIsNone(economics.metrics("subscription", v, 1000)["payback_months"])
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests/idea -v`
Expected: 8 ERRORs, `AttributeError: module 'economics' has no attribute 'metrics'`

- [ ] **Step 3: Write the minimal implementation**

Add to `skills/idea/economics.py`, after `revenue_per_customer`:

```python
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests/idea -v`
Expected: `Ran 20 tests` … `OK`

- [ ] **Step 5: Commit**

```bash
git add skills/idea/economics.py tests/idea/test_economics.py
git commit -m "feat(idea): compute the scenario metrics"
```

---

### Task 4: `economics.py`: sensitivity and result

Hand-checked sensitivity for `SUBSCRIPTION` (each input at pessimistic, the rest at base; base customers for the target = 108; target amount = fixed costs + 1000):

| Input at pessimistic | Net contribution | Customers | Change |
| --- | --- | --- | --- |
| price 15 | 15 × 0.8 − 2 = 10 | ⌈1500 ÷ 10⌉ = 150 | +42 |
| fixed_costs 800 | 14 | ⌈1800 ÷ 14⌉ = ⌈128.57⌉ = 129 | +21 |
| gross_margin 0.7 | 20 × 0.7 − 2 = 12 | ⌈1500 ÷ 12⌉ = 125 | +17 |
| monthly_churn 0.08 | 16 − 3.2 = 12.8 | ⌈1500 ÷ 12.8⌉ = ⌈117.19⌉ = 118 | +10 |
| cac 60 | 16 − 3 = 13 | ⌈1500 ÷ 13⌉ = ⌈115.38⌉ = 116 | +8 |

Deciding variable: `price`. Pessimistic share 6.32% ≤ 10%, so the result is **closes comfortably**. With `reachable_market` pessimistic at 2000, the pessimistic share is 316 ÷ 2000 = 15.8% > 10%: **closes, but hinges on price**. With base `cac` 400, the base net contribution is −4: **doesn't close**.

**Files:**
- Modify: `skills/idea/economics.py`
- Test: `tests/idea/test_economics.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/idea/test_economics.py`, above `if __name__ == "__main__":`:

```python
class Compute(unittest.TestCase):
    def test_sensitivity_ranks_inputs_by_how_much_they_move_customers(self):
        r = economics.compute(copy.deepcopy(SUBSCRIPTION))
        ranking = [(row["input"], row["customers"], row["change"]) for row in r["sensitivity"]]
        self.assertEqual(ranking, [
            ("price", 150, 42),
            ("fixed_costs", 129, 21),
            ("gross_margin", 125, 17),
            ("monthly_churn", 118, 10),
            ("cac", 116, 8),
        ])
        self.assertEqual(r["deciding"], "price")

    def test_closes_comfortably_when_even_pessimistic_closes(self):
        self.assertEqual(economics.compute(copy.deepcopy(SUBSCRIPTION))["result"], "closes comfortably")

    def test_hinges_when_pessimistic_needs_an_implausible_share(self):
        r = economics.compute(spec(reachable_market=rng(2000, 10000, 15000)))
        self.assertEqual(r["result"], "closes, but hinges on price")

    def test_doesnt_close_when_base_net_contribution_is_negative(self):
        r = economics.compute(spec(cac=rng(500, 400, 300)))
        self.assertEqual(r["result"], "doesn't close")
        self.assertEqual(r["sensitivity"], [])
        self.assertIsNone(r["deciding"])

    def test_doesnt_close_when_base_needs_an_implausible_share(self):
        r = economics.compute(spec(reachable_market=rng(500, 1000, 1500)))  # 108 / 1000 = 10.8%
        self.assertEqual(r["result"], "doesn't close")

    def test_max_share_can_be_changed(self):
        s = spec(reachable_market=rng(500, 1000, 1500))
        s["max_share"] = 0.25  # base 10.8% closes; pessimistic 316 / 500 = 63.2% does not
        self.assertEqual(economics.compute(s)["result"], "closes, but hinges on price")

    def test_an_input_that_breaks_the_business_ranks_first(self):
        r = economics.compute(spec(cac=rng(400, 40, 30)))
        self.assertEqual(r["sensitivity"][0]["input"], "cac")
        self.assertIsNone(r["sensitivity"][0]["customers"])
        self.assertIsNone(r["sensitivity"][0]["change"])
        self.assertEqual(r["deciding"], "cac")

    def test_compute_validates_first(self):
        s = copy.deepcopy(SUBSCRIPTION)
        s["model"] = "freemium"
        with self.assertRaises(economics.InputError):
            economics.compute(s)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests/idea -v`
Expected: 8 ERRORs, `AttributeError: module 'economics' has no attribute 'compute'`

- [ ] **Step 3: Write the minimal implementation**

Add to `skills/idea/economics.py`, after `metrics`:

```python
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests/idea -v`
Expected: `Ran 28 tests` … `OK`

- [ ] **Step 5: Commit**

```bash
git add skills/idea/economics.py tests/idea/test_economics.py
git commit -m "feat(idea): rank inputs by sensitivity and classify the economics"
```

---

### Task 5: `economics.py`: markdown output and CLI

**Files:**
- Modify: `skills/idea/economics.py`
- Test: `tests/idea/test_economics.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/idea/test_economics.py`, above `if __name__ == "__main__":`:

```python
def run_cli(payload):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        path = f.name
    try:
        return subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True)
    finally:
        os.unlink(path)


class Render(unittest.TestCase):
    def test_render_shows_every_output_row(self):
        out = economics.render(economics.compute(copy.deepcopy(SUBSCRIPTION)))
        self.assertIn("Model: subscription · Currency: USD · Target: 1000.00/month · Plausible share: up to 10.00%", out)
        self.assertIn("| Net contribution / month | 5.70 | 14.00 | 20.35 |", out)
        self.assertIn("| LTV / CAC | 2.2 | 8.0 | 23.6 |", out)
        self.assertIn("| Customers for the target | 316 | 108 | 69 |", out)
        self.assertIn("| Market share for the target | 6.32% | 1.08% | 0.46% |", out)
        self.assertIn("| price | 150 | +42 |", out)
        self.assertIn("Deciding variable: price", out)
        self.assertIn("Result: closes comfortably", out)

    def test_render_names_what_cannot_be_reached(self):
        out = economics.render(economics.compute(spec(cac=rng(500, 400, 300))))
        # optimistic: 25 * 0.85 - 0.03 * 300 = 12.25; ceil((400 + 1000) / 12.25) = ceil(114.29) = 115
        self.assertIn("| Customers for the target | never | never | 115 |", out)
        self.assertIn("Deciding variable: none (the base scenario never reaches the target)", out)
        self.assertIn("Result: doesn't close", out)


class Cli(unittest.TestCase):
    def test_prints_the_table(self):
        p = run_cli(SUBSCRIPTION)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("Result: closes comfortably", p.stdout)

    def test_invalid_input_exits_2(self):
        bad = copy.deepcopy(SUBSCRIPTION)
        del bad["inputs"]["cac"]
        p = run_cli(bad)
        self.assertEqual(p.returncode, 2)
        self.assertIn("missing input 'cac'", p.stderr)

    def test_no_argument_prints_usage(self):
        p = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn("usage: economics.py <inputs.json>", p.stderr)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m unittest discover -s tests/idea -v`
Expected: 5 failures or errors: `render` does not exist, and the CLI prints nothing

- [ ] **Step 3: Write the minimal implementation**

Add to `skills/idea/economics.py`, after `compute`:

```python
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
        with open(argv[1]) as f:
            spec = json.load(f)
        print(render(compute(spec)))
    except (OSError, json.JSONDecodeError, InputError) as e:
        print(f"economics.py: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m unittest discover -s tests/idea -v`
Expected: `Ran 33 tests` … `OK`

- [ ] **Step 5: Commit**

```bash
git add skills/idea/economics.py tests/idea/test_economics.py
git commit -m "feat(idea): render the economics as markdown from the command line"
```

---

### Task 6: `MAP-FORMAT.md`

**Files:**
- Create: `skills/idea/MAP-FORMAT.md`

- [ ] **Step 1: Write the file**

Create `skills/idea/MAP-FORMAT.md` with exactly this content:

````markdown
# MAP.md format

`MAP.md` is the one source of truth of an idea: what it is, what it rests on, and how sure we are of each part. A state that changes is rewritten in place; the history lives in `STATUS.md`'s Log.

```md
# {slug}

> {One-line pitch: who, what pain, what you offer.}

- Model: subscription | transactional | one-time | ads
- Created: {YYYY-MM-DD}
- Research topics: [{topic}]({research home}/{topic}/TOPIC.md), ...

## View

{the question, the Mermaid block and the source list `diagram` handed back}

## Problem

| ID | Assumption | Impact | State | Evidence |
| --- | --- | --- | --- | --- |
| P1 | {falsifiable statement} | critical \| high \| low | {state} | {links, or "none yet"} |

## Customer

{same table, IDs CU1, CU2...}

## Solution

{same table, IDs S1...}

## Competition and value added

{same table, IDs V1...}

## Market

{same table, IDs M1...}

## Economics

{same table, IDs E1...}

{the latest run, as ECONOMICS-FORMAT.md lays out, or "Not run yet."}

## Channel

{same table, IDs CH1...}

## Tests

{the test blocks, as TEST-FORMAT.md lays out, or "None."}

## Verdict

{the verdicts, newest first, as LIFECYCLE.md lays out, or "None yet."}
```

## Zones

The seven zones are fixed and always in this order:

| Zone | ID prefix | The question it answers |
| --- | --- | --- |
| Problem | `P` | Does the pain exist, and does it hurt enough to pay? |
| Customer | `CU` | Who exactly suffers it, and how many are they? |
| Solution | `S` | Does what you propose solve that pain? |
| Competition and value added | `V` | Who solves it today, and why would they pick you? |
| Market | `M` | Is it big enough, and is it growing or shrinking? |
| Economics | `E` | Can the numbers close? |
| Channel | `CH` | How do you reach that customer, and at what cost? |

An ID is never reused: a removed assumption leaves a gap in the numbering.

## Assumptions

An assumption is a statement **that can turn out false**. "People want to be more organized" can never be false, so it is not one; "salon owners with 2 to 5 chairs lose more than 3 bookings a week to no-shows" is. Rewrite a vague one until a fact could break it.

Every idea starts with these, which New fills in from the pitch:

- One Value added assumption: "{segment} would pick this over {what they use today} because {what is better}".
- `E1`: "On base inputs the idea reaches the target with a plausible market share", `critical`.

### Impact

- `critical`: if it is false, the idea dies.
- `high`: if it is false, the idea has to pivot (another segment, another price, another channel).
- `low`: if it is false, it is adjusted on the way.

### States

| State | Means | Reached by |
| --- | --- | --- |
| `unknown` | nothing read yet | New |
| `researched (for)` | research tried to break it and failed | Continue |
| `researched (against)` | the facts lean against it, but no `[fact]` proves it false | Continue |
| `researched (mixed)` | the facts point both ways, or are too weak to lean | Continue |
| `in-test` | a test is written and waiting for the user | Test |
| `validated` | a real-world test passed its threshold | Result |
| `dead` | a `[fact]` from a primary source, or a failed test, proves it false | Continue or Result |

```
unknown ──► researched (for | against | mixed) ──► in-test ──► validated
               │                                           └──► dead
               └──► dead   (only on a primary-source [fact] against it)
```

- **Desk research never validates.** It reaches `researched (for)` at most.
- **`[secondary]` and `[inference]` never kill.** Alone they leave an assumption `researched (against)`.
- An assumption already researched is researched again when a fact it rests on expires, or when the user brings new evidence; its state moves between the researched states.
- A `dead` or `validated` assumption only changes when the user explicitly reopens it; the Log says why.

### Evidence

Evidence is a link, never a copied fact:

- A `research` section: `[{topic} § {question}]({research home}/{topic}/TOPIC.md#{anchor})`.
- A test in this map: `[T{n}](#tests)`.
- An economics run: `[run {YYYY-MM-DD}](#economics)`.

## Competition

A Competition and value added assumption asks `research` for a **competitor table** in the industry topic, as the Answer of a section titled "Who solves {the problem} today", every cell backed by a fact under that section's Facts:

```md
| Competitor | Segment | Price | Weakness users report | Source |
| --- | --- | --- | --- | --- |
| {name} | {who it serves} | {price and period, or "free"} | {what reviews or forums complain about} | {fact or secondary, with its source} |
```

The value-added assumption is researched against that table: "better than {competitors} at {what} for {segment}" is broken by a competitor that already does it for that segment.

## The view

`diagram` draws one overview, so it stays within its node limit. Hand it:

- The question: "Where does {slug} stand?"
- The kind: a `flowchart LR` with one node per zone, in the order above, and no edges between them.
- Each node's label: the zone's name and its counts by state (`Problem · 1 for · 1 unknown`).
- Each node's color: the state of its riskiest assumption, in this order from worst to best: `dead` > `researched (against)` > `unknown` > `researched (mixed)` > `in-test` > `researched (for)` > `validated`.
- The source: this `MAP.md`.

Write what it hands back under `## View`, replacing the previous view. Redraw it every time a state changes. With no Node, `diagram` marks it unverified; the tables stay the source of truth.

# STATUS.md format

```md
# {slug}

- State: exploring | testing | discarded | parked
- Target: {amount} {currency} a month, or "break-even"
- Verdict: {the latest verdict} on {YYYY-MM-DD}, or "none yet"

## Log

- {YYYY-MM-DD} · {one line: what happened, and why}
```

The Log is append-only. Every intent that changes the idea writes one line: an assumption's new state and the fact behind it, a test written, a result, an economics run, a verdict, an outcome, a declined offer of a test.

# IDEAS.md format

`<ideas home>/IDEAS.md` keeps every idea Generate proposed and the user did not pick, newest last:

```md
# Ideas not picked

- {YYYY-MM-DD} · {pitch} · Pays: {who} · Would die if: {the assumption most likely to kill it} · From: {the starting point}
```
````

- [ ] **Step 2: Commit**

```bash
git add skills/idea/MAP-FORMAT.md
git commit -m "feat(idea): define the map, status and ideas formats"
```

---

### Task 7: `ECONOMICS-FORMAT.md`

**Files:**
- Create: `skills/idea/ECONOMICS-FORMAT.md`

- [ ] **Step 1: Write the file**

Create `skills/idea/ECONOMICS-FORMAT.md` with exactly this content:

````markdown
# Economics format

The economics answer one question: **can this close, and what does it hinge on?** They are unit economics with three scenarios, never a multi-year projection: at the idea stage a P&L is invented numbers with decimals. **Every derived number comes from `economics.py`**, never from your head.

## Models

The model sets how a customer pays. Propose it from the pitch; the user corrects it.

| Model | Revenue per customer per month | Model inputs |
| --- | --- | --- |
| `subscription` | price | `price` |
| `transactional` | volume × take rate | `volume` (what a customer moves a month), `take_rate` (0 to 1) |
| `one-time` | price ÷ months between purchases | `price`, `months_between_purchases` |
| `ads` | ad revenue per user | `ad_arpu` (a customer is a user) |

For `one-time`, `monthly_churn` is the monthly share of buyers who never buy again.

## Inputs

Every model also takes:

| Input | What it is | Where it comes from |
| --- | --- | --- |
| `gross_margin` | 0 to 1: what is left of the revenue after the cost of serving the customer (infra, payment fees, AI tokens, support) | the provider's own prices, read by `research` |
| `cac` | cost to acquire one customer | the Channel zone; an industry benchmark is `[secondary]`, never `[fact]` |
| `monthly_churn` | 0 to 1: the share of customers lost each month | a benchmark for the model and the segment |
| `fixed_costs` | the minimum a month to operate | the providers' prices plus what the user says they would spend |
| `reachable_market` | how many customers the idea can reach | the Market zone |

`price` comes from the competitor table (MAP-FORMAT.md, Competition). When nobody charges for anything similar, say so: that is information, and the price is then an `[inference]` named as such.

Every input has three values: **pessimistic** (bad for the business: low price, high CAC, high churn), **base** and **optimistic**. Each value is labeled as TOPIC-FORMAT.md in `research` defines and links the fact it comes from. A value with no source is the user's guess and is labeled `[unverified]`.

**The target** is asked once per idea: "how much a month do you want it to make, once costs are paid?" It is written in `STATUS.md`; with no answer, the target is break-even (0).

**The plausible share** (`max_share`) is the largest share of the reachable market the idea may need. It defaults to 10%, a rule of thumb; the user may change it, and the run says which was used.

## Running

1. Write `<idea>/economics.json`:

```json
{
  "model": "subscription",
  "currency": "USD",
  "target": 1000,
  "max_share": 0.10,
  "inputs": {
    "price": {"pessimistic": 15, "base": 20, "optimistic": 25},
    "gross_margin": {"pessimistic": 0.7, "base": 0.8, "optimistic": 0.85},
    "cac": {"pessimistic": 60, "base": 40, "optimistic": 30},
    "monthly_churn": {"pessimistic": 0.08, "base": 0.05, "optimistic": 0.03},
    "fixed_costs": {"pessimistic": 800, "base": 500, "optimistic": 400},
    "reachable_market": {"pessimistic": 5000, "base": 10000, "optimistic": 15000}
  }
}
```

2. Run `python3 <this skill's folder>/economics.py <idea>/economics.json`. It exits 2 with the reason on a wrong input: fix the JSON and run it again.
3. Without `python3`, tell the user, and stop the economics: `E1` stays where it is, and the verdict cannot be "worth testing" until a run exists.

## Formulas

What the script computes, written under every run so anyone can redo it:

- **Contribution** = revenue per customer × gross margin
- **Net contribution** = contribution − monthly churn × CAC: what a customer leaves once replacing the customers who churn is paid for
- **LTV** = contribution ÷ monthly churn
- **LTV / CAC**: below 3 is a warning; below 1 every customer loses money
- **CAC payback** = CAC ÷ contribution, in months
- **Customers needed** = (fixed costs + target) ÷ net contribution, rounded up; for break-even the target is 0
- **Market share needed** = customers needed ÷ reachable market
- **Sensitivity**: each input except the reachable market moved to its pessimistic value alone, the rest at base, ranked by how many customers it adds. The first is **the deciding variable**.

A scenario **closes** when its net contribution is positive and its market share for the target is at most `max_share`. The **result**:

- **doesn't close**: the base scenario does not close.
- **closes, but hinges on {X}**: base closes, pessimistic does not. X is the deciding variable.
- **closes comfortably**: even pessimistic closes. Rare: give the inputs a second look, and say so.

## Writing a run

Under the Economics zone's table in `MAP.md`, replacing the previous run:

```md
### Run {YYYY-MM-DD}

| Input | Pessimistic | Base | Optimistic | Source |
| --- | --- | --- | --- | --- |
| {input} | {value} | {value} | {value} | {label and link for each value} |

{the script's output, pasted as it printed it}

{the Formulas list above}
```

Then:

1. Set `E1` from the result: **closes comfortably** or **closes, but hinges** → `researched (for)`; **doesn't close** → `researched (against)`. Link the run.
2. When the deciding variable is not already a `critical` Economics assumption, add one ("{input} is at least {its base value}", `critical`), and say so.
3. Log the run with its result.

An Economics assumption waits until the assumptions its inputs come from (price from Competition, CAC from Channel, reachable market from Market) are researched; until then Continue skips it. A run is **stale** when a fact one of its inputs links has expired; Continue runs it again after `research` re-verifies that fact.
````

- [ ] **Step 2: Commit**

```bash
git add skills/idea/ECONOMICS-FORMAT.md
git commit -m "feat(idea): define the economics format"
```

---

### Task 8: `TEST-FORMAT.md`

**Files:**
- Create: `skills/idea/TEST-FORMAT.md`

- [ ] **Step 1: Write the file**

Create `skills/idea/TEST-FORMAT.md` with exactly this content:

````markdown
# Test format

A test is how an assumption leaves the desk. It is **always optional**: offer it when a critical assumption is left `researched (mixed)` or `researched (against)`, or when the user asks; a declined offer is logged and the work goes on. **The threshold is written before the test runs, and never moves afterwards**: a threshold set after the result is a way of convincing yourself it passed.

## Kinds

Pick the cheapest kind that can settle the assumption:

| Kind | Settles | Typical threshold |
| --- | --- | --- |
| `interviews` | whether the problem exists and hurts (Problem, Customer) | "at least 4 of 6 lost a booking to a no-show in the last month" |
| `smoke-test` | whether people want the solution enough to act (Solution, Value added, Channel) | "at least 5% of 200 visits leave their email" |
| `pre-sale` | whether they pay (Economics, Value added) | "at least 3 of 20 asked pay the deposit" |

A pre-sale is the strongest signal there is, because it is real money; prefer it whenever the user can sell before building.

### Interviews

The questions ask about what the person **did**, never what they would do. Everyone says they would use it, and almost nobody pays.

- Ask about the last time it happened: "When did a client last miss a booking? What did you do?"
- Ask what it cost them and what they already tried: someone who never looked for a fix does not hurt enough.
- Never pitch before the questions are done: once they know the idea, they are polite about it.
- Count what happened, never opinions: "lost a booking last month" counts, "it would be useful" does not.

Write 5 to 8 questions in the test block.

### Smoke test

Write what the page must say (the pitch, the price when it is being tested, one call to action) and where the traffic comes from. The skill does not build the page.

## The test block

Under `## Tests` in `MAP.md`, numbered `T1`, `T2`... and never reused:

```md
### T{n} · {assumption ID} · {kind}

- Written: {YYYY-MM-DD}
- Assumption: {ID}: {statement}
- Method: {what the user does, step by step}
- Sample: {how many, who, where to find them}
- Metric: {what is counted}
- Passes when: {the threshold, as a number}
- Questions: {interviews only: the numbered questions}
- Result: pending
```

## Test

1. Name the assumption, or take the one Continue would pick among the critical ones left `mixed` or `against`.
2. Propose the kind, the sample, the metric and the threshold, and say why that threshold: what result would make you believe it, and what would not.
3. **Checkpoint:** the user corrects the block; then write it, set the assumption to `in-test`, link the test, redraw the view and log it.

Done when the block is written with a threshold, and the assumption is `in-test`.

## Result

The user ran a test and tells what happened.

1. Write the raw numbers the user gives under the block's Result, with the date: "6 interviewed, 4 lost a booking last month". Quotes from interviews go in as said.
2. Compare against **Passes when**, and nothing else:
   - At or above it: the assumption becomes `validated`.
   - Below it: the assumption becomes `dead`.
   - A smaller sample than the block says: **inconclusive**. The assumption goes back to its researched state, and the test stays open.
3. A user who wants a different threshold after seeing the result gets a new test, `T{n+1}`, with the new threshold; the Log says it changed from what to what. The result already in stays judged against the old threshold.
4. Link the result, redraw the view, log it, and say what changed in the verdict, if there is one.

Done when the result is written, the assumption has its state from the threshold, and the Log has the line.
````

- [ ] **Step 2: Commit**

```bash
git add skills/idea/TEST-FORMAT.md
git commit -m "feat(idea): define the optional tests"
```

---

### Task 9: `LIFECYCLE.md`

**Files:**
- Create: `skills/idea/LIFECYCLE.md`

- [ ] **Step 1: Write the file**

Create `skills/idea/LIFECYCLE.md` with exactly this content:

````markdown
# Lifecycle

What happens to an idea once its map exists. Each section is one intent from SKILL.md and runs on the idea it resolved.

```
exploring ──▶ testing
    │  ▲         │
    │  └─────────┤
    ├──▶ parked ─┤
    └──▶ discarded
```

Any state may go back to `exploring`.

## Verdict

The user asks for the verdict. It can be asked at any time; the rules say what it can be.

1. Read `MAP.md`. When the economics run is stale, or a fact the map rests on has expired, say so first and offer to re-verify through `research`; the user may ask for the verdict as it stands.
2. Apply the rules **top to bottom**; the first that matches is the verdict:

| Verdict | When |
| --- | --- |
| **Discard** | A `critical` assumption is `dead`, or the latest economics run doesn't close |
| **Not enough information** | A `critical` assumption is still `unknown`: Continue has not reached it, or research found nothing either way |
| **Worth testing** | None of the above: no critical dead, none unknown, and the economics close on base |

A critical `researched (against)` counts as `researched (mixed)` in these rules, and is named first among the assumptions to test and as the best reason not to do it.

3. Write the verdict at the top of `## Verdict`, keeping the previous ones below it, and copy its name and date into `STATUS.md`:

```md
### {YYYY-MM-DD} · {Discard | Not enough information | Worth testing}

- Why: {the rule that matched, with the assumption IDs and the economics result}
- Best reason not to do it: {one or two lines, linked}
- To test next: {2 or 3 IDs, each with the test kind that settles it} (Worth testing only)
- Still unknown: {the critical IDs} (Not enough information only)
- Rests on: {the research sections and the economics run, and the earliest expiry among their facts}

#### What this idea demands

- Capital to start: {range and currency}: {what it goes to}
- Key skills: {the two or three that decide it, e.g. "selling B2B by phone", "content SEO"}
- Hours a week: {to an MVP} · {to operate it}
- Access: {who must be reached, and how many: "50 salon owners"}
- Time to first revenue: {range}
- Hardest part: {one line}
```

**The best reason not to do it is always written**, even for "worth testing": the strongest fact or assumption against the idea. Not finding one means the research did not look hard enough: go back to the weakest critical assumption.

**What this idea demands describes the work, never the user.** It never says whether the user can do it: the user compares it with what they have. Each line that rests on a fact links it; the rest is an `[inference]`, named as such.

4. Show the verdict, and ask what the user wants to do (Outcome). "Worth testing" offers to design the tests to test next (TEST-FORMAT.md).

Done when the verdict is written with its reason, the best reason not to do it and what the idea demands, `STATUS.md` has it, and the Log has the line.

## Outcome

The user decides. Set the state in `STATUS.md` and log the reason in the user's words:

- **testing**: the user will run tests. When the latest verdict is not "worth testing", say what it is first; the user decides anyway. Offer Test for each assumption to test next.
- **parked**: good, not now. Nothing else changes; List keeps showing it, with its verdict going stale as its facts expire.
- **discarded**: the reason is logged. The map stays as it is: it is what the next idea in the same industry learns from, and its `research` topics stay for that idea.
- **exploring**: back to work on the map; Continue picks the next assumption.

Done when `STATUS.md` has the new state and the Log has the reason.

## Stale verdicts

A verdict is **stale** when a fact it rests on has expired, as `research` defines expiry, or when an assumption changed state after the verdict's date. List shows it as stale, and Continue says so before picking. A stale verdict is never handed back as current: offer to re-verify through `research`, then issue it again.
````

- [ ] **Step 2: Commit**

```bash
git add skills/idea/LIFECYCLE.md
git commit -m "feat(idea): define the verdict and the idea lifecycle"
```

---

### Task 10: `SKILL.md`

**Files:**
- Create: `skills/idea/SKILL.md`

- [ ] **Step 1: Write the file**

Create `skills/idea/SKILL.md` with exactly this content:

````markdown
---
name: idea
description: Clarify a product, startup or digital-business idea into a map of falsifiable assumptions, each researched by trying to refute it, with ranged unit economics and a dated verdict the user decides on.
disable-model-invocation: true
argument-hint: "<idea>: what to do (an idea to map, a test result, verdict), generate: <starting point>, or nothing to list your ideas"
---

An idea is a building on ground nobody has surveyed. This skill never promises the building stands: it surveys the ground fast and says where it will not hold. Each idea is a **map of falsifiable assumptions** in seven zones, and every step lowers the uncertainty with facts that are labeled, sourced and dated. **Research tries to break an assumption, never to confirm it**: an agent asked to confirm an idea always does, and only what survives an attempt to break it is worth anything. Desk research is the default and is fast; a real-world test is offered, never required. The decision is always the user's.

## Locating the idea

The **ideas home** is `$ARSENAL_IDEAS_HOME` when set, else `~/ideas`. Each idea is one folder, `<ideas home>/<slug>/`, holding `MAP.md` and `STATUS.md`; `<ideas home>/IDEAS.md` keeps the ideas Generate proposed and the user did not pick.

1. **No argument:** the intent is **List**.
2. An argument that starts with `generate` is **Generate**; what follows its colon is the starting point.
3. Otherwise split the argument at its first colon into the idea and the rest. Slug the idea in kebab-case; if it is close to an existing idea's folder, ask whether it is the same idea.
4. Read the intent from the rest; when it fits none of these, ask what the user wants to do:

| Intent | Example argument | Idea folder | Then |
| --- | --- | --- | --- |
| **List** | (nothing) | none | [List](#list) |
| **Generate** | `generate: I'm an accountant and small firms keep asking me for the same report` | none | [Generate](#generate) |
| **New** | `salon-bookings: salons take a deposit with each booking so no-shows cost the client` | missing: create it | [New](#new) |
| **Continue** | `salon-bookings`, `salon-bookings: go on` | exists | [Continue](#continue) |
| **Test** | `salon-bookings: design the interview for P1` | exists | [TEST-FORMAT.md](./TEST-FORMAT.md), Test |
| **Result** | `salon-bookings: did 6 interviews, 4 lost a booking last month` | exists | [TEST-FORMAT.md](./TEST-FORMAT.md), Result |
| **Verdict** | `salon-bookings: verdict` | exists | [LIFECYCLE.md](./LIFECYCLE.md), Verdict |
| **Outcome** | `salon-bookings: I'm parking it`, `salon-bookings: discard it` | exists | [LIFECYCLE.md](./LIFECYCLE.md), Outcome |

A description of an idea under a slug whose folder already holds a different idea asks for another slug.

Done when you hold the ideas home, one intent and, unless it is List or Generate, one absolute idea path, and have told the user all of them.

## Where things are written

Write only inside the ideas home. Facts about a market, an industry or a competitor live in `research` topics and are linked from `MAP.md`, never copied: they expire, and `research` is what re-verifies them. The repo the session was opened in is never written to. Every intent that changes an idea appends one line to its `STATUS.md` Log, as [MAP-FORMAT.md](./MAP-FORMAT.md) lays out.

## List

Read every `STATUS.md` and `MAP.md` under the ideas home and show one row per idea: slug, state, the latest verdict and its date, how many critical assumptions are still open, and whether the verdict is stale ([LIFECYCLE.md](./LIFECYCLE.md), Stale verdicts). Then ask which idea to continue, or whether to start or generate one. With no ideas yet, ask for the first idea, or for a starting point to generate from.

Done when the user has the table, or was asked for the first idea.

## Generate

When the argument gave no starting point, ask for one: a **problem** the user has seen, an **industry** they know, or a **skill** they have. Never ask for a profile: the starting point is all Generate needs.

1. Propose 3 to 5 ideas, each as: a one-line pitch, who pays, and **the assumption most likely to kill it**, phrased so a fact could break it. Do not research yet: this is a quick filter, and an idea earns research by being picked.
2. The user picks one, combines two, or asks for another round.
3. Append the ideas not picked to `IDEAS.md` as MAP-FORMAT.md lays out, and run **New** on the picked one.

Done when one idea went to New and the rest are in `IDEAS.md`.

## New

Read [MAP-FORMAT.md](./MAP-FORMAT.md) and [ECONOMICS-FORMAT.md](./ECONOMICS-FORMAT.md).

1. Write the pitch in one line: who, what pain, what you offer. Ask only what the description leaves impossible to write.
2. Propose the revenue model (ECONOMICS-FORMAT.md, Models), and ask for the target (ECONOMICS-FORMAT.md, Inputs).
3. Propose 2 to 4 assumptions per zone, each falsifiable and with its impact, including the two every idea starts with (MAP-FORMAT.md, Assumptions). Rewrite a vague one until a fact could break it, and say what you rewrote.
4. **Checkpoint:** show the pitch, the model, the target and the assumptions. The user corrects, removes or adds; then write `MAP.md`, and `STATUS.md` with the state `exploring`, and draw the view (MAP-FORMAT.md, The view).
5. Offer to start Continue now.

Done when `MAP.md` holds the pitch, the model and every zone with at least one assumption, the user has seen them at the checkpoint, and the Log has the line.

## Continue

Read `MAP.md`, MAP-FORMAT.md, and the `research` sections its evidence links. When the latest verdict is stale, say so first.

1. **Pick** the next assumption: the open `critical` one with the least evidence, `unknown` before `researched (mixed)` before `researched (against)`; on a tie, the cheapest to research. With no critical one open, the same over `high`. An assumption `in-test` waits for the user, and an Economics assumption waits for its inputs (ECONOMICS-FORMAT.md, Writing a run): skip both. Tell the user which one and why.
2. **Economics:** when the pick is in the Economics zone, run the economics as ECONOMICS-FORMAT.md lays out, and skip step 3.
3. **Research:** hand the question to `research`, in the background when the host can, so the user keeps working; a host that cannot runs it in the foreground. The topic is the industry's (`salons-ar`) or a cross-cutting one (`online-payments-ar`), reusing a topic another idea already created. **Phrase the question to refute the assumption**: "what shows salon owners do not lose bookings to no-shows, or do not care?", never "confirm that salons lose bookings". A Competition and value added assumption asks for the competitor table (MAP-FORMAT.md, Competition).
4. **Update:** when the answer returns, set the assumption's state by the transitions in MAP-FORMAT.md, link the sections, redraw the view, and log it.
5. A critical assumption left `researched (mixed)` or `researched (against)` gets the offer of a test (TEST-FORMAT.md). The user may decline; the Log says so and Continue goes on.

The user may ask for several assumptions in one turn; each still gets its own refuting question.

Done when the picked assumption has a new state backed by linked facts, or the economics ran; the view is redrawn; the Log has the line; and the user knows what Continue would pick next, or that the map is ready for a verdict.

## Language

An idea keeps the language it was created in: the language of the conversation that created it. Its `research` questions are asked in that language too.

## Never

- **State a market fact from memory.** A competitor, a price, a market size or a law is `research`, with its label and its source.
- **Validate from the desk.** Desk research reaches `researched (for)` at most; `validated` takes a real-world test.
- **Do arithmetic on money in your head.** Every derived number comes from `economics.py`.
- **Judge the user.** The verdict describes what the idea demands; whether that fits the user is theirs to say.
- **Move a threshold** after a test ran.
````

- [ ] **Step 2: Validate the plugin**

Run: `claude plugin validate .`
Expected: validation passes with no errors

- [ ] **Step 3: Commit**

```bash
git add skills/idea/SKILL.md
git commit -m "feat(idea): add the idea skill"
```

---

### Task 11: README, CHANGELOG and version

**Files:**
- Modify: `README.md` (skills table row after `interview`; new section after `### \`interview\`: where your preparation lives`, before `## Layout`)
- Modify: `CHANGELOG.md` (new entry above `## [0.5.0] - 2026-10-19`)
- Modify: `.claude-plugin/plugin.json` (`"version": "0.5.0"` → `"0.6.0"`)

- [ ] **Step 1: Add the README table row**

After the row that starts with `| \`interview\` |`, add:

```md
| `idea` | Clarifies a product or startup idea: a map of falsifiable assumptions, each researched by trying to refute it, ranged unit economics computed by a script, and a dated verdict with what the idea demands | user (`/arsenal:idea <idea>: <what to do>`) |
```

- [ ] **Step 2: Add the README section**

Before `## Layout`, add:

```md
### `idea`: where your ideas live

Ideas live in `$ARSENAL_IDEAS_HOME` when the variable is set, else `~/ideas/`, never in a project's repo:

- Each idea gets `<slug>/`, with `MAP.md` (the pitch, the revenue model, seven zones of falsifiable
  assumptions with their impact and state, the economics, the tests and the verdicts) and `STATUS.md`
  (exploring, testing, parked or discarded, with a log). `IDEAS.md` keeps the ideas you generated and
  did not pick.
- Every assumption is researched by trying to refute it, through `research`, so its facts are labeled,
  sourced and expire. Desk research never validates: `validated` takes a real-world test, which is
  always offered and never required, with its threshold written before it runs.
- The economics run three scenarios through `economics.py` (Python 3, standard library): LTV, LTV/CAC,
  payback, customers and market share needed for your target, and the variable the result hinges on.

`/arsenal:idea generate: <a problem, an industry or a skill>` proposes ideas to pick from;
`/arsenal:idea <idea>` researches the riskiest open assumption; `<idea>: verdict` says discard, not
enough information, or worth testing, with the best reason not to do it and what the idea demands. The
map's view is drawn with `diagram`.
```

- [ ] **Step 3: Add the CHANGELOG entry**

Above `## [0.5.0] - 2026-10-19`, add:

```md
## [0.6.0] - 2026-10-20

### Added

- **`idea`** (`/arsenal:idea <idea>: <what to do>`): clarifies a product, startup or digital-business
  idea into an explicit decision.
  - Lives at `$ARSENAL_IDEAS_HOME`, default `~/ideas/`: one folder per idea with `MAP.md` and
    `STATUS.md`, and `IDEAS.md` for generated ideas not picked.
  - An idea is a map of falsifiable assumptions in seven fixed zones (problem, customer, solution,
    competition and value added, market, economics, channel), each with an impact and a state, drawn
    as an overview with `diagram`.
  - Continue picks the critical assumption with the least evidence and hands `research` a question
    phrased to refute it. Desk research reaches `researched` at most and can kill on a primary
    `[fact]`; `validated` takes a real-world test (interviews, smoke test, pre-sale), always optional,
    with its threshold written before it runs and never moved.
  - Unit economics in three scenarios computed by `economics.py`: net contribution after replacing
    churn, LTV, LTV/CAC, payback, customers and market share needed for the user's target, and a
    sensitivity pass whose deciding variable becomes a critical assumption.
  - The verdict (discard, not enough information, worth testing) always carries the best reason not to
    do it and what the idea demands (capital, skills, hours, access, time to revenue), never a
    judgment of the user, and goes stale when the facts it rests on expire.
```

- [ ] **Step 4: Bump the version**

In `.claude-plugin/plugin.json`, change `"version": "0.5.0"` to `"version": "0.6.0"`.

- [ ] **Step 5: Validate and run the tests**

Run: `claude plugin validate . && python3 -m unittest discover -s tests/idea`
Expected: validation passes; `Ran 33 tests` … `OK`

- [ ] **Step 6: Commit**

```bash
git add README.md CHANGELOG.md .claude-plugin/plugin.json
git commit -m "docs: document the idea skill and release 0.6.0"
```

---

### Task 12: Real run and audit (with the user)

This task needs the user: it is the field test that found the gaps in `interview`.

**Files:**
- Possibly modify: any file under `skills/idea/`

- [ ] **Step 1: Run the skill on a real idea**

Ask the user for one of their ideas, then run in a fresh session with the local checkout:

```bash
ARSENAL_IDEAS_HOME=~/ideas-test claude --plugin-dir .
```

Inside it: `/arsenal:idea generate: <starting point>` or `/arsenal:idea <slug>: <description>`, then Continue 3 or 4 times, through the economics, then `<slug>: verdict`.

- [ ] **Step 2: Audit the transcript against the skill text**

For every intent that ran, list where the agent deviated from the text (a research question phrased to confirm, a number computed outside `economics.py`, a state moved against the transitions, a verdict without the best reason not to do it) and where the text was ambiguous enough to allow it.

- [ ] **Step 3: Fix and commit**

One commit per fix, `fix(idea): <what>`, then run `python3 -m unittest discover -s tests/idea` and `claude plugin validate .` again.
