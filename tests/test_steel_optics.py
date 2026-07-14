import numpy as np
import pytest

from steel_optics import (
    drude_lorentz_dielectric,
    load_spectrum,
    real_drude_conductivity,
    reflectivity_from_dielectric,
)


def test_load_spectrum_sorts_wavenumbers_and_signal(tmp_path):
    path = tmp_path / "unsorted.dat"
    np.savetxt(path, [[3.0, 30.0], [1.0, 10.0], [2.0, 20.0]])

    wn, signal = load_spectrum(path)

    assert np.array_equal(wn, [1.0, 2.0, 3.0])
    assert np.array_equal(signal, [10.0, 20.0, 30.0])


def test_load_spectrum_rejects_single_column_data(tmp_path):
    path = tmp_path / "invalid.dat"
    np.savetxt(path, [1.0, 2.0, 3.0])

    with pytest.raises(ValueError, match="two columns"):
        load_spectrum(path)


def test_dielectric_function_has_positive_loss_for_passive_terms():
    nu = np.array([500.0, 1000.0, 3000.0])

    epsilon = drude_lorentz_dielectric(
        nu,
        eps_inf=3.0,
        plasma_drude=8000.0,
        gamma_drude=200.0,
        plasma_lorentz=3000.0,
        gamma_lorentz=250.0,
        nu_lorentz=200.0,
    )

    assert np.all(np.imag(epsilon) > 0.0)


def test_reflectivity_is_real_finite_and_bounded_for_passive_dielectric():
    nu = np.linspace(500.0, 5000.0, 50)
    epsilon = drude_lorentz_dielectric(
        nu,
        eps_inf=3.0,
        plasma_drude=8000.0,
        gamma_drude=200.0,
        plasma_lorentz=3000.0,
        gamma_lorentz=250.0,
        nu_lorentz=200.0,
    )

    reflectivity = reflectivity_from_dielectric(epsilon)

    assert np.isrealobj(reflectivity)
    assert np.all(np.isfinite(reflectivity))
    assert np.all((reflectivity >= 0.0) & (reflectivity <= 1.0))


def test_real_drude_conductivity_has_expected_dc_lorentzian_form():
    nu = np.array([0.0, 200.0, 1000.0])
    plasma = 8000.0
    gamma = 200.0

    conductivity = real_drude_conductivity(nu, plasma, gamma)

    assert np.all(np.isfinite(conductivity))
    assert conductivity[0] > conductivity[1] > conductivity[2] > 0.0

    epsilon_0_f_per_cm = 8.8541878128e-14
    c_cm_per_s = 2.99792458e10
    expected_dc = epsilon_0_f_per_cm * 2.0 * np.pi * c_cm_per_s * plasma**2 / gamma
    assert np.isclose(conductivity[0], expected_dc)
