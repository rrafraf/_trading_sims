# Research map — latent market representation

> Post-freeze research note. These references are not claims that the exact product already exists; they are adjacent work showing useful pieces of the design space.

## 1. TS2Vec — timestamp-level time-series representations

**Paper:** *TS2Vec: Towards Universal Representation of Time Series* — Yue et al., AAAI 2022.

- Learns contextual representations for each timestamp using hierarchical contrastive learning.
- Supports arbitrary subsequence representations by aggregating timestamp representations.
- Demonstrates usefulness for forecasting and anomaly detection in addition to classification.
- Relevant because our first question is whether causal windows can be mapped into a useful geometry before any trading policy is added.

Paper: https://arxiv.org/abs/2106.10466

Official code: https://github.com/zhihanyue/ts2vec

## 2. MASTER — market-guided cross-stock representation

**Paper:** *MASTER: Market-Guided Stock Transformer for Stock Price Forecasting* — Li et al., 2023.

- Explicitly models relationships across stocks instead of treating each symbol independently.
- Motivated by correlations that can be momentary, cross-time, and dependent on changing market conditions.
- Uses market information for dynamic feature selection.
- Relevant because our proposed state is multi-asset: `X[time, asset, feature]`, not merely one ticker encoded alone.

Paper: https://arxiv.org/abs/2312.15235

## 3. MF-CLR — multi-frequency self-supervised representations

**Paper:** *MF-CLR: Multi-Frequency Contrastive Learning Representation for Time Series* — Duan et al., ICML 2024.

- Self-supervised contrastive representation learning for time series whose channels/features arrive at different frequencies.
- Motivation explicitly includes financial data with daily/monthly/quarterly variables.
- Relevant later if the market state expands beyond minute bars to heterogeneous data frequencies.

Paper: https://proceedings.mlr.press/v235/duan24b.html

## 4. Multi-Patch Prediction / aLLM4TS — predictive representations rather than only reconstruction

**Paper:** *Multi-Patch Prediction: Adapting Language Models for Time Series Representation Learning* — Bian et al., ICML 2024.

- Reframes time-series learning around causal next/multi-patch prediction.
- Interesting for our hypothesis that a market representation should preserve information useful for the future, not merely reconstruct the past.

Paper: https://proceedings.mlr.press/v235/bian24a.html

## 5. TimeSiam — explicitly learning temporal relation between past and current subseries

**Paper:** *TimeSiam: A Pre-Training Framework for Siamese Time-Series Modeling* — Dong et al., ICML 2024.

- Learns temporal correlations using past/current subseries pairs and temporal-distance information.
- Relevant as another self-supervised objective to compare against TS2Vec-like contrastive learning and direct future prediction.

Paper: https://proceedings.mlr.press/v235/dong24e.html

## 6. Time2Vec — learned representation of time itself

**Paper:** *Time2Vec: Learning a Vector Representation of Time* — Kazemi et al., 2019.

- Provides a learnable vector representation of periodic/non-periodic temporal structure.
- Relevant because market time is not just an integer index: intraday/session/week/calendar effects may matter, and we need to encode them without accidentally leaking the future.

Paper: https://arxiv.org/abs/1907.05321

## 7. Survey / map of the broader representation-learning space

**Survey:** *Universal Time-Series Representation Learning: A Survey* — Trirat et al., 2024.

- Useful taxonomy of representation-learning objectives and architectures.
- Good source for selecting baseline families rather than inventing every experiment from scratch.

Paper: https://arxiv.org/abs/2401.03717

Companion resource: https://github.com/itouchz/awesome-deep-time-series-representations

---

## Adjacent conceptual connection: latent reasoning

This is not a finance paper, but it helped trigger the design discussion.

**Paper:** *Training Large Language Models to Reason in a Continuous Latent Space* (Coconut) — Hao et al., 2024.

The work explores feeding continuous hidden states forward rather than forcing every reasoning step through discrete language tokens. The conceptual connection here is not that we should apply Coconut directly to markets; it is the broader idea that useful structure need not first be projected into a human-named symbolic vocabulary.

Paper: https://arxiv.org/abs/2412.06769

---

## Our open gap

The product hypothesis is deliberately more specific than "learn a good time-series embedding":

> Build a causal multi-asset latent geometry and directly test whether neighbourhood similarity predicts similarity of **future outcome distributions** on genuinely unseen future data.

That test should be run before optimizing a trading strategy.

The first useful contribution may therefore be less a novel neural architecture and more a rigorous experimental harness joining:

```text
causal market tensor
       -> encoder
       -> latent geometry
       -> historical episodic neighbours
       -> multi-horizon conditional future distributions
       -> leakage-audited out-of-sample evaluation
```

If that geometry survives, it becomes the substrate for the later simulated-trading and multi-agent layers.
