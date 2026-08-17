# Repo Integration Options

## Option A: Keep Repos Separate First

Best first move.

Pros:

- no risky merge
- preserves existing engine history
- this harness can import the engine by path or package
- easier for the engine dev to continue working independently

Cons:

- path/package setup needs care
- CI must know where both repos live

Use this until the adapter contract is stable.

## Option B: Mono-Repo

Pros:

- one workspace
- easier shared tests
- easier dashboards/UI later

Cons:

- harder merge
- can muddy ownership boundaries
- risks pulling experimental harness churn into engine code

Use only after we know the shared adapter contract is right.

## Option C: Vendor The Engine Core

Pros:

- harness can run without external checkout
- reproducible experiments

Cons:

- duplicated code
- update drift
- unclear ownership

Use only for a frozen benchmark snapshot, not active engine development.

## Recommendation

Start with Option A. Add an adapter that points to the in-house engine from its
current repo. Use the reports as the shared decision record. Revisit mono-repo
only after the adapter survives baseline and stress scenarios.

