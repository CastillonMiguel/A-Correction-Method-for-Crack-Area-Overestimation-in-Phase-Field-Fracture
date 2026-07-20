.. _ref_theory_overestimation:

Crack Surface Overestimation
-----------------------------

This directory analyzes the overestimation of the crack surface area that arises
in phase-field fracture simulations due to **strain localization**. This numerical
artifact causes the phase-field variable to artificially saturate at :math:`\phi = 1`
across an entire finite element of size :math:`h`, distorting the ideal diffuse
profile and increasing the computed crack surface energy in the one dimensional case
by :math:`h / (c_0 l)`, where :math:`c_0` is a model-dependent constant 
and :math:`l` is the length-scale parameter.

The three scripts use the one-dimensional analytical solution of the crack surface
density functional to quantify this overestimation for the AT1 and AT2 regularization
models:

* **plot_profiles_at1_at2.py:** Plots the phase-field profile :math:`\phi(x)` and
  its gradient :math:`\phi'(x)`, comparing the ideal analytical solution with the
  strain-localized profile in which :math:`\phi = 1` is maintained over the central
  element.

* **plot_energy_at2.py:** Plots the energy contributions of the AT2 model as a
  function of :math:`l/a`, comparing the theoretical values with the
  strain-localized energies for several mesh sizes :math:`h/a`.

* **plot_energy_at1.py:** Same as above, but for the AT1 regularization model.
