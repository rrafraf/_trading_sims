from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from tools.compare_strategy_results import compare
from tools.run_strategy_matrix import run_suite


def result_row(
    adapter: str,
    *,
    final_cash: float = 1000.0,
    final_position: float = 10.0,
    final_price: float = 10.0,
    final_equity: float = 1100.0,
    fill_side: str = "buy",
    fill_quantity: float = 10.0,
    fill_price: float = 10.0,
    fill_fee: float = 1.0,
) -> dict:
    return {
        "run_id": "r1",
        "adapter": adapter,
        "strategy": "scheduled_targets",
        "dataset": "fixture.csv",
        "symbol": "SIM",
        "initial_cash": 1000.0,
        "final_cash": final_cash,
        "final_position": final_position,
        "final_price": final_price,
        "final_equity": final_equity,
        "return_pct": 10.0,
        "fill_count": 1,
        "signal_count": 1,
        "notes": [],
        "fills": [
            {
                "timestamp": "2024-01-01T00:01:00+00:00",
                "symbol": "SIM",
                "side": fill_side,
                "quantity": fill_quantity,
                "price": fill_price,
                "fee": fill_fee,
                "source_signal_timestamp": "2024-01-01T00:00:00+00:00",
            }
        ],
    }


class TruthGateTests(unittest.TestCase):
    def test_opposite_position_and_fill_are_not_a_match(self) -> None:
        baseline = result_row("reference_bar")
        candidate = result_row(
            "candidate",
            final_cash=1200.0,
            final_position=-10.0,
            final_equity=1100.0,
            fill_side="sell",
            fill_quantity=10.0,
        )

        rows = compare([baseline, candidate], baseline_adapter="reference_bar", numeric_tolerance=1e-9)
        candidate_row = next(row for row in rows if row["adapter"] == "candidate")

        self.assertEqual(candidate_row["status"], "diff")
        self.assertIn("final_cash", candidate_row["mismatches"])
        self.assertIn("final_position", candidate_row["mismatches"])
        self.assertIn("fill[0].side", candidate_row["mismatches"])

    def test_fill_price_and_fee_differences_are_not_a_match(self) -> None:
        baseline = result_row("reference_bar")
        candidate = result_row("candidate", fill_price=10.01, fill_fee=1.25)

        rows = compare([baseline, candidate], baseline_adapter="reference_bar", numeric_tolerance=1e-9)
        candidate_row = next(row for row in rows if row["adapter"] == "candidate")

        self.assertEqual(candidate_row["status"], "diff")
        self.assertIn("fill[0].price", candidate_row["mismatches"])
        self.assertIn("fill[0].fee", candidate_row["mismatches"])

    def test_policy_difference_is_not_called_a_clean_match(self) -> None:
        baseline = result_row("reference_bar")
        candidate = result_row("candidate")
        candidate["notes"] = ["policy_difference: P0_DATA_INVALID"]

        rows = compare([baseline, candidate], baseline_adapter="reference_bar", numeric_tolerance=1e-9)
        candidate_row = next(row for row in rows if row["adapter"] == "candidate")

        self.assertEqual(candidate_row["status"], "policy_diff")
        self.assertEqual(candidate_row["mismatches"], "")

    def test_dirty_data_rejects_before_strategy_generation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dataset = Path(tmp) / "bad.csv"
            with dataset.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["timestamp", "symbol", "open", "high", "low", "close", "volume"],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "timestamp": "2024-01-01T00:00:00+00:00",
                        "symbol": "SIM",
                        "open": "10",
                        "high": "10",
                        "low": "10",
                        "close": "10",
                        "volume": "100",
                    }
                )
                writer.writerow(
                    {
                        "timestamp": "2024-01-01T00:00:00+00:00",
                        "symbol": "SIM",
                        "open": "10",
                        "high": "9",
                        "low": "10",
                        "close": "10",
                        "volume": "100",
                    }
                )

            suite = {
                "data_quality": "reject",
                "adapters": {"reference_bar": {"initial_cash": 1000}},
                "runs": [
                    {
                        "id": "bad",
                        "dataset": str(dataset),
                        "symbol": "SIM",
                        "strategy": "buy_hold",
                        "quantity": 10,
                        "params": {"start_index": 0},
                    }
                ],
            }

            with self.assertRaisesRegex(ValueError, "rejected dirty bars before strategy generation"):
                run_suite(suite, adapter_names=["reference_bar"])


if __name__ == "__main__":
    unittest.main()
