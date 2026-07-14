from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.signal import savgol_filter

# --------------------------------------------------
# Paths
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent

FILES = {
    "0°": ROOT / "BeO_0pol_8zff_BH3_2.dat",
    "45°": ROOT / "BeO_45pol_8zff_BH3.dat",
    "90°": ROOT / "BeO_90pol_8zff_BH3.dat",
}

FIGURES_DIR = ROOT / "figures"
RESULTS_DIR = ROOT / "results"

FIGURES_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# Analysis windows
# --------------------------------------------------

WN_MIN = 500
WN_MAX = 1300

TO_MIN = 650
TO_MAX = 750

LO_MIN = 1050
LO_MAX = 1120

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
# Find TO and LO markers
# --------------------------------------------------

def find_to_lo_markers(wn, signal):

    smooth_signal = savgol_filter(
        signal,
        window_length=51,
        polyorder=3
    )

    derivative = np.gradient(
        smooth_signal,
        wn
    )

    # ---------- TO region ----------

    to_mask = (
        (wn >= TO_MIN)
        & (wn <= TO_MAX)
    )

    wn_to = wn[to_mask]
    d_to = derivative[to_mask]

    to_idx = np.argmax(d_to)

    to_position = wn_to[to_idx]

    # ---------- LO region ----------

    lo_mask = (
        (wn >= LO_MIN)
        & (wn <= LO_MAX)
    )

    wn_lo = wn[lo_mask]
    d_lo = derivative[lo_mask]

    lo_idx = np.argmin(d_lo)

    lo_position = wn_lo[lo_idx]

    return (
        smooth_signal,
        derivative,
        to_position,
        lo_position
    )


# --------------------------------------------------
# Storage
# --------------------------------------------------

results = []

# --------------------------------------------------
# Figure 1
# Spectra with markers
# --------------------------------------------------

plt.figure(figsize=(11, 6))

for pol, file in FILES.items():

    wn, signal = load_spectrum(file)

    mask = (
        (wn >= WN_MIN)
        & (wn <= WN_MAX)
    )

    wn = wn[mask]
    signal = signal[mask]

    (
        smooth_signal,
        derivative,
        to_pos,
        lo_pos
    ) = find_to_lo_markers(
        wn,
        signal
    )

    results.append(
        [pol, to_pos, lo_pos]
    )

    print("\n" + "=" * 40)
    print(pol)

    print(
        f"TO marker = {to_pos:.2f} cm^-1"
    )

    print(
        f"LO marker = {lo_pos:.2f} cm^-1"
    )

    plt.plot(
        wn,
        smooth_signal,
        linewidth=2,
        label=pol
    )

    plt.axvline(
        to_pos,
        linestyle="--",
        alpha=0.8
    )

    plt.axvline(
        lo_pos,
        linestyle=":",
        alpha=0.8
    )

plt.title(
    "BeO Spectra with TO and LO Markers"
)

plt.xlabel(
    "Wavenumber (cm$^{-1}$)"
)

plt.ylabel(
    "Reflectivity (a.u.)"
)

plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "04_beo_phonon_markers.png",
    dpi=300,
    bbox_inches="tight"
)

# --------------------------------------------------
# Figure 2
# Derivatives
# --------------------------------------------------

plt.figure(figsize=(11, 6))

for pol, file in FILES.items():

    wn, signal = load_spectrum(file)

    mask = (
        (wn >= WN_MIN)
        & (wn <= WN_MAX)
    )

    wn = wn[mask]
    signal = signal[mask]

    (
        smooth_signal,
        derivative,
        _,
        _
    ) = find_to_lo_markers(
        wn,
        signal
    )

    plt.plot(
        wn,
        derivative,
        linewidth=2,
        label=pol
    )

plt.title(
    "Derivative dR/dν of BeO Spectra"
)

plt.xlabel(
    "Wavenumber (cm$^{-1}$)"
)

plt.ylabel(
    "dR/dν"
)

plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "04_beo_derivatives.png",
    dpi=300,
    bbox_inches="tight"
)

# --------------------------------------------------
# CSV Output
# --------------------------------------------------

csv_file = (
    RESULTS_DIR /
    "beo_phonon_markers.csv"
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
            "TO_cm^-1",
            "LO_cm^-1"
        ]
    )

    writer.writerows(results)

print(
    f"\nSaved: {csv_file}"
)

plt.show()