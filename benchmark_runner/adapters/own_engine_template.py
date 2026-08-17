from __future__ import annotations

from .common import unavailable_result
from .types import AdapterContext


class OwnEngineTemplateAdapter:
    """Template adapter for plugging in the in-house simulator.

    Copy this file to `own_engine_adapter.py`, point it at the in-house engine,
    and replace `run` with a real translation:

    - context.bars: canonical OHLCV bars
    - context.signals: shared strategy target-position signals
    - context.data_notes: data validation findings
    - return value: normalized RunResult with fills
    """

    name = "own_engine_template"

    def __init__(self, initial_cash: float, **_kwargs):
        self.initial_cash = initial_cash

    def run(self, context: AdapterContext):
        return unavailable_result(
            context=context,
            adapter_name=self.name,
            initial_cash=self.initial_cash,
            reason="template only; copy to own_engine_adapter.py and wire to the in-house engine",
        )

