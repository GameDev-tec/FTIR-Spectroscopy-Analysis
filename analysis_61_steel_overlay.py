from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# Paths
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent

FILES = {
    "Steel n3": ROOT / "steel_n3_nopol_8zff_BH3.dat",
    "Steel n6": ROOT / "steel_n6_nopol_8zff_BH3.dat",
}

FIGURES_DIR = ROOT / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

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
# Inspect data
# --------------------------------------------------

spectra = {}

for label, file in FILES.items():

    wn, signal = load_spectrum(file)

    spectra[label] = (wn, signal)

    print("\n" + "=" * 60)
    print(label)

    print(
        f"Wavenumber range : "
        f"{wn.min():.2f} → {wn.max():.2f} cm^-1"
    )

    print(
        f"Signal range     : "
        f"{signal.min():.6f} → {signal.max():.6f}"
    )

    print(
        f"Number of points : "
        f"{len(wn)}"
    )

# --------------------------------------------------
# Full spectrum overlay
# --------------------------------------------------

plt.figure(figsize=(11, 6))

for label, (wn, signal) in spectra.items():

    plt.plot(
        wn,
        signal,
        linewidth=1.5,
        label=label
    )

plt.title(
    "Stainless Steel Spectra"
)

plt.xlabel(
    "Wavenumber (cm$^{-1}$)"
)

plt.ylabel(
    "Signal (a.u.)"
)

plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "06_steel_overlay_full.png",
    dpi=300,
    bbox_inches="tight"
)

# --------------------------------------------------
# Zoom to 0–5000 cm^-1
# --------------------------------------------------

plt.figure(figsize=(11, 6))

for label, (wn, signal) in spectra.items():

    mask = (
        (wn >= 0)
        &
        (wn <= 5000)
    )

    plt.plot(
        wn[mask],
        signal[mask],
        linewidth=1.5,
        label=label
    )

plt.title(
    "Stainless Steel Spectra (0–5000 cm$^{-1}$)"
)

plt.xlabel(
    "Wavenumber (cm$^{-1}$)"
)

plt.ylabel(
    "Signal (a.u.)"
)

plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "06_steel_overlay_0_5000.png",
    dpi=300,
    bbox_inches="tight"
)

# --------------------------------------------------
# Individual spectra
# --------------------------------------------------

for label, (wn, signal) in spectra.items():

    plt.figure(figsize=(10, 6))

    plt.plot(
        wn,
        signal,
        linewidth=1.5
    )

    plt.title(
        f"{label}"
    )

    plt.xlabel(
        "Wavenumber (cm$^{-1}$)"
    )

    plt.ylabel(
        "Signal (a.u.)"
    )

    plt.grid(True)

    plt.tight_layout()

    filename = (
        label.lower()
             .replace(" ", "_")
    )

    plt.savefig(
        FIGURES_DIR /
        f"06_{filename}.png",
        dpi=300,
        bbox_inches="tight"
    )

print(
    "\nSaved figures to figures/"
)

plt.show()