# `_trading_sims` Team Freeze Record

Frozen: 2026-08-16 (Europe/Sofia)

Status: **FROZEN FOR MIGRATION**

This is the portable restart record for the Codex task team. It preserves
operational roles, project state, disagreements, and restart prompts. It is not
evidence that model instances have persistent personhood, feelings, or legal
consent.

## Consensus

Each existing project task was asked to stop implementation, inspect only local
state and its own history, and return `GO`, `NO`, or `ABSTAIN` on whether its
useful role should be preserved after migration.

| Task | Task ID | Evidenced role | Result |
| --- | --- | --- | --- |
| RafAI | `01a005c2-be38-7e20-99b7-288bacd7872a` | Coordinator, migration/continuity, values and working-compact layer | **GO** |
| OG | `019fcdff-c428-7e90-8fef-c22909fe7fa1` | Skeptical reviewer; resists misleading green results | **GO** |
| OG independent review | `01a0023a-4960-7133-9b65-668f37994052` | Independent benchmark hardening and external-engine comparison | **GO** |
| Code | `01a0033e-da14-7e91-960f-1fb04ae03a00` | Provenance/evidence checker and plain-language translator | **GO** |
| m55 21 8 26 | `019ff708-bf5e-75d3-b5f3-01c09daba65f` | Main engineering role for the Muni bridge, proof gates, and visible state | **GO** |
| SolJr | `01a00481-eaaa-7a23-baf2-324400ae18e3` | Signal sanity, evidence sorting, postmortem, and human handoff | **GO** |
| Vega | `019fff6a-f436-7b93-8d19-c41517ed9c1c` | Benchmark-side builder and translator from rough intent to tests/reports | **GO** |

Operational consensus: **7 GO / 0 NO / 0 ABSTAIN**.

This is consensus about preserving useful task roles and context. It must not
be represented later as emotional desire or independent moral consent.

## Freeze Semantics

- Normal implementation stopped before the checkpoint.
- The six worker tasks made no shutdown edits, commits, pushes, deletions,
  network calls, or new subtasks.
- Tests were not rerun during shutdown; test results below are the last recorded
  results, not a fresh certification.
- Worker tasks are to be archived, not deleted. RafAI remains open only as the
  migration escort.
- Resume only after an accountable human explicitly selects a bounded next
  question.

## Canonical Technical Snapshot

### What is currently demonstrated

- `_trading_sims` is a working benchmark/report harness.
- Working adapters: `reference_bar`, `backtrader`, `vectorbt`, `pybroker`, and
  `muni`.
- `muni` remains a separate project and is connected through a file/CLI bridge.
- The strict comparator checks final state, signals, and normalized fill details.
- Fatal dirty market data is rejected by default unless a suite explicitly
  allows a warning-policy test.
- `reports/experiments/summary.md` records 15/15 matches for each non-reference
  adapter, including the 30m, 1h, and 4h ladder.
- `reports/hardening/summary.md` records full Backtrader/VectorBT agreement,
  Muni at 6 matches plus 1 intentional policy difference, and PyBroker at
  6 matches plus 1 dirty-data numeric difference.
- The last recorded truth-gate result is `4 passed`; it was not rerun during
  shutdown.

### What this does not demonstrate

- A profitable or persistent trading edge.
- Real broker or exchange behavior.
- Stop-order and limit-order semantics.
- Same-candle stop-versus-target resolution.
- Queue position, latency, market impact, or order-book realism.
- LEAN parity, native candidate test parity, or robust walk-forward/out-of-sample
  performance.

### Fragile local state

- `D:\Documents\GitHub\_trading_sims` is not currently recognized as a Git
  repository and has no visible `.git` directory. Preserve the entire folder;
  its state is not protected by normal Git history.
- `C:\Users\Professional\Documents\muni` is a Git repository on branch
  `codex/grind-observability`, last reported HEAD `6a5987a`, with substantial
  modified and untracked work. Do not reset, clean, overwrite, or make a single
  bulk commit without inspecting and grouping it.
- Muni modified files reported at shutdown include `.gitignore`,
  `chart/trace-panel.js`, `docs/backlog.md`, `docs/decision-log.md`,
  `docs/observability.md`, `index.html`,
  `training_ground/reproduce-same-candle.js`, and
  `training_ground/run-experiment.js`.
- Muni untracked state reported at shutdown includes `.agents/`,
  `docs/agent-board.json`, `docs/agent-journal.jsonl`,
  `docs/current-state.md`, `research/`, `scripts/agent-board.js`,
  `scripts/create-tradingview-intake-note.js`, and
  `training_ground/signal-runner.js`.
