import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from pathlib import Path
import pandas as pd

# ============================================================
# SETTINGS
# ============================================================

DATA_DIR = Path("/Users/amaydusar/Downloads/data praktikum M2.7")

FILES = {
    "n3": "steel_n3_nopol_8zff_BH3.dat",
    "n6": "steel_n6_nopol_8zff_BH3.dat",
}

FIT_MIN = 500
FIT_MAX = 5000

OMEGA0_FIXED = 200.0

# ============================================================
# DIELECTRIC FUNCTION
# ============================================================

def eps_drude_lorentz(w, eps_inf,
                      wp_d, gamma_d,
                      wp_l, gamma_l):

    eps = (
        eps_inf
        - wp_d**2 / (w**2 + 1j*gamma_d*w)
        + wp_l**2 /
          (OMEGA0_FIXED**2 - w**2 - 1j*gamma_l*w)
    )

    return eps


def reflectivity_model(w,
                       eps_inf,
                       wp_d,
                       gamma_d,
                       wp_l,
                       gamma_l):

    eps = eps_drude_lorentz(
        w,
        eps_inf,
        wp_d,
        gamma_d,
        wp_l,
        gamma_l
    )

    n_complex = np.sqrt(eps)

    R = np.abs(
        (n_complex - 1) /
        (n_complex + 1)
    )**2

    return np.real(R)

# ============================================================
# DRUDE CONDUCTIVITY
# ============================================================

def sigma1_drude(w, wp_d, gamma_d):
    """
    Real conductivity of ONLY free electrons.

    Arbitrary units are fine for the lab report.
    """

    return (
        wp_d**2 * gamma_d
        /
        (gamma_d**2 + w**2)
    )

# ============================================================
# LOAD DATA
# ============================================================

results = []

for sample, filename in FILES.items():

    print("\n" + "="*60)
    print(sample)

    data = np.loadtxt(DATA_DIR / filename)

    wn = data[:,0]
    R  = data[:,1]

    mask = (
        (wn >= FIT_MIN)
        &
        (wn <= FIT_MAX)
    )

    wn_fit = wn[mask]
    R_fit  = R[mask]

    # --------------------------------------------------------
    # Initial guess
    # --------------------------------------------------------

    p0 = [
        5.0,        # eps_inf
        40000.0,    # wp_d
        8000.0,     # gamma_d
        8000.0,     # wp_l
        200.0       # gamma_l
    ]

    # --------------------------------------------------------
    # Bounds
    # --------------------------------------------------------

    lower = [
        1.0,        # eps_inf
        1000.0,     # wp_d
        100.0,      # gamma_d
        1000.0,     # wp_l
        50.0        # gamma_l
    ]

    upper = [
        100.0,      # eps_inf
        80000.0,    # wp_d
        50000.0,    # gamma_d
        15000.0,    # wp_l
        3000.0      # gamma_l
    ]

    popt, _ = curve_fit(
        reflectivity_model,
        wn_fit,
        R_fit,
        p0=p0,
        bounds=(lower, upper),
        maxfev=50000
    )

    (
        eps_inf,
        wp_d,
        gamma_d,
        wp_l,
        gamma_l
    ) = popt

    print(f"eps_inf = {eps_inf:.4f}")
    print(f"wp_d    = {wp_d:.2f}")
    print(f"gamma_d = {gamma_d:.2f}")
    print(f"wp_l    = {wp_l:.2f}")
    print(f"gamma_l = {gamma_l:.2f}")

    # --------------------------------------------------------
    # Reflectivity fit
    # --------------------------------------------------------

    R_model = reflectivity_model(wn_fit, *popt)

    plt.figure(figsize=(9,5))
    plt.plot(wn_fit, R_fit, lw=2, label="Data")
    plt.plot(
        wn_fit,
        R_model,
        "--",
        lw=3,
        label="Drude-Lorentz Fit"
    )

    plt.xlabel("Wavenumber (cm$^{-1}$)")
    plt.ylabel("Reflectivity")
    plt.title(f"{sample} Reflectivity Fit")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # --------------------------------------------------------
    # Sigma1
    # --------------------------------------------------------

    sigma1 = sigma1_drude(
        wn_fit,
        wp_d,
        gamma_d
    )

    plt.figure(figsize=(9,5))
    plt.plot(wn_fit, sigma1, lw=2)

    plt.xlabel("Wavenumber (cm$^{-1}$)")
    plt.ylabel(r"$\sigma_1$")
    plt.title(f"{sample} Drude Conductivity")
    plt.tight_layout()
    plt.show()

    sigma_dc = wp_d**2 / gamma_d

    results.append({
        "sample": sample,
        "eps_inf": eps_inf,
        "wp_d": wp_d,
        "gamma_d": gamma_d,
        "wp_l": wp_l,
        "gamma_l": gamma_l,
        "sigma_dc": sigma_dc
    })

# ============================================================
# SAVE RESULTS
# ============================================================

df = pd.DataFrame(results)

out = DATA_DIR / "results" / "steel_drude_lorentz_fit.csv"

out.parent.mkdir(exist_ok=True)

df.to_csv(out, index=False)

print("\nSaved:")
print(out)