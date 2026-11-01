"""Synthetic edge cases. These do NOT certify Pine compilation or investment results."""
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from policy_reference import AlertGate, evaluate, interpret, quarter_day, quarter_key, vix_fix


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 1, 15)
        self.close = datetime(2026, 9, 30, 16)
        self.base = dict(quantities=(25, 25, 30, 20), prices=(100,) * 4,
                         cash=0, reserve=0, targets=(25, 25, 30, 20),
                         now=self.now, checked_at=self.now,
                         price_closes=(self.close,) * 4)

    def run_case(self, **kwargs):
        return evaluate(**(self.base | kwargs))

    def test_exact_target(self):
        result = self.run_case()
        self.assertEqual(result.state, "ON_TRACK")
        self.assertEqual(result.weights, (25, 25, 30, 20))

    def test_band_boundary(self):
        for deviation, state in [(4.99, "QUARTERLY_REVIEW"), (5, "REBALANCE_REVIEW"), (5.01, "REBALANCE_REVIEW")]:
            with self.subTest(deviation=deviation):
                result = self.run_case(quantities=(25 + deviation, 25 - deviation, 30, 20), review_due=True)
                self.assertEqual(result.state, state)

    def test_cash_is_in_denominator(self):
        result = self.run_case(cash=2500)
        self.assertEqual(result.weights, (20, 20, 24, 16))
        self.assertAlmostEqual(sum(result.gaps), 2500)

    def test_cash_reserve_excluded(self):
        result = self.run_case(cash=2500, reserve=2500)
        self.assertEqual(result.weights, (25, 25, 30, 20))
        self.assertAlmostEqual(sum(result.gaps), 0)

    def test_partial_reserve(self):
        result = self.run_case(cash=2500, reserve=1000)
        self.assertEqual(result.total, 11500)
        self.assertAlmostEqual(sum(result.gaps), 1500)

    def test_invalid_cash_or_weights(self):
        for args in [dict(reserve=1), dict(targets=(25, 25, 30, 21)), dict(quantities=(-1, 1, 1, 1))]:
            with self.subTest(args=args):
                self.assertEqual(self.run_case(**args).state, "DATA_CHECK")

    def test_missing_zero_negative_price(self):
        for p in [float("nan"), 0, -1]:
            self.assertEqual(self.run_case(prices=(100, p, 100, 100)).state, "DATA_CHECK")

    def test_stale_or_mismatched_prices(self):
        self.assertEqual(self.run_case(price_closes=(self.close - timedelta(days=8),) * 4).state, "DATA_CHECK")
        self.assertEqual(self.run_case(price_closes=(self.close,) * 3 + (self.close - timedelta(days=1),)).state, "DATA_CHECK")

    def test_unverified_or_future_holdings(self):
        for args in [dict(unchanged=False), dict(checked_at=None), dict(checked_at=self.now + timedelta(seconds=1)), dict(checked_at=self.now - timedelta(days=8))]:
            self.assertEqual(self.run_case(**args).state, "DATA_CHECK")

    def test_quarter_requires_confirmation_after_close(self):
        checked = self.close - timedelta(hours=1)
        self.assertEqual(self.run_case(checked_at=checked).state, "ON_TRACK")
        self.assertEqual(self.run_case(checked_at=checked, review_due=True).state, "DATA_CHECK")

    def test_initial_and_empty_account(self):
        self.assertEqual(self.run_case(quantities=(0,) * 4, cash=100).state, "INITIAL_ALLOCATION")
        self.assertEqual(self.run_case(quantities=(0,) * 4).state, "DATA_CHECK")

    def test_priority_and_experimental_state(self):
        options = dict(quantities=(31, 19, 30, 20), weekly_flip=True)
        self.assertEqual(self.run_case(**options).state, "EARLY_REVIEW_CANDIDATE")
        self.assertEqual(self.run_case(**options, review_due=True).state, "REBALANCE_REVIEW")
        self.assertEqual(self.run_case(**options, trend_ok=False).state, "DRIFT_WATCH")

    def test_holiday_quarter_and_year_transition(self):
        # Observed sessions: Mar 28 -> Apr 1 (Good Friday closure in 2024).
        self.assertEqual(quarter_day(datetime(2024, 4, 1), datetime(2024, 3, 28), 60), 1)
        self.assertEqual(quarter_day(datetime(2024, 4, 2), datetime(2024, 4, 1), 0), 2)
        self.assertEqual(quarter_day(datetime(2027, 1, 4), datetime(2026, 12, 31), 60), 1)
        self.assertEqual(quarter_key(datetime(2027, 1, 4)), 20271)

    def test_new_york_quarter_not_seoul(self):
        utc = ZoneInfo("UTC")
        ny = ZoneInfo("America/New_York")
        self.assertEqual(quarter_key(datetime(2026, 4, 1, 0, 30, tzinfo=utc).astimezone(ny)), 20261)
        self.assertEqual(datetime(2026, 7, 1, 14, 30, tzinfo=utc).astimezone(ny).hour, 10)
        self.assertEqual(datetime(2027, 1, 4, 15, 30, tzinfo=utc).astimezone(ny).hour, 10)

    def test_alert_dedup_and_data_recovery(self):
        gate = AlertGate()
        args = dict(enabled=True, due=True, realtime=True, confirmed=True)
        self.assertEqual(gate.event(20264, valid=False, **args), "DATA_CHECK")
        self.assertIsNone(gate.event(20264, valid=False, **args))
        self.assertEqual(gate.event(20264, valid=True, **args), "REVIEW")
        self.assertIsNone(gate.event(20264, valid=True, **args))
        self.assertEqual(gate.event(20271, valid=True, **args), "REVIEW")

    def test_no_intrabar_historical_or_early_alerts(self):
        for change in [dict(realtime=False), dict(confirmed=False), dict(due=False), dict(enabled=False)]:
            args = dict(enabled=True, due=True, realtime=True, confirmed=True, valid=True) | change
            self.assertIsNone(AlertGate().event(20264, **args))

    def test_vix_fix_formula_and_warmup(self):
        closes = [100.0] * 80
        lows = [99.0] * 80
        lows[30] = 90.0
        out = vix_fix(closes, lows)
        self.assertIsNone(out[20][0])                      # < 22 closes
        self.assertAlmostEqual(out[30][0], 10.0)           # (100-90)/100*100
        self.assertIsNone(out[60][1])                      # 50-bar range not ready (wvf from bar 21)
        self.assertIsNotNone(out[70][1])

    def test_vix_fix_spike_then_normal(self):
        closes = [100.0 + (i % 3) for i in range(100)]
        lows = [c - 1.0 - 0.3 * (i % 4) for i, c in enumerate(closes)]
        lows[90] = 85.0
        out = vix_fix(closes, lows)
        self.assertTrue(out[90][1])                        # panic-sized drop flagged
        self.assertFalse(out[95][1])                       # ordinary dip right after spike not flagged

    def test_vix_fix_range_high_boundary(self):
        # Last bar exactly at 85% of the 50-bar WVF high must count (>=), like Pine.
        closes = [100.0] * 80
        lows = [99.0 - (i % 2) for i in range(80)]         # WVF alternates 1 / 2
        lows[60] = 80.0                                    # WVF 20 -> range high 17
        lows[79] = 83.0                                    # WVF exactly 17
        only_range = dict(band_mult=100.0)                 # isolate the range-high rule from the Bollinger rule
        out = vix_fix(closes, lows, **only_range)
        self.assertAlmostEqual(out[79][0], 17.0)
        self.assertTrue(out[79][1])
        lows[79] = 83.01
        self.assertFalse(vix_fix(closes, lows, **only_range)[79][1])
        self.assertTrue(vix_fix(closes, lows)[79][1])      # default Bollinger rule still flags it

    def test_vix_fix_calm_regime_limitation(self):
        # Known property of the 50-bar relative threshold: a perfectly calm series is flagged.
        # Documented so the weekly backtest checks false positives; not a desired behavior.
        out = vix_fix([100.0] * 80, [99.0] * 80)
        self.assertTrue(out[79][1])

    def test_interpretation_matrix(self):
        base = dict(data_ok=True, actionable=True, trend_ok=True)
        cases = [
            (-3, 1, False, "상승: 보충 검토 우호"),
            (-3, -1, True, "하락+공포: 1차 분할 보충 검토"),
            (-3, -1, False, "하락: 분할·재확인"),
            (3, -1, True, "하락: 축소 검토 우선"),            # fear never changes the sell side
            (3, 1, True, "상승: 초과분만 검토"),
        ]
        for diff, trend, fear, expected in cases:
            with self.subTest(diff=diff, trend=trend, fear=fear):
                self.assertEqual(interpret(**base, difference=diff, trend=trend, fear=fear), expected)
        self.assertEqual(interpret(**(base | dict(trend_ok=False)), difference=-3, trend=-1, fear=True), "추세 미확인")
        self.assertEqual(interpret(**(base | dict(actionable=False)), difference=-3, trend=-1, fear=True), "추세 하락 참고")

    def test_pine_contract_static_only(self):
        pine = (Path(__file__).resolve().parents[1] / "pine" / "quarterly_etf_review.pine").read_text(encoding="utf-8")
        self.assertTrue(pine.startswith("//@version=6"))
        self.assertEqual(pine.count("request.security("), 8)
        self.assertEqual(pine.count("lookahead = barmerge.lookahead_on"), 8)
        self.assertIn("[close[1], time[1], time_close[1], count[1], endOfQuarter[1]]", pine)
        self.assertIn("[st[1], flipped[1], lastFlip[1], fear[1], wvf[1], time_close[1]]", pine)
        self.assertIn("ta.supertrend(stMultiplier, stLength)", pine)
        self.assertIn("100 * (highestClose - low) / highestClose", pine)
        for label, expected in [("하락+공포: 1차 분할 보충 검토", 1), ("하락: 축소 검토 우선", 1)]:
            self.assertEqual(pine.count(label), expected)
        self.assertNotIn("strategy.entry", pine)
        self.assertNotIn("strategy.order", pine)
        self.assertIn("barstate.isrealtime and barstate.isconfirmed", pine)


if __name__ == "__main__":
    unittest.main()
