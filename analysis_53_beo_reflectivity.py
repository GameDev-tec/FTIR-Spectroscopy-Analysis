import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path.cwd()

FILES = {
    "0°": (
        ROOT / "BeO_0pol_8zff_BH3_2.dat",
        ROOT / "Ref_0pol_8zff_BH3.dat",
    ),
    "45°": (
        ROOT / "BeO_45pol_8zff_BH3.dat",
        ROOT / "Ref_45pol_8zff_BH3.dat",
    ),
    "90°": (
        ROOT / "BeO_90pol_8zff_BH3.dat",
        ROOT / "Ref_90pol_8zff_BH3.dat",
    ),
}

WN_MIN = 500
WN_MAX = 1300


def load_spectrum(path):
    data = np.loadtxt(path)

    wn = data[:, 0]
    intensity = data[:, 1]

    order = np.argsort(wn)

    return wn[order], intensity[order]


def calculate_reflectivity(sample_file, reference_file):

    wn_sample, sample = load_spectrum(sample_file)
    wn_ref, ref = load_spectrum(reference_file)

    if not np.allclose(wn_sample, wn_ref):
        raise ValueError(
            f"Grid mismatch between {sample_file.name} "
            f"and {reference_file.name}"
        )

    print("\n" + "=" * 60)
    print(sample_file.name)

    print(
        f"Sample  : min={sample.min():.6f} "
        f"max={sample.max():.6f}"
    )

    print(
        f"Reference: min={ref.min():.6f} "
        f"max={ref.max():.6f}"
    )

    min_ref_idx = np.argmin(ref)

    print(
        f"Smallest reference value = "
        f"{ref[min_ref_idx]:.10f}"
    )

    print(
        f"Occurs at "
        f"{wn_ref[min_ref_idx]:.2f} cm^-1"
    )

    # Raw division
    eps = 1e-12
    R = sample / (ref + eps)

    print(
        f"Reflectivity estimate:"
        f" min={R.min():.3f}"
        f" max={R.max():.3f}"
    )

    return wn_sample, sample, ref, R


fig, axes = plt.subplots(
    3,
    1,
    figsize=(10, 10),
    sharex=True
)

for ax, (pol, files) in zip(
    axes,
    FILES.items()
):

    sample_file, ref_file = files

    wn, sample, ref, R = calculate_reflectivity(
        sample_file,
        ref_file
    )

    mask = (
        (wn >= WN_MIN)
        & (wn <= WN_MAX)
    )

    wn = wn[mask]
    sample = sample[mask]
    ref = ref[mask]
    R = R[mask]

    ax.plot(
    wn,
    sample,
    linewidth=1.5,
    label=f"BeO {pol}"
)

    ax.plot(
        wn,
        ref,
        linewidth=1.5,
        label="Reference signal"
    )

    ax.set_title(f"{pol}")
    ax.grid(True)
    ax.legend()

axes[-1].set_xlabel(
    "Wavenumber (cm$^{-1}$)"
)

fig.suptitle(
    "Raw BeO and Reference Signals"
)

plt.tight_layout()
plt.show()