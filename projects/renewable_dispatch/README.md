# Renewable dispatch case study

This folder contains two related artifacts:

- `quick_demo.py` is a small, dependency-free dispatch simulation. It creates synthetic hourly wind, solar, and demand data; uses a battery to reduce unmet demand; and writes a CSV of the results. It is the fastest way to understand and run the basic energy-balance idea.
- `notebooks/original_case_study.ipynb` is the supplied exploratory notebook. It generates five years of **synthetic** hourly data and combines gradient-boosting forecasts, a mixed-integer dispatch model, a Q-learning overlay, and a dashboard. It has more dependencies and may take substantial time to run.

The supplied report uses phrases such as "operational data" and reports numerical improvements, but the notebook itself generates synthetic inputs. Treat its results as a demonstration, not evidence of real grid performance.

## Run the quick demo

From the repository root:

```bash
python projects/renewable_dispatch/quick_demo.py
python projects/renewable_dispatch/tests/test_quick_demo.py
```

The CSV appears in `projects/renewable_dispatch/results/`. Try changing the battery capacity or power limit and compare unmet demand and curtailed energy.

## Run the original notebook

Create a separate Python environment, install `requirements-notebook.txt`, then open the notebook in Jupyter or VS Code. Run it from this folder because it writes relative `data/` and `outputs/` directories. Those generated files are ignored by Git.

```bash
python -m venv .venv
# Activate the environment for your shell, then:
python -m pip install -r projects/renewable_dispatch/requirements-notebook.txt
```

The original notebook is retained as supplied for study. Its output claims have not been independently validated for this portfolio.
