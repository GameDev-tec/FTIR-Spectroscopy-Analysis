from pathlib import Path
import argparse
import os

# Keep Matplotlib cache inside the project so the script runs cleanly in VS Code.
ROOT = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib-cache"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot the reference spectra near 1500 cm^-1 for different zero-filling factors."
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Save the figures without opening an interactive Matplotlib window.",
    )
    return parser.parse_args()


ARGS = parse_args()
if ARGS.no_show:
    os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
import numpy as np


# Reference spectra measured with boxcar apodization and different zero filling.
REFERENCE_FILES = {
    "ZF = 1": ROOT / "Ref_0pol_1zff_boxcar.dat",
    "ZF = 8": ROOT / "Ref_0pol_8zff_boxcar.dat",
    "ZF = 32": ROOT / "Ref_0pol_32zff_boxcar.dat",
}

# Zoom window for the downward/negative peak around 1500 cm^-1.
ZOOM_MIN = 1475.0
ZOOM_MAX = 1525.0

FIGURE_DIR = ROOT / "figures"


def load_spectrum(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Load a two-column spectrum and return wavenumber, intensity."""
    data = np.loadtxt(path)
    wavenumber = data[:, 0]
    intensity = data[:, 1]

    # Sort to increasing wavenumber for easier masking and plotting.
    order = np.argsort(wavenumber)
    return wavenumber[order], intensity[order]


def select_zoom(
    wavenumber: np.ndarray,
    intensity: np.ndarray,
    xmin: float = ZOOM_MIN,
    xmax: float = ZOOM_MAX,
) -> tuple[np.ndarray, np.ndarray]:
    """Select the spectral region around the peak of interest."""
    mask = (wavenumber >= xmin) & (wavenumber <= xmax)
    return wavenumber[mask], intensity[mask]


def local_minimum(
    wavenumber: np.ndarray,
    intensity: np.ndarray,
) -> tuple[float, float]:
    """Return the position and intensity of the downward peak."""
    idx = np.argmin(intensity)
    return float(wavenumber[idx]), float(intensity[idx])


def plot_three_panels(spectra: dict[str, tuple[np.ndarray, np.ndarray]]) -> None:
    """Create one figure with three separate plots, one for each zero filling."""
    fig, axes = plt.subplots(
        nrows=3,
        ncols=1,
        figsize=(8, 9),
        sharex=True,
        constrained_layout=True,
    )

    for ax, (label, (wavenumber, intensity)) in zip(axes, spectra.items()):
        wn_zoom, i_zoom = select_zoom(wavenumber, intensity)
        wn_min, i_min = local_minimum(wn_zoom, i_zoom)

        ax.plot(wn_zoom, i_zoom, linewidth=1.4)
        ax.scatter(wn_min, i_min, color="crimson", zorder=3)
        ax.annotate(
            f"{wn_min:.2f} cm$^{{-1}}$",
            xy=(wn_min, i_min),
            xytext=(8, 12),
            textcoords="offset points",
            color="crimson",
            fontsize=9,
        )

        ax.set_title(label)
        ax.set_ylabel("Intensity (a.u.)")
        ax.grid(True, alpha=0.3)

    axes[-1].set_xlabel("Wavenumber (cm$^{-1}$)")

    fig.suptitle(
        "Reference Measurements Around the Downward Peak Near 1500 cm$^{-1}$",
        fontsize=13,
    )

    output = FIGURE_DIR / "zero_filling_negative_peak_1500_three_panels.png"
    fig.savefig(output, dpi=300)
    print(f"Saved: {output}")


def plot_individual_figures(spectra: dict[str, tuple[np.ndarray, np.ndarray]]) -> None:
    """Save three individual plots, one per zero-filling factor."""
    for label, (wavenumber, intensity) in spectra.items():
        wn_zoom, i_zoom = select_zoom(wavenumber, intensity)
        wn_min, i_min = local_minimum(wn_zoom, i_zoom)

        fig, ax = plt.subplots(figsize=(8, 4.5), constrained_layout=True)
        ax.plot(wn_zoom, i_zoom, linewidth=1.4)
        ax.scatter(wn_min, i_min, color="crimson", zorder=3)
        ax.annotate(
            f"minimum: {wn_min:.2f} cm$^{{-1}}$",
            xy=(wn_min, i_min),
            xytext=(8, 12),
            textcoords="offset points",
            color="crimson",
            fontsize=9,
        )

        ax.set_title(f"{label}: Reference Spectrum Near 1500 cm$^{{-1}}$")
        ax.set_xlabel("Wavenumber (cm$^{-1}$)")
        ax.set_ylabel("Intensity (a.u.)")
        ax.grid(True, alpha=0.3)

        safe_label = label.lower().replace(" = ", "").replace(" ", "")
        output = FIGURE_DIR / f"{safe_label}_negative_peak_1500.png"
        fig.savefig(output, dpi=300)
        print(f"Saved: {output}")


def main() -> None:
    FIGURE_DIR.mkdir(exist_ok=True)

    spectra = {}
    for label, path in REFERENCE_FILES.items():
        wavenumber, intensity = load_spectrum(path)
        spectra[label] = (wavenumber, intensity)

        wn_zoom, i_zoom = select_zoom(wavenumber, intensity)
        wn_min, i_min = local_minimum(wn_zoom, i_zoom)
        print(f"{label}: local minimum at {wn_min:.3f} cm^-1, intensity = {i_min:.6g}")

    plot_three_panels(spectra)
    plot_individual_figures(spectra)

    if ARGS.no_show:
        plt.close("all")
        print("Done. Open the PNG files in the figures folder to view the plots.")
    else:
        print("Opening interactive Matplotlib window. The PNG files were also saved.")
        plt.show()


if __name__ == "__main__":
    main()
