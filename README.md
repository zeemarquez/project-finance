# Project Finance Showcase

A portfolio of Jupyter notebooks demonstrating **project finance modelling**, **stochastic
methods**, and **Monte Carlo simulation** applied to a utility-scale solar PV investment.

The notebooks build on each other, going from a classic deterministic model to a
data-driven probabilistic risk analysis of equity returns.

## The story across the notebooks

| # | Notebook | What it does |
|---|---|---|
| **01** | [`01-pv-model-scenarios/`](01-pv-model-scenarios/) | A full three-statement, cash-flow-waterfall **project finance model** of a 10 MW solar plant, with DSCR-sculpted debt and a deterministic resource sensitivity sweep. |
| **02** | [`02-pv-data/`](02-pv-data/) | Builds the real-world **solar resource dataset** — clear-sky (theoretical) vs. NASA-measured irradiance — and derives the **Clear-Sky Index**, the key weather-randomness variable. |
| **03a** | [`03-pv-stochastic-model/generate-synthetic-data.ipynb`](03-pv-stochastic-model/) | Fits a **Markov chain + Beta** model to the solar resource and a **KDE** to electricity prices, then simulates **1,000 synthetic 30-year futures**. |
| **03b** | [`03-pv-stochastic-model/pv-markov-model.ipynb`](03-pv-stochastic-model/) | Runs the notebook-01 model across all 1,000 simulated futures — a **Monte Carlo** producing the full **probability distribution of equity IRR**. |

Each folder contains its own `README` with a detailed overview, and every notebook is
annotated with markdown cells explaining the method step by step.

## The narrative arc

1. **Deterministic baseline** (01) — one model, one answer, plus one-at-a-time sensitivity.
2. **Real data** (02) — separate the predictable (astronomical) part of sunlight from the
   random (weather) part.
3. **Stochastic model** (03a) — capture the *shape* and *persistence* of that randomness,
   and of merchant prices, in fitted probability models.
4. **Monte Carlo** (03b) — propagate that uncertainty through the financial model to get a
   distribution of returns, not a point estimate — the basis for a real risk assessment.

## Tech stack

- **[`finmodel`](https://github.com/zeemarquez/finmodel)** — a formula-driven financial
  modelling library (spreadsheet-style `@row` formulas, lazy evaluation, iterative calc
  for circular references, styled output).
- **`pvlib`** — clear-sky solar irradiance modelling.
- **NASA POWER** / **ESIOS** — measured irradiance and Spanish electricity price data.
- **`scipy.stats`** — Beta fits and Gaussian KDE.
- **`numpy` / `numpy_financial` / `pandas`** — numerics and IRR.
- **`plotly`** — charts (custom dark theme in each `utils/`).

## Installation & setup

**Prerequisites:** [Python 3.11+](https://www.python.org/downloads/) (developed on 3.14)
and [git](https://git-scm.com/).

### 1. Clone the repository

```bash
git clone https://github.com/zeemarquez/project-finance.git
cd project-finance
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 3. Install the dependencies

All dependencies — including the `finmodel` library from
[github.com/zeemarquez/finmodel](https://github.com/zeemarquez/finmodel) — are pinned in
[`requirements.txt`](requirements.txt):

```bash
pip install -r requirements.txt
```

> `finmodel` is not published on PyPI, so it is installed straight from GitHub. To install
> it on its own:
>
> ```bash
> pip install git+https://github.com/zeemarquez/finmodel.git
> ```
>
> If you want to hack on `finmodel` alongside these notebooks, clone it separately and do
> an editable install instead: `git clone https://github.com/zeemarquez/finmodel.git`
> then `pip install -e ../finmodel`.

### 4. Launch Jupyter

```bash
jupyter lab
```

## How to run

Run the notebooks in order (`01` → `02` → `03a` → `03b`). Notebook `03b` depends on the
synthetic dataset written by `03a`, which in turn depends on the merged dataset written
by `02`.

A few notes:

- **Run each notebook from its own folder** so the local `utils/` helpers (Plotly theme,
  progress widget) and `data/` paths resolve correctly.
- **Notebook `02` needs internet access** — it fetches measured irradiance from the NASA
  POWER API. The other notebooks read the CSV/JSON data already committed in the repo.
- **Regenerating the synthetic data** (`03a`) writes ~1.3 GB across 1,000 CSVs into
  `03-pv-stochastic-model/data/PV_SYNTHETIC_DATA/`; this is optional, as the bundle is
  already committed.
