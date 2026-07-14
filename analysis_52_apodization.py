from pathlib import Path
import argparse
import os

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib-cache"))

# --------------------------------------------------
# Arguments
# --------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare apodization functions around the 1500 cm^-1 peak."
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Save figures without opening interactive windows."
    )
    return parser.parse_args()


ARGS = parse_args()

if ARGS.no_show:
    os.environ.setdefault("MPLBACKEND", "Agg")

import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# Files
# --------------------------------------------------

APODIZATION_FILES = {
    "Boxcar": ROOT / "Ref_0pol_8zff_boxcar.dat",
    "Triangular": ROOT / "Ref_0pol_8zff_triangular.dat",
    "Blackman-Harris3": ROOT / "Ref_0pol_8zff_BH3.dat",
}

# SAME PEAK AS QUESTION 5.1
ZOOM_MIN = 1502.0
ZOOM_MAX = 1510.0

FIGURE_DIR = ROOT / "figures"


# --------------------------------------------------
# Data Handling
# --------------------------------------------------

def load_spectrum(path):
    data = np.loadtxt(path)

    wn = data[:, 0]
    intensity = data[:, 1]

    order = np.argsort(wn)

    return wn[order], intensity[order]


def select_zoom(wn, intensity):
    mask = (wn >= ZOOM_MIN) & (wn <= ZOOM_MAX)
    return wn[mask], intensity[mask]


def local_minimum(wn, intensity):
    idx = np.argmin(intensity)
    return wn[idx], intensity[idx]


# --------------------------------------------------
# Plot 1: Three stacked panels
# --------------------------------------------------

def plot_three_panels(spectra):

    fig, axes = plt.subplots(
        3,
        1,
        figsize=(8, 9),
        sharex=True,
        constrained_layout=True
    )

    for ax, (label, (wn, intensity)) in zip(axes, spectra.items()):

        wn_zoom, i_zoom = select_zoom(wn, intensity)

        wn_min, i_min = local_minimum(
            wn_zoom,
            i_zoom
        )

        ax.plot(
            wn_zoom,
            i_zoom,
            linewidth=1.4
        )

        ax.scatter(
            wn_min,
            i_min,
            color="crimson",
            zorder=3
        )

        ax.annotate(
            f"{wn_min:.2f} cm$^{{-1}}$",
            xy=(wn_min, i_min),
            xytext=(8, 12),
            textcoords="offset points",
            color="crimson",
            fontsize=9
        )

        ax.set_title(label)
        ax.set_ylabel("Intensity (a.u.)")
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel(
        "Wavenumber (cm$^{-1}$)"
    )

    fig.suptitle(
        "Comparison of Apodization Functions Near 1500 cm$^{-1}$",
        fontsize=13
    )

    output = (
        FIGURE_DIR /
        "apodization_three_panels.png"
    )

    fig.savefig(
        output,
        dpi=300
    )

    print(f"Saved: {output}")


# --------------------------------------------------
# Plot 2: Individual figures
# --------------------------------------------------

def plot_individual_figures(spectra):

    for label, (wn, intensity) in spectra.items():

        wn_zoom, i_zoom = select_zoom(
            wn,
            intensity
        )

        wn_min, i_min = local_minimum(
            wn_zoom,
            i_zoom
        )

        fig, ax = plt.subplots(
            figsize=(8, 4.5),
            constrained_layout=True
        )

        ax.plot(
            wn_zoom,
            i_zoom,
            linewidth=1.5
        )

        ax.scatter(
            wn_min,
            i_min,
            color="crimson",
            zorder=3
        )

        ax.annotate(
            f"minimum: {wn_min:.2f} cm$^{{-1}}$",
            xy=(wn_min, i_min),
            xytext=(8, 12),
            textcoords="offset points",
            color="crimson",
            fontsize=9
        )

        ax.set_title(
            f"{label} Apodization"
        )

        ax.set_xlabel(
            "Wavenumber (cm$^{-1}$)"
        )

        ax.set_ylabel(
            "Intensity (a.u.)"
        )

        ax.grid(True, alpha=0.3)

        filename = (
            label.lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

        output = (
            FIGURE_DIR /
            f"{filename}_apodization.png"
        )

        fig.savefig(
            output,
            dpi=300
        )

        print(f"Saved: {output}")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    FIGURE_DIR.mkdir(
        exist_ok=True
    )

    spectra = {}

    for label, path in APODIZATION_FILES.items():

        wn, intensity = load_spectrum(path)

        spectra[label] = (
            wn,
            intensity
        )

        wn_zoom, i_zoom = select_zoom(
            wn,
            intensity
        )

        wn_min, i_min = local_minimum(
            wn_zoom,
            i_zoom
        )

        print(
            f"{label}: "
            f"minimum at {wn_min:.3f} cm^-1, "
            f"intensity = {i_min:.6g}"
        )

    plot_three_panels(
        spectra
    )

    plot_individual_figures(
        spectra
    )

    if ARGS.no_show:
        plt.close("all")
        print("Done.")
    else:
        plt.show()


if __name__ == "__main__":
    main()