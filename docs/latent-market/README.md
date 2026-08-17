# Latent Market — product snapshot

> Post-freeze design note. Created after the Codex team freeze. Do **not** treat this branch as evidence of pre-freeze team state.

## Core idea

Stop treating human-designed indicators as the primary ontology of the market.

Represent a causal window of raw/mildly processed multi-asset market data as a learned latent state:

```text
market history X[t-L:t, asset, feature]
            |
            v
         encoder
            |
            v
          Z(t)
```

`Z(t)` should encode the market configuration at time `t` without requiring labels such as RSI, MACD, breakout, squeeze, trend, or regime.

Indicators may later be added as optional sensors, but they are not the worldview.

## Product hypothesis

If two causal market windows map to nearby latent states, then their **future outcome distributions** should also be similar out-of-sample.

Formally, the first thing to test is not whether a strategy makes money. It is whether:

```text
distance(Za, Zb) small
```

implies approximately:

```text
future_distribution(a) ~= future_distribution(b)
```

for horizons relevant to the project: roughly 15 minutes to 4 hours.

If that relationship does not survive strict out-of-sample testing, the representation is not useful enough yet for trading.

## Why this is different from the indicator scanner

The earlier scanner asks which hand-designed transforms/combinations work best.

This product asks a prior question:

> Can the market itself be mapped into a useful geometry, such that similar market states have measurably similar futures?

A successful representation could later support:

- nearest-neighbour / episodic market memory;
- conditional outcome distributions;
- regime discovery without hand labels;
- cross-asset state comparison;
- action-conditioned historical lookup;
- policy learning or simulated trading on top of the latent state;
- visualization of market-state geometry for humans.

## Minimal data model

Start with simple causal features, per asset and time step:

- returns / price change;
- volume;
- high/low/range;
- trade count if available;
- bid/ask spread if available;
- explicit time-of-day / session information.

Potential shape:

```text
X: [time, asset, feature]
Z: [latent_dim]
```

Do not begin by maximizing feature count. The first experiment should prove whether useful geometry exists at all.

## Training objectives worth comparing

Do not assume reconstruction is enough. A representation can reconstruct prices beautifully while preserving mostly irrelevant information.

Compare objectives such as:

1. self-supervised contrastive representation learning;
2. next-patch / future-window prediction;
3. multi-horizon future distribution prediction;
4. cross-asset predictive objectives;
5. hybrid objectives that preserve current state while rewarding future relevance.

A particularly useful product-facing target is a multi-horizon distribution head:

```text
                 Z(t)
             /    |    \
          15m    1h     4h
           |      |      |
       future outcome distributions
```

Possible outputs include:

- return quantiles / bins;
- probability of moves greater than +/-x;
- future volatility;
- maximum favourable excursion;
- maximum adverse excursion;
- cross-asset movement summaries.

## Episodic market memory

Store historical episodes as:

```text
(Z_t, action, future_outcome)
```

At runtime:

```text
current market -> Z_now
                   |
                   v
          nearest historical states
                   |
                   v
       conditional outcome distribution
```

This replaces rules like `RSI > 70 => sell` with evidence such as:

> States geometrically close to the present state historically produced this distribution of outcomes under this action/horizon.

## Non-negotiable experimental rules

- strict causality: no feature/window/normalization may depend on future observations;
- walk-forward or otherwise time-respecting evaluation;
- no random train/test split across time;
- universe membership and delistings must not leak future knowledge;
- hyperparameter selection must not inspect the final holdout period;
- profitable backtests are not evidence until leakage checks pass;
- first milestone is representation validity, **not P&L**.

## Product stages

### V0 — Representation probe

Learn `Z(t)` and test whether latent proximity predicts similarity of future distributions on held-out future periods.

### V1 — Market memory

Build a searchable store of `(Z, future outcomes)` and return calibrated distributions for new states.

### V2 — Simulated actions

Add action-conditioned outcomes and simulated trades. Compare latent-state policies against simple baselines and existing indicator strategies.

### V3 — Human projection

Project latent state into a visual map: neighbourhoods, transitions, uncertainty, historical analogues, and why the current state is unusual.

### V4 — Multi-agent research surface

Allow agents to inspect the same latent market state and propose competing hypotheses/policies while keeping their conclusions separable and auditable.

## Success criterion for Experiment 001

The representation earns the right to continue only if, on strictly unseen future data, neighbourhoods in latent space show statistically meaningful stability in subsequent outcome distributions beyond trivial baselines such as recent return, volatility, asset identity, and time-of-day.

See `experiment-001.md` for the falsifiable first test and `research-map.md` for relevant prior work.
