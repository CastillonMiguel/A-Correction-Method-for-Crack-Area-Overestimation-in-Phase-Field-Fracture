.. _ref_examples_phase_field_central_crack_3d:

Phase-field: Central cracked specimen 3D
----------------------------------------

This section presents the three-dimensional phase-field fracture simulation of the central
cracked tension specimen, used in the paper to demonstrate that the
**Double Gradient Correction Method (DGCM)** is directly applicable to 3D problems without
any modification to its formulation.

The geometry is the same as the 2D benchmark (see :ref:`ref_examples_phase_field_central_crack`),
but extruded to a thickness of :math:`t = 0.05` mm. Due to the left-right symmetry of the
problem, only half of the specimen (:math:`x \geq -0.5` mm) is modeled in 3D.

Unlike the 2D benchmarks, **four** correction approaches are compared here. Because computing
an exact 3D LEFM analytical solution for the crack area is not straightforward, the
skeletonization method serves as the reference:

- **No correction** — uncorrected phase-field integral :math:`\Gamma[\phi]`.
- **Bourdin** — element size-based correction :math:`\mathcal{F} = 1 + h/(c_0 l)`.
- **DGCM** — Double Gradient Correction Method (proposed).
- **Skeleton** — crack area measured from thresholded phase-field images
  (:math:`\phi > 0.95`) via spline-based skeletonization.

**Boundary conditions (half-symmetry model)**

.. code-block::

    #           u/\/\/\/\/\/\       u/\/\/\ 
    #            ||||||||||||        ||||||
    #            *----------*    o|\ *-----*
    #            |          |    o|/ |     |
    #            |    2a    |    o|\ | a   |
    #            |   ----   |    o|/ *--   |
    #            |          |    o|\ |     |
    #            |          |    o|/ |     |
    #            *----------*        *-----*
    #            ||||||||||||         /_\/_\ 
    #     |Y    u\/\/\/\/\/\/          oo oo 
    #     |
    #     *---X

- Bottom face (:math:`y = -3` mm): fixed in :math:`y` and :math:`z`.
- Left faces (:math:`x = -0.5` mm): fixed in :math:`x` (symmetry plane).
- Top face (:math:`y = 3` mm): upward traction (energy-controlled scheme).

**Material properties**

+------+---------+--------+
|      | Value   | Units  |
+======+=========+========+
| E    | 210     | kN/mm² |
+------+---------+--------+
| ν    | 0.3     | —      |
+------+---------+--------+
| Gc   | 0.0027  | kN/mm  |
+------+---------+--------+

**Simulation parameters**

+-------+------------------+------------------+-------------+------------------+-------------------------------+
| Model | :math:`l` (mm)   | :math:`h` (mm)   | :math:`l/h` | :math:`t` (mm)   | Results folder                |
+=======+==================+==================+=============+==================+===============================+
| AT2   | 0.00625          | 0.0025           | 2.5         | 0.05             | ``results_simulation_3d``     |
+-------+------------------+------------------+-------------+------------------+-------------------------------+
| AT1   | 0.00625          | 0.0025           | 2.5         | 0.05             | ``results_simulation_3d_AT1`` |
+-------+------------------+------------------+-------------+------------------+-------------------------------+

**Files in this folder**

- :ref:`ref_central_cracked_3d_simulation_at2` — AT2 simulation, post-processing, and
  comparison of all four correction methods.
- :ref:`ref_central_cracked_3d_simulation` — AT1 simulation and comparison.
- :ref:`ref_skeleton_3d` — skeletonization pipeline for AT2 results.
- :ref:`ref_skeleton_3d_at1` — skeletonization pipeline for AT1 results.
