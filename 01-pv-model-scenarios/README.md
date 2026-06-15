# 01 · Solar PV Project Finance Model & Scenario Analysis

**Notebook:** [`pv-model.ipynb`](pv-model.ipynb)

## What this notebook does

It builds a complete, integrated **project finance model** for a 10 MW utility-scale
solar PV plant and runs a deterministic **scenario sweep** to measure how investor
returns respond to the solar resource assumption.

This is the deterministic baseline for the portfolio. Notebooks `02` and `03` extend
it with real-world data and a stochastic Monte Carlo simulation.

## The model

A classic *three-statement, cash-flow-waterfall* model of the kind used to size
non-recourse debt and price equity returns for a project SPV:

- **Timeline** — 1 year of construction followed by a 25-year operating life, modelled
  on an annual time grid (26 periods).
- **Revenues** — energy production (capacity × net equivalent hours × availability ×
  degradation) sold partly under a fixed-price **PPA** and partly at **merchant**
  market prices, both indexed to inflation.
- **P&L** — revenues → EBITDA → EBIT (after depreciation) → EBT (after financial
  expenses) → net income (after tax).
- **Balance sheet** — net fixed assets, working capital, cash, debt and equity, with a
  per-period `balance_check` (assets = liabilities).
- **Cash flow waterfall** — EBITDA → cash available for debt service → debt repayment
  → cash to shareholders → dividends.
- **Financing** — bank debt **sculpted** to a target **DSCR** (1.25×); equity funds the
  residual.

The model is **circular** (interest ⇄ debt balance ⇄ cash flow ⇄ debt sizing), so it is
solved with `finmodel`'s iterative calculation rather than closed-form algebra.

## Implementation notes

- Built with the [`finmodel`](../) library — each line item is a Python function
  decorated with `@row(...)` and evaluated lazily per period, with spreadsheet-style
  cross-references (`self.revenue(t-1)`).
- All assumptions live in a single `Inputs` dataclass, which makes scenario analysis a
  matter of cloning the dataclass with one field changed (`dataclasses.replace`).
- Iterative calc is tuned with `damping=1.0`, `max_iterations=100` — the library default
  damping of 0.5 over-damps this particular model and prevents convergence.

## Scenario analysis

Using the `Scenarios` helper, `net_equivalent_hours` (the resource — the most uncertain
input) is swept across **900 → 2,000 hours** over 100 cases. Two equity-return metrics
are tracked:

- **Cash-on-cash (`coc`)** — total dividends ÷ total capital invested.
- **IRR (`irr`)** — internal rate of return of the equity cash-flow stream.

The resulting IRR-vs-resource curve illustrates the project's **operating leverage**:
with a large fixed cost base (capex + debt service), equity returns are highly geared to
the solar resource.

## Key outputs

- A fully styled three-statement model table (`model.show()`).
- A `coc` / `irr` scenario table.
- An **IRR vs. net equivalent hours** sensitivity chart.

## How to run

Run the cells top to bottom. Requires `finmodel`, `pandas`, `numpy`,
`numpy_financial`, `plotly`, and the local `utils/` Plotly theme helpers.
