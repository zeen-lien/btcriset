"""FINAL VISUALIZATION FIX — C1 corrected data only.

Regenerates ONLY the stability-vs-error scatter figures from
reports/final-pairing-evidence.csv, using the frozen C1 pairing:
    X = jaccard_t = Jaccard(S_t, S_{t+1})
    Y = mae_t_plus_1 = MAE_{t+1}

Design preserved from the previous figures: observation points, clear axis labels,
title naming Jaccard vs next-window OOS MAE, grid. No regression line and no
inferential annotation (neither existed in the previous design).

Does NOT touch any experiment artifact, dataset, model, or other figure.
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

ROOT = Path("D:/Hermes/Projects/riset-btc")
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

ev = pd.read_csv(REPORTS / "final-pairing-evidence.csv")

# Sanity: pairing columns must exist (J_t -> MAE_{t+1})
assert {"dataset", "jaccard_t", "mae_t_plus_1"}.issubset(ev.columns)

SPECS = {
    "Binance": ("stability_vs_error_scatter.png",
                "Feature Stability ($J_t$) vs. Next-Window OOS Error ($MAE_{t+1}$)"),
    "Coinbase": ("coinbase_stability_vs_error_scatter.png",
                 "Coinbase: Stability ($J_t$) vs. Next-Window OOS Error ($MAE_{t+1}$)"),
}

for dataset, (fname, title) in SPECS.items():
    sub = ev[ev["dataset"] == dataset].sort_values("t")
    assert len(sub) > 0, f"no rows for {dataset}"
    assert not sub[["jaccard_t", "mae_t_plus_1"]].isna().any().any()

    plt.figure(figsize=(6, 6))
    plt.scatter(sub["jaccard_t"], sub["mae_t_plus_1"], color="#1b9e77", s=60, alpha=0.8)
    plt.title(title, fontsize=11, fontweight="bold")
    plt.xlabel("Jaccard Index ($J_t$) = Jaccard($S_t$, $S_{t+1}$)", fontsize=10)
    plt.ylabel("Next-Window OOS MAE ($MAE_{t+1}$)", fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURES / fname, dpi=300)
    plt.close()
    print(f"{dataset}: {len(sub)} points -> reports/figures/{fname}")

print("done")
