# FTIR Spectroscopy Analysis of BeO and Stainless Steel

## Overview

This repository contains the complete analysis workflow for the FTIR spectroscopy experiment (Praktikum M2.7).

The project investigates the optical properties of:

- Beryllium Oxide (BeO)
- Stainless Steel samples (n3 and n6)

using Fourier Transform Infrared (FTIR) spectroscopy.

The analysis includes:

- Zero-filling comparison
- Apodization comparison
- BeO reflectivity analysis
- Phonon identification
- Lorentz dielectric fitting
- Optical constants extraction
- Drude and Drude-Lorentz fitting
- Electrical conductivity analysis
- Carrier density estimation

---

## Repository Structure

```text
.
├── analysis_51_zerofilling.py
├── analysis_52_apodization.py
├── analysis_53_beo_overlay.py
├── analysis_53_beo_reflectivity.py
├── analysis_53_phonon_markers.py
├── analysis_54_dielectric_fit.py
├── analysis_55_beo_45deg.py
│
├── analysis_61_steel_overlay.py
├── analysis_62_steel_drude_fit.py
├── analysis_63_steel_drude_lorentz.py
├── analysis_64_steel_carrier_density.py
│
├── figures/
├── results/
└── *.dat
```

---

## Experimental Data

The repository contains FTIR spectra for:

### BeO

- BeO_0pol_8zff_BH3_2.dat
- BeO_45pol_8zff_BH3.dat
- BeO_90pol_8zff_BH3.dat

### Reference Measurements

- Ref_0pol_8zff_BH3.dat
- Ref_45pol_8zff_BH3.dat
- Ref_90pol_8zff_BH3.dat

### Stainless Steel

- steel_n3_nopol_8zff_BH3.dat
- steel_n6_nopol_8zff_BH3.dat

The spectral range covers approximately:

```text
500 – 10000 cm⁻¹
```

---

# Analysis Workflow

## 1. Zero Filling

**Script**

```bash
python analysis_51_zerofilling.py
```

Purpose:

- Compare different zero-filling factors
- Investigate spectral interpolation
- Analyze the peak near 1500 cm⁻¹

---

## 2. Apodization

**Script**

```bash
python analysis_52_apodization.py
```

Purpose:

- Compare Boxcar, Triangular, and Blackman-Harris windows
- Evaluate effects on peak shape and spectral resolution

---

## 3. BeO Reflectivity Analysis

### Overlay of Polarizations

```bash
python analysis_53_beo_overlay.py
```

Compares:

- 0°
- 45°
- 90°

polarization spectra.

### Reflectivity Inspection

```bash
python analysis_53_beo_reflectivity.py
```

Examines sample and reference spectra.

### Phonon Marker Extraction

```bash
python analysis_53_phonon_markers.py
```

Determines characteristic phonon frequencies and Reststrahlen-band boundaries.

---

## 4. Dielectric Function Fitting

**Script**

```bash
python analysis_54_dielectric_fit.py
```

Fits the BeO spectra using a Lorentz oscillator model:

\[
\varepsilon(\omega)
=
\varepsilon_{\infty}
+
\frac{S}
{\omega_{TO}^{2}-\omega^{2}-i\gamma\omega}
\]

Extracted quantities:

- Reflectivity
- Dielectric function ε₁(ω)
- Dielectric function ε₂(ω)
- Refractive index n(ω)
- Extinction coefficient k(ω)

---

## 5. 45° Polarization Analysis

**Script**

```bash
python analysis_55_beo_45deg.py
```

Studies the mixed-polarization response and compares it to the principal crystal axes.

---

## 6. Stainless Steel Analysis

### Spectrum Comparison

```bash
python analysis_61_steel_overlay.py
```

Compares the spectra of steel samples:

- n3
- n6

### Drude Fit

```bash
python analysis_62_steel_drude_fit.py
```

Fits the metallic response using the classical Drude model.

### Drude-Lorentz Fit

```bash
python analysis_63_steel_drude_lorentz.py
```

Fits the spectra using:

- Free-electron Drude contribution
- Additional Lorentz oscillator

and extracts the optical response.

### Carrier Density Calculation

```bash
python analysis_64_steel_carrier_density.py
```

Calculates:

\[
\sigma_{dc}
=
\frac{Ne^2}{m_e\gamma}
\]

and estimates the free charge carrier density.

---

# Main Results

## BeO Dielectric Fit

| Polarization | ε∞ | νTO (cm⁻¹) | γ (cm⁻¹) |
|-------------|------:|------:|------:|
| 0° | 2.9875 | 720.99 | 7.60 |
| 90° | 3.1009 | 676.08 | 7.45 |

These results demonstrate the anisotropic optical response of BeO and the polarization dependence of the transverse optical phonon frequencies.

---

## Stainless Steel Carrier Density

| Sample | Carrier Density (cm⁻³) |
|----------|--------------------:|
| n3 | 4.86 × 10²⁰ |
| n6 | 4.71 × 10²² |

The n6 sample exhibits significantly stronger metallic behavior and a substantially larger free-carrier concentration than n3.

---

# Requirements

Install the required Python packages:

```bash
pip install numpy scipy matplotlib pandas
```

---

# Output

The scripts automatically generate:

```text
figures/
```

for plots and visualizations, and

```text
results/
```

for fitted parameters and derived physical quantities.

---

# License

This repository is intended for academic and educational use.

---

# Author

**Amay Dusar**

FTIR Spectroscopy Analysis — Praktikum M2.7
