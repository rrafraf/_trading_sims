from __future__ import annotations

import shutil

from .common import unavailable_result
from .types import AdapterContext


class LeanAdapter:
    name = "lean"

    def __init__(self, initial_cash: float, **_kwargs):
        self.initial_cash = initial_cash

    def run(self, context: AdapterContext):
        dotnet = shutil.which("dotnet")
        if dotnet is None:
            return unavailable_result(
                context=context,
                adapter_name=self.name,
                initial_cash=self.initial_cash,
                reason="dotnet is not on PATH; LEAN requires a native .NET runner",
            )

        return unavailable_result(
            context=context,
            adapter_name=self.name,
            initial_cash=self.initial_cash,
            reason=(
                "LEAN adapter slot is present, but v1 has not generated a LEAN algorithm "
                "project/config from AdapterContext yet"
            ),
            extra_notes=[
                "LEAN is still a first-wave target because it has the strongest all-around broker/order model surface.",
                "Next implementation step: generate a minimal C#/Python LEAN algorithm that reads canonical CSV bars and emits normalized fills.",
            ],
        )

