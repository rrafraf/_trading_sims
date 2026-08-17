from __future__ import annotations

import csv
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from .common import unavailable_result
from .types import AdapterContext
from ..models import Fill, RunResult


class MuniAdapter:
    name = "muni"

    def __init__(
        self,
        initial_cash: float,
        fee_bps: float = 0.0,
        slippage_bps: float = 0.0,
        enforce_volume: bool = True,
        volume_policy: str | None = None,
        data_quality: str = "warn",
        muni_root: str | None = None,
        node_executable: str | None = None,
        timeout_seconds: int = 60,
        **_kwargs: Any,
    ):
        self.initial_cash = initial_cash
        self.fee_bps = fee_bps
        self.slippage_bps = slippage_bps
        self.volume_policy = volume_policy or ("partial" if enforce_volume else "ignore")
        self.data_quality = data_quality
        self.muni_root = Path(muni_root or os.environ.get("MUNI_ROOT", r"C:\Users\Professional\Documents\muni"))
        self.node_executable = node_executable or os.environ.get("NODE_EXE") or shutil.which("node") or "node"
        self.timeout_seconds = timeout_seconds

    def run(self, context: AdapterContext) -> RunResult:
        cli_path = self.muni_root / "training_ground" / "run-experiment.js"
        if not cli_path.exists():
            return unavailable_result(
                context=context,
                adapter_name=self.name,
                initial_cash=self.initial_cash,
                reason=f"muni CLI not found at {cli_path}",
            )

        with tempfile.TemporaryDirectory(prefix=f"muni-{context.run_id}-") as tmp:
            tmp_path = Path(tmp)
            bars_path = tmp_path / "bars.csv"
            signals_path = tmp_path / "signals.json"
            policy_path = tmp_path / "policy.json"
            result_path = tmp_path / "run-result.json"

            self._write_bars(context, bars_path)
            self._write_signals(context, signals_path)
            self._write_policy(context, policy_path)

            command = [
                self.node_executable,
                str(cli_path),
                "--mode",
                "target-signals",
                "--bars",
                str(bars_path),
                "--signals",
                str(signals_path),
                "--policy",
                str(policy_path),
                "--out",
                str(result_path),
            ]
            try:
                completed = subprocess.run(
                    command,
                    cwd=self.muni_root,
                    text=True,
                    capture_output=True,
                    timeout=self.timeout_seconds,
                    check=False,
                )
            except Exception as exc:
                return unavailable_result(
                    context=context,
                    adapter_name=self.name,
                    initial_cash=self.initial_cash,
                    reason=f"muni CLI failed before completion: {type(exc).__name__}: {exc}",
                )

            if completed.returncode != 0:
                reason = (completed.stderr or completed.stdout or "muni CLI returned non-zero").strip()
                return unavailable_result(
                    context=context,
                    adapter_name=self.name,
                    initial_cash=self.initial_cash,
                    reason=reason,
                )

            payload = json.loads(result_path.read_text(encoding="utf-8"))
            return self._result_from_payload(context, payload)

    def _write_bars(self, context: AdapterContext, path: Path) -> None:
        fieldnames = ["timestamp", "symbol", "open", "high", "low", "close", "volume"]
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for bar in context.bars:
                writer.writerow(
                    {
                        "timestamp": bar.timestamp.isoformat(),
                        "symbol": bar.symbol,
                        "open": bar.open,
                        "high": bar.high,
                        "low": bar.low,
                        "close": bar.close,
                        "volume": bar.volume,
                    }
                )

    def _write_signals(self, context: AdapterContext, path: Path) -> None:
        payload = {
            "run_id": context.run_id,
            "strategy": context.strategy_name,
            "dataset": str(context.dataset),
            "symbol": context.symbol,
            "signals": [
                {
                    "timestamp": signal.timestamp.isoformat(),
                    "symbol": signal.symbol,
                    "target_quantity": signal.target_quantity,
                    "reason": signal.reason,
                }
                for signal in context.signals
            ],
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _write_policy(self, context: AdapterContext, path: Path) -> None:
        payload = {
            "run_id": context.run_id,
            "strategy": context.strategy_name,
            "dataset": str(context.dataset),
            "symbol": context.symbol,
            "initial_cash": self.initial_cash,
            "fee_bps": self.fee_bps,
            "slippage_bps": self.slippage_bps,
            "volume_policy": self.volume_policy,
            "data_quality": self.data_quality,
            "allow_short": True,
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _result_from_payload(self, context: AdapterContext, payload: dict[str, Any]) -> RunResult:
        notes = list(payload.get("notes", []))
        policy_differences = payload.get("policy_differences", [])
        if policy_differences:
            notes.extend(f"policy_difference: {item}" for item in policy_differences)

        fills = [
            Fill(
                timestamp=parse_timestamp(row["timestamp"]),
                symbol=row["symbol"],
                side=row["side"],
                quantity=float(row["quantity"]),
                price=float(row["price"]),
                fee=float(row["fee"]),
                source_signal_timestamp=parse_timestamp(row["source_signal_timestamp"]),
            )
            for row in payload.get("fills", [])
        ]

        return RunResult(
            run_id=payload.get("run_id", context.run_id),
            adapter=self.name,
            strategy=payload.get("strategy", context.strategy_name),
            dataset=payload.get("dataset", str(context.dataset)),
            symbol=payload.get("symbol", context.symbol),
            initial_cash=float(payload.get("initial_cash", self.initial_cash)),
            final_cash=float(payload["final_cash"]),
            final_position=float(payload["final_position"]),
            final_price=float(payload["final_price"]),
            final_equity=float(payload["final_equity"]),
            return_pct=float(payload["return_pct"]),
            fill_count=int(payload["fill_count"]),
            signal_count=int(payload["signal_count"]),
            notes=notes,
            fills=fills,
        )


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
