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

    def test_top_level_must_be_an_object(self):
        with self.assertRaisesRegex(economics.InputError, "the input must be a JSON object"):
            economics.validate([SUBSCRIPTION])

    def test_inputs_must_be_an_object(self):
        s = copy.deepcopy(SUBSCRIPTION)
        s["inputs"] = 5
        with self.assertRaisesRegex(economics.InputError, "inputs must be an object"):
            economics.validate(s)

    def test_a_range_must_be_an_object(self):
        s = spec(price=20)
        with self.assertRaisesRegex(economics.InputError, "'price' must be an object with pessimistic, base and optimistic values"):
            economics.validate(s)

    def test_model_must_be_a_string(self):
        s = copy.deepcopy(SUBSCRIPTION)
        s["model"] = ["a"]
        with self.assertRaisesRegex(economics.InputError, "model must be a string"):
            economics.validate(s)

    def test_nan_value(self):
        s = spec(price=rng(15, float("nan"), 25))
        with self.assertRaisesRegex(economics.InputError, "'price' base must be a finite number"):
            economics.validate(s)

    def test_infinite_value(self):
        s = spec(cac=rng(float("inf"), 40, 30))
        with self.assertRaisesRegex(economics.InputError, "'cac' pessimistic must be a finite number"):
            economics.validate(s)

    def test_nan_target(self):
        s = copy.deepcopy(SUBSCRIPTION)
        s["target"] = float("nan")
        with self.assertRaisesRegex(economics.InputError, "target must be a finite number, 0 or more"):
            economics.validate(s)

    def test_boolean_target(self):
        s = copy.deepcopy(SUBSCRIPTION)
        s["target"] = True
        with self.assertRaisesRegex(economics.InputError, "target must be a finite number, 0 or more"):
            economics.validate(s)

    def test_boolean_max_share(self):
        s = copy.deepcopy(SUBSCRIPTION)
        s["max_share"] = True
        with self.assertRaisesRegex(economics.InputError, "max_share must be a finite number above 0 and at most 1"):
            economics.validate(s)


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

    def test_transactional_end_to_end(self):
        s = {
            "model": "transactional",
            "target": 500,
            "inputs": {
                "volume": rng(800, 1000, 1200),
                "take_rate": rng(0.045, 0.05, 0.06),
                "gross_margin": rng(0.8, 0.9, 0.95),
                "cac": rng(50, 30, 20),
                "monthly_churn": rng(0.06, 0.04, 0.02),
                "fixed_costs": rng(550, 400, 300),
                "reachable_market": rng(3000, 5000, 8000),
            },
        }
        r = economics.compute(s)
        # base: 1000 * 0.05 * 0.9 - 0.04 * 30 = 43.8; ceil((400 + 500) / 43.8) = ceil(20.55) = 21
        self.assertEqual(r["scenarios"]["base"]["customers_target"], 21)
        # pessimistic: 800 * 0.045 * 0.8 - 0.06 * 50 = 25.8; ceil(1050 / 25.8) = 41; 41 / 3000 = 1.37%
        self.assertEqual(r["result"], "closes comfortably")
        # volume 800: 36 - 1.2 = 34.8 -> 26 (+5); gross_margin and fixed_costs -> 24 (+3); take_rate -> 23 (+2)
        self.assertEqual(r["deciding"], "volume")

    def test_one_time_end_to_end(self):
        s = {
            "model": "one-time",
            "target": 1000,
            "inputs": {
                "price": rng(100, 150, 200),
                "months_between_purchases": rng(15, 12, 6),
                "gross_margin": rng(0.5, 0.6, 0.7),
                "cac": rng(40, 25, 15),
                "monthly_churn": rng(0.05, 0.03, 0.02),
                "fixed_costs": rng(1000, 800, 600),
                "reachable_market": rng(2000, 4000, 6000),
            },
        }
        r = economics.compute(s)
        # base: 150 / 12 * 0.6 - 0.03 * 25 = 6.75; ceil(1800 / 6.75) = ceil(266.67) = 267; 267 / 4000 = 6.68%
        self.assertEqual(r["scenarios"]["base"]["customers_target"], 267)
        # pessimistic: 100 / 15 * 0.5 - 0.05 * 40 = 1.33; ceil(2000 / 1.33) = 1500; 1500 / 2000 = 75%
        self.assertEqual(r["result"], "closes, but hinges on price")
        # price 100: 100 / 12 * 0.6 - 0.75 = 4.25 -> 424 (+157); months 15: 5.25 -> 343 (+76)
        self.assertEqual(r["deciding"], "price")

    def test_ads_end_to_end(self):
        s = {
            "model": "ads",
            "inputs": {
                "ad_arpu": rng(0.3, 0.5, 0.8),
                "gross_margin": rng(0.8, 0.9, 0.95),
                "cac": rng(2, 1, 0.5),
                "monthly_churn": rng(0.1, 0.08, 0.05),
                "fixed_costs": rng(500, 400, 300),
                "reachable_market": rng(5000, 8000, 12000),
            },
        }
        r = economics.compute(s)
        # no target, so break-even: 0.5 * 0.9 - 0.08 * 1 = 0.37; ceil(400 / 0.37) = ceil(1081.08) = 1082
        self.assertEqual(r["scenarios"]["base"]["customers_target"], 1082)
        # 1082 / 8000 = 13.5%, above the default 10%
        self.assertEqual(r["result"], "doesn't close")
        # ad_arpu 0.3: 0.27 - 0.08 = 0.19 -> 2106 (+1024); cac 2: 0.29 -> 1380 (+298); fixed_costs 500 -> 1352 (+270)
        self.assertEqual(r["deciding"], "ad_arpu")

    def test_compute_validates_first(self):
        s = copy.deepcopy(SUBSCRIPTION)
        s["model"] = "freemium"
        with self.assertRaises(economics.InputError):
            economics.compute(s)


