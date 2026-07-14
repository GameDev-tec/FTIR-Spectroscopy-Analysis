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
    "0deg": ROOT / "BeO_0pol_8zff_BH3_2.dat",
    "90deg": ROOT / "BeO_90pol_8zff_BH3.dat",
}

FIGURES_DIR = ROOT / "figures"
RESULTS_DIR = ROOT / "results"

FIGURES_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# Fit range
# --------------------------------------------------

FIT_MIN = 500
FIT_MAX = 1300

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
# Dielectric model
# --------------------------------------------------

def dielectric_function(
    nu,
    eps_inf,
    S,
    nu_TO,
    gamma
):

    return (
        eps_inf
        +
        S
        /
        (
            nu_TO**2
            - nu**2
            - 1j * gamma * nu
        )
    )


# --------------------------------------------------
# Reflectivity model
# --------------------------------------------------

def reflectivity_model(
    nu,
    eps_inf,
    S,
    nu_TO,
    gamma
):

    eps = dielectric_function(
        nu,
        eps_inf,
        S,
        nu_TO,
        gamma
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

INITIAL_GUESSES = {
    "0deg": [6.5, 5e6, 723.0, 20.0],
    "90deg": [6.5, 5e6, 678.0, 20.0],
}

# --------------------------------------------------
# Storage
# --------------------------------------------------

fit_results = []

# --------------------------------------------------
# Main loop
# --------------------------------------------------

for pol, file in FILES.items():

    wn, R_exp = load_spectrum(file)

    mask = (
        (wn >= FIT_MIN)
        &
        (wn <= FIT_MAX)
    )

    wn = wn[mask]
    R_exp = R_exp[mask]

    p0 = INITIAL_GUESSES[pol]

    bounds = (
        [1.0, 1e4, 600, 1],
        [20.0, 1e9, 800, 200]
    )

    try:

        popt, pcov = curve_fit(
            reflectivity_model,
            wn,
            R_exp,
            p0=p0,
            bounds=bounds,
            maxfev=50000
        )

        eps_inf, S, nu_TO, gamma = popt

        fit_results.append(
            [
                pol,
                eps_inf,
                S,
                nu_TO,
                gamma
            ]
        )

        print("\n" + "=" * 50)
        print(pol)

        print(
            f"eps_inf = {eps_inf:.4f}"
        )

        print(
            f"S       = {S:.4e}"
        )

        print(
            f"nu_TO   = {nu_TO:.2f} cm^-1"
        )

        print(
            f"gamma   = {gamma:.2f}"
        )

        # ------------------------------------------
        # Calculate optical quantities
        # ------------------------------------------

        eps = dielectric_function(
            wn,
            eps_inf,
            S,
            nu_TO,
            gamma
        )

        eps1 = np.real(eps)
        eps2 = np.imag(eps)

        N = np.sqrt(eps)

        n = np.real(N)
        k = np.imag(N)

        R_fit = reflectivity_model(
            wn,
            *popt
        )

        # ------------------------------------------
        # Reflectivity fit
        # ------------------------------------------

        plt.figure(figsize=(8, 5))

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

        plt.title(
            f"Reflectivity Fit ({pol})"
        )

        plt.xlabel(
            "Wavenumber (cm$^{-1}$)"
        )

        plt.ylabel(
            "Reflectivity"
        )

        plt.grid(True)
        plt.legend()

        plt.tight_layout()

        plt.savefig(
            FIGURES_DIR /
            f"05_fit_{pol}.png",
            dpi=300
        )

        # ------------------------------------------
        # eps1
        # ------------------------------------------

        plt.figure(figsize=(8, 5))

        plt.plot(wn, eps1)

        plt.title(
            f"$\\epsilon_1$ ({pol})"
        )

        plt.xlabel(
            "Wavenumber (cm$^{-1}$)"
        )

        plt.ylabel(
            "$\\epsilon_1$"
        )

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            FIGURES_DIR /
            f"05_eps1_{pol}.png",
            dpi=300
        )

        # ------------------------------------------
        # eps2
        # ------------------------------------------

        plt.figure(figsize=(8, 5))

        plt.plot(wn, eps2)

        plt.title(
            f"$\\epsilon_2$ ({pol})"
        )

        plt.xlabel(
            "Wavenumber (cm$^{-1}$)"
        )

        plt.ylabel(
            "$\\epsilon_2$"
        )

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            FIGURES_DIR /
            f"05_eps2_{pol}.png",
            dpi=300
        )

        # ------------------------------------------
        # n
        # ------------------------------------------

        plt.figure(figsize=(8, 5))

        plt.plot(wn, n)

        plt.title(
            f"Refractive Index n ({pol})"
        )

        plt.xlabel(
            "Wavenumber (cm$^{-1}$)"
        )

        plt.ylabel(
            "n"
        )

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            FIGURES_DIR /
            f"05_n_{pol}.png",
            dpi=300
        )

        # ------------------------------------------
        # k
        # ------------------------------------------

        plt.figure(figsize=(8, 5))

        plt.plot(wn, k)

        plt.title(
            f"Extinction Coefficient k ({pol})"
        )

        plt.xlabel(
            "Wavenumber (cm$^{-1}$)"
        )

        plt.ylabel(
            "k"
        )

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            FIGURES_DIR /
            f"05_k_{pol}.png",
            dpi=300
        )

    except Exception as e:

        print(
            f"\nFit failed for {pol}"
        )

        print(e)

# --------------------------------------------------
# Save fit parameters
# --------------------------------------------------

csv_file = (
    RESULTS_DIR /
    "dielectric_fit_parameters.csv"
)

with open(
    csv_file,
    "w",
    newline=""
) as f:

    writer = csv.writer(f)

    writer.writerow(
        [
            "Polarization",
            "eps_inf",
            "S",
            "nu_TO",
            "gamma"
        ]
    )

    writer.writerows(
        fit_results
    )

print(
    f"\nSaved: {csv_file}"
)

plt.show()