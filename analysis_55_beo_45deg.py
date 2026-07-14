from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent

FILE = ROOT / "BeO_45pol_8zff_BH3.dat"

FIGURES_DIR = ROOT / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

FIT_MIN = 500
FIT_MAX = 1300


def load_spectrum(path):

    data = np.loadtxt(path)

    wn = data[:, 0]
    signal = data[:, 1]

    order = np.argsort(wn)

    return wn[order], signal[order]


wn, R = load_spectrum(FILE)

mask = (
    (wn >= FIT_MIN)
    &
    (wn <= FIT_MAX)
)

wn = wn[mask]
R = R[mask]

plt.figure(figsize=(9,5))

plt.plot(
    wn,
    R,
    linewidth=2
)

plt.title(
    "BeO Reflectivity (45° Polarization)"
)

plt.xlabel(
    "Wavenumber (cm$^{-1}$)"
)

plt.ylabel(
    "Reflectivity (a.u.)"
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "06_reflectivity_45deg.png",
    dpi=300
)

plt.show()
