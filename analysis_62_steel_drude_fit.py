from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv

# --------------------------------------------------
# Paths
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent

FILES = {
    "n3": ROOT / "steel_n3_nopol_8zff_BH3.dat",
    "n6": ROOT / "steel_n6_nopol_8zff_BH3.dat",
}

FIGURES_DIR = ROOT / "figures"
RESULTS_DIR = ROOT / "results"

FIGURES_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# Fit range
# --------------------------------------------------

FIT_MIN = 500
FIT_MAX = 5000

# --------------------------------------------------
# Load spectrum
# --------------------------------------------------

def load_spectrum(path):

    data = np.loadtxt(path)

    wn = data[:, 0]
    signal = data[:, 1]

    order = np.argsort(wn)

    return wn[order], signal[order]

# --------------------------------------------------
# Drude + Lorentz dielectric function
# --------------------------------------------------

def dielectric_function(
    nu,
    eps_inf,

    wp_d,
    gamma_d,

    wp_l,
    gamma_l
):

    # -------------------------------
    # Drude
    # -------------------------------

    drude = (
        -(wp_d ** 2)
        /
        (
            nu**2
            + 1j * gamma_d * nu
        )
    )

    # -------------------------------
    # Lorentz oscillator
    # fixed omega0 = 200 cm^-1
    # -------------------------------

    omega0 = 200.0

    lorentz = (
        wp_l**2
        /
        (
            omega0**2
            - nu**2
            - 1j * gamma_l * nu
        )
    )

    return eps_inf + drude + lorentz

# --------------------------------------------------
# Reflectivity
# --------------------------------------------------

def reflectivity_model(
    nu,
    eps_inf,
    wp_d,
    gamma_d,
    wp_l,
    gamma_l
):

    eps = dielectric_function(
        nu,
        eps_inf,
        wp_d,
        gamma_d,
        wp_l,
        gamma_l
    )

    N = np.sqrt(eps)

    R = np.abs(
        (N - 1)
        /
        (N + 1)
    )**2

    return R

# --------------------------------------------------
# Initial guesses
# --------------------------------------------------

P0 = [

    1.0,      # eps_inf

    15000.0,  # wp_d
    500.0,    # gamma_d

    8000.0,   # wp_l
    200.0     # gamma_l

]

BOUNDS = (

    [

        0.1,
        1000,
        1,

        100,
        1

    ],

    [

        100,
        100000,
        10000,

        50000,
        5000

    ]

)

# --------------------------------------------------
# Storage
# --------------------------------------------------

results = []

# --------------------------------------------------
# Main loop
# --------------------------------------------------

for label, file in FILES.items():

    wn, R_exp = load_spectrum(file)

    mask = (
        (wn >= FIT_MIN)
        &
        (wn <= FIT_MAX)
    )

    wn = wn[mask]
    R_exp = R_exp[mask]

    try:

        popt, pcov = curve_fit(
            reflectivity_model,
            wn,
            R_exp,
            p0=P0,
            bounds=BOUNDS,
            maxfev=100000
        )

        (
            eps_inf,
            wp_d,
            gamma_d,
            wp_l,
            gamma_l
        ) = popt

        print("\n" + "=" * 60)
        print(label)

        print(f"eps_inf = {eps_inf:.4f}")

        print(f"wp_d    = {wp_d:.2f}")
        print(f"gamma_d = {gamma_d:.2f}")

        print(f"wp_l    = {wp_l:.2f}")
        print(f"gamma_l = {gamma_l:.2f}")

        results.append([
            label,
            eps_inf,
            wp_d,
            gamma_d,
            wp_l,
            gamma_l
        ])

        # -----------------------------------
        # Calculate fit
        # -----------------------------------

        eps = dielectric_function(
            wn,
            *popt
        )

        eps1 = np.real(eps)
        eps2 = np.imag(eps)

        R_fit = reflectivity_model(
            wn,
            *popt
        )

        # -----------------------------------
        # Reflectivity fit
        # -----------------------------------

        plt.figure(figsize=(8,5))

        plt.plot(
            wn,
            R_exp,
            label="Data"
        )

        plt.plot(
            wn,
            R_fit,
            "--",
            linewidth=2,
            label="Fit"
        )

        plt.xlabel(
            "Wavenumber (cm$^{-1}$)"
        )

        plt.ylabel(
            "Reflectivity"
        )

        plt.title(
            f"Steel {label} Reflectivity Fit"
        )

        plt.grid(True)
        plt.legend()

        plt.tight_layout()

        plt.savefig(
            FIGURES_DIR /
            f"62_reflectivity_fit_{label}.png",
            dpi=300
        )

        # -----------------------------------
        # sigma1 from DRUDE ONLY
        # -----------------------------------

        drude_only = (
            -(wp_d ** 2)
            /
            (
                wn**2
                + 1j * gamma_d * wn
            )
        )

        sigma1 = np.imag(
            drude_only
        )

        plt.figure(figsize=(8,5))

        plt.plot(
            wn,
            sigma1
        )

        plt.xlabel(
            "Wavenumber (cm$^{-1}$)"
        )

        plt.ylabel(
            r"$\sigma_1$ (arb.)"
        )

        plt.title(
            f"Steel {label} Drude Conductivity"
        )

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            FIGURES_DIR /
            f"62_sigma1_{label}.png",
            dpi=300
        )

    except Exception as e:

        print("\nFit failed")
        print(label)
        print(e)

# --------------------------------------------------
# Save parameters
# --------------------------------------------------

csv_file = (
    RESULTS_DIR /
    "steel_drude_fit_parameters.csv"
)

with open(
    csv_file,
    "w",
    newline=""
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "sample",
        "eps_inf",
        "wp_d",
        "gamma_d",
        "wp_l",
        "gamma_l"
    ])

    writer.writerows(results)

print("\nSaved:")
print(csv_file)

plt.show()