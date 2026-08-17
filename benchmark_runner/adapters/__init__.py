from __future__ import annotations

from .backtrader_adapter import BacktraderAdapter
from .lean_adapter import LeanAdapter
from .muni_adapter import MuniAdapter
from .own_engine_template import OwnEngineTemplateAdapter
from .pybroker_adapter import PyBrokerAdapter
from .reference_bar import ReferenceBarAdapter
from .vectorbt_adapter import VectorBTAdapter


ADAPTERS = {
    BacktraderAdapter.name: BacktraderAdapter,
    LeanAdapter.name: LeanAdapter,
    MuniAdapter.name: MuniAdapter,
    OwnEngineTemplateAdapter.name: OwnEngineTemplateAdapter,
    PyBrokerAdapter.name: PyBrokerAdapter,
    ReferenceBarAdapter.name: ReferenceBarAdapter,
    VectorBTAdapter.name: VectorBTAdapter,
}
