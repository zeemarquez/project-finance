# 02 · Building the Solar Resource Dataset

**Notebook:** [`pv_data.ipynb`](pv_data.ipynb)

## What this notebook does

It assembles the real-world **solar resource dataset** that the stochastic model in
notebook `03` is calibrated on. The target location is in southern Spain
(lat `38.81`, lon `−6.52`, near Badajoz), covering **2015–2026** at hourly resolution.

The central concept is to split solar irradiance into a **deterministic** component and
a **random** component:

| Component | Source | Nature |
|---|---|---|
| **Clear-sky irradiance** | `pvlib` (astronomy) | Deterministic — the irradiance on a perfectly clear day, fixed by location and time. |
| **Measured irradiance** | NASA POWER API | Actual irradiance, attenuated by clouds/weather. |

Their ratio is the **Clear-Sky Index (CSI)**:

```
CSI = (GHI_measured + ε) / (GHI_clearsky + ε)      (clipped to [0, 1])
```

The CSI removes the predictable seasonal and diurnal cycle, leaving a normalised measure
of **weather randomness** — the quantity modelled stochastically in notebook `03`.

## Pipeline

1. **Clear-sky reference** — `pvlib.Location.get_clearsky` produces GHI/DNI/DHI for every
   hour. A higher-fidelity pass computes clear-sky at 5-minute resolution and resamples
   to hourly means, aligned to NASA's hour-ending timestamps.
2. **Measured data** — `fetch_nasa_power_data` pulls NASA POWER GHI, DNI and cloud cover
   for the same coordinates/period. The `-999` missing-data sentinel is filtered out.
3. **Merge & export** — the two series are joined with `merge_asof` and written to
   `data/PV_DATA_<lat>_<lon>_<range>.csv`.
4. **CSI derivation (exploratory)** — several CSI formulations are tried and visually
   sanity-checked against cloud cover, because the naïve ratio is numerically unstable
   near sunrise/sunset where both irradiances approach zero.
5. **Daily aggregation & distribution** — irradiance is summed to daily totals, the daily
   CSI is computed, and its distribution is examined overall and by month.

## Key findings surfaced

- The CSI distribution is **strongly left-skewed toward 1.0** — most days at this site
  are clear.
- There is clear **seasonal structure** — winter months carry a fatter low-CSI tail.

These two properties (distribution shape + day-to-day persistence) motivate the
Markov-chain + Beta-distribution model fitted in notebook `03`.

## Outputs

- `data/PV_DATA_<lat>_<lon>_<range>.csv` — the merged hourly dataset (the deliverable).
- Diagnostic charts: GHI/CSI/cloud overlays, daily CSI time series, and CSI histograms
  (overall and per-month).

## Notes

- This notebook is partly **exploratory**: it tests multiple CSI definitions. The one
  carried into notebook `03` is the daily-aggregated `(GHI + 0.5)/(GHI_cs + 0.5)` form.
- Depends on a `nasa_power` helper module (`fetch_nasa_power_data`) and `pvlib`,
  `pandas`, `numpy`, `plotly`, plus the local `utils/` Plotly theme. Fetching NASA POWER
  data requires network access.

## How to run

Run top to bottom. The export cell regenerates the CSV consumed by notebook `03`.
