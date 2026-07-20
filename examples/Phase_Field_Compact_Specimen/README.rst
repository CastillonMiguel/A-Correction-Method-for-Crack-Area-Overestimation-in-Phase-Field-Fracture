.. _ref_examples_phase_field_compact_specimen:

Phase-field: Compact specimen
=============================

This section presents phase-field fracture simulations of a modified compact tension (CT)
specimen taken from :footcite:t:`example_Wagner2018_phd_thesis`. The specimen contains
internal circular voids whose vertical position, controlled by the parameter :math:`H`, deflects
the crack along a **curvilinear path**. This benchmark is used in the paper to validate the
**Double Gradient Correction Method (DGCM)** for complex, non-straight crack trajectories where
the Bourdin correction — derived from a 1D idealization — is expected to be less accurate.

All three simulations use the **AT2** regularization with an isotropic degradation function.
Four correction methods are applied and compared in each case:

- **Reference** — uncorrected phase-field integral.
- **Bourdin** — element size-based correction :math:`\mathcal{F} = 1 + h/(c_0 l)` with :math:`c_0 = 2`.
- **DGCM** — Double Gradient Correction Method (proposed).
- **Skeleton** — crack path measured from thresholded phase-field images via
  skeletonization and spline fitting, used as the reference for curvilinear cracks.

**Material properties and simulation parameters**

+------+---------+--------+
|      | Value   | Units  |
+======+=========+========+
| E    | 211     | kN/mm² |
+------+---------+--------+
| ν    | 0.3     | —      |
+------+---------+--------+
| Gc   | 0.073   | kN/mm  |
+------+---------+--------+
| l    | 0.1     | mm     |
+------+---------+--------+
| h    | 0.04    | mm     |
+------+---------+--------+
| l/h  | 2.5     | —      |
+------+---------+--------+
| b    | 40      | mm     |
+------+---------+--------+
| a0   | 8       | mm     |
+------+---------+--------+
| B    | 3.20    | mm     |
+------+---------+--------+

The parameter :math:`H` shifts the vertical position of the internal voids. For :math:`H = 0`
the specimen has no voids and the crack propagates straight. For :math:`H \neq 0` the voids
are offset from the neutral axis and deflect the crack, producing a curved fracture path.

**Specimen configurations**

.. table:: Compact specimen configurations with varying void offset :math:`H` and hole presence.
    :name: tab:compact_specimen_simulation_configurations

    +-----------------------------------------------------+-------------------------------+-------------------+----------------------------------------------+
    | Specimen                                            | :math:`H` (void offset)       | Voids             | Crack path                                   |
    +=====================================================+===============================+===================+==============================================+
    | :ref:`ref_phase_field_compact_specimen_1_H00`       | :math:`H = 0.0` mm            | No                | Straight                                     |
    +-----------------------------------------------------+-------------------------------+-------------------+----------------------------------------------+
    | :ref:`ref_phase_field_compact_specimen_2_H16`       | :math:`H = +1.6` mm           | Yes               | Curved (voids shifted in one direction)      |
    +-----------------------------------------------------+-------------------------------+-------------------+----------------------------------------------+
    | :ref:`ref_phase_field_compact_specimen_4_Hminus16`  | :math:`H = -1.6` mm           | Yes               | Curved (voids shifted in opposite direction) |
    +-----------------------------------------------------+-------------------------------+-------------------+----------------------------------------------+

.. footbibliography::
