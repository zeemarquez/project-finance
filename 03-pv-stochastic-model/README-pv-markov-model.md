# 03b · Monte Carlo Project Finance Model

**Notebook:** [`pv-markov-model.ipynb`](pv-markov-model.ipynb)

## What this notebook does

It is the **payoff** of the series. It runs the same project finance model from notebook
`01` across the **1,000 synthetic weather-and-price futures** generated in
`generate-synthetic-data.ipynb`, turning a single deterministic IRR into a full
**probability distribution of equity returns**.

## How it differs from notebook 01

The model logic is unchanged. The only difference is that two inputs become
**time-varying arrays** instead of scalars:

- `net_equivalent_hours` — per-year production, derived from each simulation's stochastic
  solar resource.
- `merchant_price` — per-year merchant price, from each simulation's stochastic price path.

The corresponding rows index them by period (`...[t]`), so each model year sees that
simulation's specific resource and price. The cash waterfall, DSCR-sculpted debt, the
circular interest loop and the iterative solver are all identical to notebook `01`.

## Pipeline

1. **Import** the synthetic bundle: read `data/PV_SYNTHETIC_DATA/PV_SYNTHETIC_DATA.json`
   for parameters and the list of simulation files, then load the CSVs it points to.
2. **Transform** each path: reconstruct `ghi = clearsky_ghi × csi`, resample to annual
   (sum irradiance, average price).
3. **Convert** annual GHI to **net equivalent full-load hours** using a transposition
   factor (1.3) and performance ratio (0.8): `net_eq_hours ≈ (GHI/1000) × 1.3 × 0.8`.
4. **Run** all 1,000 input sets through the full circular model via the `Scenarios`
   helper, recording each path's IRR and cash-on-cash multiple.
5. **Analyse** the resulting return distribution.

## Outputs

- A scatter of **IRR vs. lifetime equivalent hours** (the probabilistic analogue of
  notebook `01`'s deterministic sensitivity curve).
- The headline **IRR histogram** — the full probability distribution of equity returns.
  Its centre is the expected return; its left tail quantifies downside risk (e.g. the
  probability of underperforming a hurdle rate).

## Why it matters

This is the deliverable the whole portfolio builds toward: real resource/price data
(notebook `02`) → fitted stochastic models (`03a`) → Monte Carlo through a full project
finance model (`03b`). Instead of "the IRR is X%", it supports a risk statement —
"the IRR is distributed like *this*, with this much downside" — which is what lenders and
investment committees actually need.

## How to run

Run top to bottom. Requires the `data/PV_SYNTHETIC_DATA/` bundle from
`generate-synthetic-data.ipynb`, plus `finmodel`, `pandas`, `numpy`,
`numpy_financial`, `plotly` and the local `utils/`. The 1,000-scenario solve is the main
compute cost (~1 minute).
