# 03a · Generating Synthetic Weather & Price Paths

**Notebook:** [`generate-synthetic-data.ipynb`](generate-synthetic-data.ipynb)

## What this notebook does

It is the **stochastic engine** of the portfolio. It fits probabilistic models to the
historical solar and price data, then simulates **1,000 plausible 30-year futures** for
the two variables that drive a solar plant's revenue, exporting them to the
`data/PV_SYNTHETIC_DATA/` bundle for the Monte Carlo model in `pv-markov-model.ipynb`.

## The two stochastic models

### Solar resource — Markov chain + Beta distributions

Daily weather is **persistent** (a cloudy day tends to follow a cloudy day), so a plain
i.i.d. draw from the historical Clear-Sky Index (CSI) histogram would understate runs of
bad weather. Instead the daily CSI is modelled as a **Markov-modulated Beta process**:

- The continuous CSI is discretised into **3 regimes** — `[0, 0.6)` overcast,
  `[0.6, 0.9)` intermediate, `[0.9, 1.0]` clear.
- A **3×3 transition matrix** `P[i,j] = P(tomorrow = j | today = i)` is estimated by
  counting consecutive-day transitions in the historical record. Its diagonal dominance
  encodes weather persistence.
- Within each regime a **Beta distribution** is fitted (rescaled to the regime's bounds),
  capturing the spread of CSI values in that state.

Simulating a path = walking the Markov chain to get a state sequence, then drawing each
day's CSI from that state's Beta distribution. This reproduces both the *persistence*
and the *shape* of the real CSI.

### Electricity price — Gaussian KDE

Daily daytime merchant prices are sampled from a non-parametric **Gaussian kernel density
estimate** fitted to recent history. Prices are cleaned first:

- **Sunny hours only** (`07:00–17:00`) — a solar plant only earns in daylight.
- **2024 onward only** — excludes the 2022 energy-crisis spike and abnormally low
  pre-COVID prices that would bias the distribution.
- **Daily mean** — one average daytime price per day.

## Pipeline

1. Load the merged solar dataset from notebook `02` and compute the daily CSI.
2. Fit the 3-state Markov chain + per-state Beta distributions.
3. Load and clean ESIOS prices, fit the price KDE.
4. Generate a deterministic 30-year clear-sky backbone (2027+).
5. Run 1,000 Monte Carlo simulations: Markov-walk the CSI, KDE-sample the price.
6. Export all paths to the `data/PV_SYNTHETIC_DATA/` bundle (see layout below).
7. **Validate** — overlay synthetic vs. historical distributions for CSI and price.

## Output layout

A single JSON holding all 1,000 simulations inline would be **~1 GB**, exceeding GitHub's
100 MB per-file limit. The data is therefore written as a directory bundle — one small
CSV per simulation plus a lightweight metadata JSON:

```
data/PV_SYNTHETIC_DATA/
    PV_SYNTHETIC_DATA.json      # parameters (location, horizon, Markov/Beta fits,
                                # transition matrix) + relative path of every simulation
    simulations/
        simulation_0000.csv     # one Monte Carlo path each
        simulation_0001.csv
        ...
```

The fitted transition matrix, per-state Beta parameters, and validation histograms are
also produced in-notebook.

## How to run

Run top to bottom. Depends on `pvlib`, `scipy.stats` (`beta`, `gaussian_kde`), `pandas`,
`numpy`, `plotly` and the local `utils/`. Requires the CSV produced by notebook `02`.
Generating the 1,000 paths is the main compute cost; the `PV_SYNTHETIC_DATA/` bundle it
writes is what `pv-markov-model.ipynb` consumes.
