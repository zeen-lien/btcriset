"""Stationary bootstrap + automatic block length (Politis & White 2004; Patton, Politis & White 2009 correction)."""
from __future__ import annotations

import numpy as np


def _acvf(x: np.ndarray, max_lag: int) -> np.ndarray:
    x = x - x.mean()
    n = len(x)
    acf = np.correlate(x, x, mode="full")[n - 1:] / (x.var(ddof=0) * n)
    return acf[: max_lag + 1]


def automatic_block_length(x: np.ndarray, random_state: int = 42) -> float:
    """Politis & White (2004) automatic block length with Patton et al. (2009) correction.

    Returns the expected block length b >= 1.
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 4:
        return 1.0
    max_lag = int(np.floor(n ** (1 / 3)))
    max_lag = max(max_lag, 1)
    acf = _acvf(x, max_lag)
    # Politis-White suggestion: sum acf^2 truncated at max_lag
    ss = float(np.sum(acf[1:] ** 2))
    if ss <= 0 or not np.isfinite(ss):
        return 1.0
    b = (2 * np.pi * ss) ** (-1 / 3) * (n ** (1 / 3))
    # Patton et al. (2009) correction factor
    b *= (4.0 / 3.0)
    return max(float(b), 1.0)


def stationary_bootstrap_pairs(
    x: np.ndarray,
    y: np.ndarray,
    b: float,
    B: int = 5000,
    seed: int = 42,
    ci_level: float = 0.95,
) -> dict:
    """Paired stationary bootstrap for (x, y). Returns bootstrap distribution + CI.

    Pairs (x_i, y_i) are resampled jointly; never independently shuffled.
    """
    rng = np.random.RandomState(seed)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    assert len(x) == len(y)
    n = len(x)
    if n < 2:
        return {"bootstrap_mean": float(np.nan), "ci_lower": float(np.nan), "ci_upper": float(np.nan),
                "replications": B, "block_length": b, "distribution": np.array([])}
    p = 1.0 / max(float(b), 1.0)
    stats = np.empty(B)
    for i in range(B):
        idx = np.empty(n, dtype=int)
        pos = 0
        while pos < n:
            start = rng.randint(0, n)
            length = rng.geometric(p)
            for k in range(length):
                if pos >= n:
                    break
                idx[pos] = (start + k) % n
                pos += 1
        from scipy.stats import spearmanr
        rho, _ = spearmanr(x[idx], y[idx])
        stats[i] = float(rho)
    alpha = (1 - ci_level) / 2
    ci_lower = float(np.percentile(stats, 100 * alpha))
    ci_upper = float(np.percentile(stats, 100 * (1 - alpha)))
    return {"bootstrap_mean": float(stats.mean()), "ci_lower": ci_lower, "ci_upper": ci_upper,
            "replications": B, "block_length": b, "distribution": stats}
