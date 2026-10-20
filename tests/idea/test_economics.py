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
