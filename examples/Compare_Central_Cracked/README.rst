.. _ref_examples_compare_central_cracked:

Comparison: Central cracked
---------------------------

This section collects the post-processing scripts used to generate the figures of the paper for
the central cracked tension benchmark. Each script loads pre-computed results from the
:ref:`ref_examples_phase_field_central_crack` (AT2) and
:ref:`ref_examples_phase_field_central_crack_at1` (AT1) simulation folders, applies the three
correction approaches — **Reference** (no correction), **Bourdin**, and **DGCM** — and produces
publication-quality plots.

The scripts are organized as follows:

- :ref:`ref_compare_pff_lefm` — Validates a single simulation against the LEFM analytical solution,
  illustrating correction factor, force–displacement, and stiffness–crack-length curves.
- :ref:`ref_compare_lenght_scale` — Compares the DGCM correction factor and structural stiffness
  across all AT2 convergence simulations (Study 1, Groups A and B).
- :ref:`ref_compare_lenght_scale_at1` — Same comparison for the AT1 convergence study.
- :ref:`ref_compare_save_data` — Pre-processing script that extracts scalar convergence metrics
  (peak force, crack length at given stiffness, etc.) from all 11 AT2 simulations and saves
  them as tabular data used by the subsequent convergence plots.
- :ref:`ref_convergence_l_constant_lh_2_5` — Convergence of the DGCM correction factor with
  respect to :math:`l` at constant :math:`l/h = 2.5` (log–log plot).
- :ref:`ref_convergence_l_constant_lh_2_5_4_0` — Joint convergence of peak force and crack length
  with respect to :math:`l` for both :math:`l/h = 2.5` and :math:`l/h = 4.0`.
- :ref:`ref_compare_lh_constant_length_scale` — Effect of mesh refinement at fixed
  :math:`l = 0.0025` mm, showing how the three methods behave as :math:`h/l \to 0`.
