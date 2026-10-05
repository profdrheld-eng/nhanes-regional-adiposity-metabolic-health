"""Rao-Wu rescaled (n_h-1)-PSU subbootstrap, common across models."""
import numpy as np

def rescaled_psu_factors(strata, psus, rng):
    factors = np.zeros(len(strata), dtype=float)
    for stratum in np.unique(strata):
        mask = strata == stratum
        units = np.unique(psus[mask])
        n = len(units)
        if n < 2:
            raise ValueError("Rescaled bootstrap requires at least two PSUs per stratum")
        draws = rng.choice(units, size=n-1, replace=True)
        for unit in units:
            factors[mask & (psus == unit)] = np.sum(draws == unit) * n / (n-1)
    return factors
