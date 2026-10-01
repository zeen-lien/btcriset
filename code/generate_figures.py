"""Generate publication-ready figures for the research report."""
from __future__ import annotations

import json
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(REPORTS / "experiment_results.csv")

# 1. Jaccard stability over time
plt.figure(figsize=(10, 4))
plt.plot(df["window_id"], df["jaccard_to_next"], marker="o", color="#2b5c8f", lw=2)
plt.title("Bitcoin Feature Subset Stability ($J_t$) Across Rolling Windows", fontsize=12, fontweight="bold")
plt.xlabel("Rolling Window ID", fontsize=10)
plt.ylabel("Jaccard Index ($J_t$)", fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURES / "jaccard_stability.png", dpi=300)
plt.close()

# 2. XGBoost MAE vs Naive MAE
plt.figure(figsize=(10, 4))
plt.plot(df["window_id"], df["xgboost_mae"], marker="s", color="#d95f02", label="XGBoost MAE", lw=2)
plt.plot(df["window_id"], df["naive_mae"], marker="^", color="#7570b3", label="Zero-Return Naive MAE", lw=2, linestyle="--")
plt.title("Out-of-Sample MAE: XGBoost vs. Zero-Return Baseline", fontsize=12, fontweight="bold")
plt.xlabel("Rolling Window ID", fontsize=10)
plt.ylabel("Mean Absolute Error", fontsize=10)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURES / "forecast_error_comparison.png", dpi=300)
plt.close()

# 3. Scatter J_t vs Paired MAE_{t+1}
aligned = df.copy()
aligned["paired_mae_next"] = aligned["xgboost_mae"].shift(-1)
paired = aligned.dropna(subset=["jaccard_to_next", "paired_mae_next"])

plt.figure(figsize=(6, 6))
plt.scatter(paired["jaccard_to_next"], paired["paired_mae_next"], color="#1b9e77", s=60, alpha=0.8)
plt.title("Feature Stability ($J_t$) vs. Subsequent OOS Error ($MAE_{t+1}$)", fontsize=11, fontweight="bold")
plt.xlabel("Jaccard Index ($J_t$)", fontsize=10)
plt.ylabel("Subsequent OOS MAE ($MAE_{t+1}$)", fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURES / "stability_vs_error_scatter.png", dpi=300)
plt.close()

print("Figures generated successfully under reports/figures/")