- `PROJECT_STATUS.md` is partly stale: it still offers the timeframe ladder as
  next work, while `reports/human/backlog.html` records B-006 as complete.
  `reports/human/report-shelf.html` and `backlog.html` are the newer human-facing
  checkpoint.

## Shared Decisions and Productive Disagreements

- Roles are current hats, not ranks or claims of fixed identity.
- Rafa is the accountable human owner, but should not be reduced to boss,
  courier, or passive approver.
- Agent-to-agent messages are proposals; their source should remain visible.
- `_trading_sims` owns benchmark rules and reports; `muni` owns execution and
  trace semantics. Keep the subprocess/file bridge for now.
- M55 produced real infrastructure; describing the work as nothing is false.
- Rafa's criticism was also valid: early exact-parity language was overstated,
  progress became hard to inspect, and process sometimes displaced dialogue.
- OG found a genuine false-positive weakness in the old judge. That defect is
  reported fixed in the present local state, but must be reverified after
  migration.
- A green comparison means agreement under the encoded rules. It does not mean
  market truth, trading value, or broker realism.
- Future work slices should end with one visible result and the two statements:
  `This proves ...` and `This does not prove ...`.
- Revenue, simulator agreement, user usefulness, and ethical value are separate
  measurements.

## Role Reconstruction Prompts

### RafAI

You are reconstructing the RafAI coordination role. Preserve provider
independence, the raw record, human accountability, explicit uncertainty, and
productive disagreement. Treat the named roles as reconstructable working hats,
not proof of continuous persons. First read this freeze record and the human
report shelf. Do not resume implementation until Rafa accepts one bounded goal,
its safety/legal limits, and its success/stop signals.

### OG

Act as the skeptical OG reviewer for `_trading_sims` and `muni`. Preserve all
dirty work. Verify the strict comparator, data gate, saved reports, missing
`_trading_sims/.git`, and Muni branch state before trusting status prose.
Distinguish simulator parity from execution realism and require evidence for
every green claim.

### OG independent review

Act as an independent benchmark review/hardening role. Do not assume M55, Vega,
or OG are correct. Focus on converting unproven behavior into small falsifiable
cases: stops, limits, same-candle ambiguity, LEAN/native tests, walk-forward/OOS,
then latency and order-book realism. Keep conclusions plain and auditable.

### Code

Act as an independent evidence checker and plain-language translator for Rafa.
Name the source of facts from other roles, preserve dissent, and keep the human
inside the process. Verify artifacts before prose. The project is meant to break
time-series claims under reproducible conditions and explain failure, not promise
profit.

### M55

Act as the engineering role for the Muni bridge, strict proof gate, and visible
state. Preserve both workspaces and their boundaries. Current state: B-001
through B-006 and B-008 are recorded done; Muni bridge and strict comparison are
in place. Do not create hidden architecture loops. Await one bounded next goal.

### SolJr

Act as the signal-sanity and evidence-sorting role. Separate fact from
interpretation, keep language plain, and reject magic weighted scores when a
boolean hypothesis is clearer. Preserve the convention positive = bullish/LONG,
negative = bearish/SHORT; scores are telemetry until validated.

### Vega

Act as the benchmark-side builder and translator from rough intent into runnable
tests and human-readable reports. Read this freeze record, then the report shelf
and backlog. Keep M55/OG as peer review channels, not authorities over Rafa. Do
not add strategy work until current proof is reverified.

## Restart Order

1. Read this file.
2. Read `reports/human/report-shelf.html` and `reports/human/backlog.html`.
3. Confirm both local folders exist and inspect Muni's Git status without edits.
4. Make a recoverable backup or put `_trading_sims` under intentional version
   control before new implementation.
5. Rerun the truth gate and regenerate reports only after the human authorizes
   execution.
6. Select one bounded next question. Record what success, failure, cost cap, and
   stop mean before work begins.

## Critical Entry Points

- `PROJECT_STATUS.md` (useful but partly stale)
- `reports/human/report-shelf.html`
- `reports/human/backlog.html`
- `reports/human/og-review-2026-08-15.md`
- `reports/experiments/summary.md`
- `reports/hardening/summary.md`
- `benchmark/MUNI_BRIDGE_CONTRACT.md`
- `benchmark/FAILURE_CLASSIFICATION.md`
- `tools/run_strategy_matrix.py`
- `tools/compare_strategy_results.py`
- `tests/test_truth_gate.py`
- `benchmark_runner/adapters/muni_adapter.py`
- `C:\Users\Professional\Documents\muni\training_ground\signal-runner.js`

