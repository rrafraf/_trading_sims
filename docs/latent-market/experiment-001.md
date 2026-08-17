# Experiment 001 — Does latent proximity predict similar futures?

## Question

Can a learned representation of causal multi-asset market history produce a geometry in which nearby states have similar future outcome distributions on unseen future periods?

This experiment deliberately avoids optimizing a trading strategy.

## Dataset

Start small enough to audit completely.

Example universe:

- 10–50 liquid assets;
- one consistent market/data source;
- minute bars initially;
- enough history to create separate train, validation, and untouched future holdout periods.

Input window example:

```text
L = 240 minutes
X_t = observations from t-239 ... t
```

Candidate raw features per asset:

```text
log return
range / OHLC-derived movement
volume change / normalized volume
trade count (if available)
spread (if available)
time-of-day/session encoding
```

All normalization parameters must be fit using past/training information only.

## Representation candidates

Compare at least:

### Baseline A — hand state

A small vector of obvious statistics: recent returns, realized volatility, volume, asset/time identifiers.

### Baseline B — PCA / simple dimensional reduction

A deliberately boring learned geometry.

### Model C — contrastive time-series encoder

TS2Vec-like hierarchical contextual representation.

### Model D — predictive encoder

Encode the causal window while training toward future patches or multi-horizon future distributions.

Do not assume the most complex model wins.

## Future outcome vector

For each timestamp `t`, define outcomes that occur strictly after the input boundary.

Example horizons:

```text
15m
30m
60m
120m
240m
```

For each horizon collect values such as:

```text
forward return
future realized volatility
maximum favourable excursion
maximum adverse excursion
```

The outcome representation can be continuous, quantile-binned, or distributional.

## Primary test

For every holdout state `Z_t`:

1. find its `k` nearest historical states using only permitted past/reference data;
2. retrieve the neighbours' future outcome vectors;
3. construct an empirical conditional distribution;
4. compare that distribution with the realized future at `t`;
5. aggregate calibration / likelihood / distance metrics across the holdout period.

Compare against trivial neighbourhoods built from Baseline A and B.

## Secondary geometry test

Take pairs of states `(i, j)` and measure:

```text
D_z(i,j) = distance in learned latent space
D_y(i,j) = distance between subsequent future outcome distributions/vectors
```

Test whether smaller `D_z` is associated with smaller `D_y` out-of-sample.

This is the core claim. If it fails, stop pretending that the latent geometry is market-relevant.

## Leakage audit

Before interpreting any result, mechanically verify:

- every input timestamp precedes every outcome timestamp;
- scalers/normalizers were not fit on validation/holdout data;
- neighbouring examples never include future rows relative to the query when running historical/paper simulation;
- symbol/universe selection was known at the historical time being simulated;
- no rolling indicator accidentally uses centered windows;
- missing-data filling never backfills from the future;
- model selection never sees final holdout scores.

A suspiciously strong result should trigger a leakage investigation before celebration.

## Evaluation outputs

Produce:

```text
artifacts/
  config.json
  split-manifest.json
  leakage-audit.json
  latent-neighbour-metrics.csv
  calibration.csv
  baseline-comparison.csv
  latent-map-sample.parquet
  report.md
```

Minimum report questions:

1. Does latent proximity predict future similarity better than trivial market-state features?
2. Which horizons preserve the effect?
3. Does the effect survive regime/time splits?
4. Are results dominated by asset identity or volatility level?
5. How stable are neighbour sets under small perturbations?
6. Does predictive training outperform pure reconstruction/contrastive training?

## Go / no-go

### GO

Proceed to Market Memory V1 if at least one representation shows a repeatable, leakage-audited out-of-sample relationship between latent proximity and future-outcome similarity that materially beats simple baselines.

### NO-GO / ITERATE

If not, alter the objective/data representation and repeat. Do **not** jump to reinforcement learning, agent swarms, or increasingly elaborate trading rules to hide a representation that has not demonstrated predictive structure.