def run_cli(payload):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        path = f.name
    try:
        return subprocess.run([sys.executable, SCRIPT, path], capture_output=True, text=True)
    finally:
        os.unlink(path)


def run_cli_raw(data):
    with tempfile.NamedTemporaryFile("wb", suffix=".json", delete=False) as f:
        f.write(data)
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

    def test_top_level_array_exits_2(self):
        self.assert_rejected(run_cli([SUBSCRIPTION]), "the input must be a JSON object")

    def test_inputs_not_an_object_exits_2(self):
        bad = copy.deepcopy(SUBSCRIPTION)
        bad["inputs"] = 5
        self.assert_rejected(run_cli(bad), "inputs must be an object")

    def test_scalar_range_exits_2(self):
        self.assert_rejected(run_cli(spec(price=20)), "'price' must be an object")

    def test_model_not_a_string_exits_2(self):
        bad = copy.deepcopy(SUBSCRIPTION)
        bad["model"] = ["a"]
        self.assert_rejected(run_cli(bad), "model must be a string")

    def test_nan_value_exits_2(self):
        raw = json.dumps(SUBSCRIPTION).replace('"base": 20,', '"base": NaN,')
        self.assert_rejected(run_cli_raw(raw.encode()), "'price' base must be a finite number")

    def test_nan_target_exits_2(self):
        raw = json.dumps(SUBSCRIPTION).replace('"target": 1000', '"target": NaN')
        self.assert_rejected(run_cli_raw(raw.encode()), "target must be a finite number")

    def test_infinity_value_exits_2(self):
        raw = json.dumps(SUBSCRIPTION).replace('"base": 40,', '"base": Infinity,')
        self.assert_rejected(run_cli_raw(raw.encode()), "'cac' base must be a finite number")

    def test_overflowing_value_exits_2(self):
        raw = json.dumps(SUBSCRIPTION).replace('"base": 500,', '"base": 1e400,')
        self.assert_rejected(run_cli_raw(raw.encode()), "'fixed_costs' base must be a finite number")

    def test_boolean_target_exits_2(self):
        bad = copy.deepcopy(SUBSCRIPTION)
        bad["target"] = True
        self.assert_rejected(run_cli(bad), "target must be a finite number")

    def test_boolean_max_share_exits_2(self):
        bad = copy.deepcopy(SUBSCRIPTION)
        bad["max_share"] = True
        self.assert_rejected(run_cli(bad), "max_share must be a finite number")

    def test_non_utf8_file_exits_2(self):
        raw = json.dumps(SUBSCRIPTION).replace('"USD"', '"US\\u00e9"').encode().replace(b"\\u00e9", b"\xe9")
        self.assert_rejected(run_cli_raw(raw), "is not UTF-8 text")

    def assert_rejected(self, p, message):
        self.assertEqual(p.returncode, 2, p.stderr)
        self.assertIn(message, p.stderr)
        self.assertNotIn("Traceback", p.stderr)

    def test_no_argument_prints_usage(self):
        p = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn("usage: economics.py <inputs.json>", p.stderr)


if __name__ == "__main__":
    unittest.main()
