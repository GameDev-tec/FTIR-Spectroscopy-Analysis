from pathlib import Path

import numpy as np
import pandas as pd

# ============================================================
# Physical constants (SI)
# ============================================================

e = 1.602176634e-19      # C
m_e = 9.1093837015e-31   # kg
c = 2.99792458e10        # cm/s

# ============================================================
# Load fit results
# ============================================================

RESULTS = Path("results")
fit_file = RESULTS / "steel_drude_lorentz_fit.csv"

df = pd.read_csv(fit_file)

rows = []

for _, row in df.iterrows():

    sample = row["sample"]

    wp_d = float(row["wp_d"])          # cm^-1
    gamma_cm = float(row["gamma_d"])   # cm^-1

    # --------------------------------------------------------
    # Convert gamma to s^-1
    # Lab instruction:
    #
    # gamma[s^-1] = 2*pi*c*gamma[cm^-1]
    # --------------------------------------------------------

    gamma_s = 2.0 * np.pi * c * gamma_cm

    # --------------------------------------------------------
    # Plasma frequency
    #
    # RefFit uses wavenumber units:
    #
    # omega_p = 2*pi*c*wp_d
    #
    # --------------------------------------------------------

    omega_p = 2.0 * np.pi * c * wp_d

    # --------------------------------------------------------
    # Carrier density from:
    #
    # omega_p^2 = N e^2 / (eps0 m_e)
    #
    # SI units
    # --------------------------------------------------------

    eps0 = 8.8541878128e-12

    N_m3 = eps0 * m_e * omega_p**2 / e**2
    N_cm3 = N_m3 / 1e6

    # --------------------------------------------------------
    # Drude dc conductivity
    #
    # sigma_dc = N e^2 / (m_e gamma)
    # --------------------------------------------------------

    sigma_dc = N_m3 * e**2 / (m_e * gamma_s)

    rows.append({
        "sample": sample,
        "wp_d_cm^-1": wp_d,
        "gamma_cm^-1": gamma_cm,
        "gamma_s^-1": gamma_s,
        "omega_p_s^-1": omega_p,
        "sigma_dc_S/m": sigma_dc,
        "carrier_density_m^-3": N_m3,
        "carrier_density_cm^-3": N_cm3,
    })

# ============================================================
# Save
# ============================================================

out = pd.DataFrame(rows)

outfile = RESULTS / "steel_carrier_density.csv"
out.to_csv(outfile, index=False)

print("\n====================================================")
print("Carrier Density Results")
print("====================================================")

for _, r in out.iterrows():

    print(f"\nSample: {r['sample']}")
    print(f"wp_d           = {r['wp_d_cm^-1']:.2f} cm^-1")
    print(f"gamma          = {r['gamma_cm^-1']:.2f} cm^-1")
    print(f"sigma_dc       = {r['sigma_dc_S/m']:.3e} S/m")
    print(f"N              = {r['carrier_density_cm^-3']:.3e} cm^-3")

print(f"\nSaved: {outfile}")