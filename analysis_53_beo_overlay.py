import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path.cwd()

FILES = {
    "0°": ROOT / "BeO_0pol_8zff_BH3_2.dat",
    "45°": ROOT / "BeO_45pol_8zff_BH3.dat",
    "90°": ROOT / "BeO_90pol_8zff_BH3.dat",
    "Reference 0°": ROOT / "Ref_0pol_8zff_BH3.dat",
    "Reference 45°": ROOT / "Ref_45pol_8zff_BH3.dat",
    "Reference 90°": ROOT / "Ref_90pol_8zff_BH3.dat"
}

WN_MIN = 500
WN_MAX = 1300


def load_spectrum(path):
    data = np.loadtxt(path)

    wn = data[:, 0]
    intensity = data[:, 1]

    order = np.argsort(wn)

    return wn[order], intensity[order]


plt.figure(figsize=(11, 6))

for pol, file in FILES.items():

    wn, intensity = load_spectrum(file)

    mask = (
        (wn >= WN_MIN)
        & (wn <= WN_MAX)
    )

    wn = wn[mask]
    intensity = intensity[mask]

    plt.plot(
        wn,
        intensity,
        linewidth=2,
        label=pol
    )

plt.title(
    "BeO Spectra Comparison"
)

plt.xlabel(
    "Wavenumber (cm$^{-1}$)"
)

plt.ylabel(
    "Signal Reflectivity (a.u.)"
)
plt.axvspan(
    650,
    730,
    alpha=0.15,
    label="TO region"
)

plt.axvspan(
    1070,
    1110,
    alpha=0.15,
    label="LO region"
)
plt.grid(True)
plt.legend()

plt.tight_layout()
FIGURES_DIR = ROOT / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

plt.savefig(
    FIGURES_DIR / "03_beo_overlay.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# --------------------------------------------------
# Individual BeO spectra
# --------------------------------------------------

for pol, file in FILES.items():

    wn, intensity = load_spectrum(file)

    mask = (
        (wn >= WN_MIN)
        & (wn <= WN_MAX)
    )

    wn = wn[mask]
    intensity = intensity[mask]

    plt.figure(figsize=(10, 6))

    plt.plot(
        wn,
        intensity,
        linewidth=2,
        label=pol
    )

    plt.axvspan(
        650,
        730,
        alpha=0.15,
        label="TO region"
    )

    plt.axvspan(
        1070,
        1110,
        alpha=0.15,
        label="LO region"
    )

    plt.title(
        f"BeO Spectrum ({pol})"
    )

    plt.xlabel(
        "Wavenumber (cm$^{-1}$)"
    )

    plt.ylabel(
        "Signal / Reflectivity (a.u.)"
    )

    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    filename = (
        pol.replace("°", "deg")
           .replace(" ", "_")
    )

    plt.savefig(
        FIGURES_DIR / f"03_beo_{filename}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()