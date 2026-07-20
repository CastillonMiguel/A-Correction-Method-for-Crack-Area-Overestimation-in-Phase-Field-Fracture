.. _ref_examples_phase_field_central_crack:

Central cracked specimen (AT2)
------------------------------

These simulations correspond to the central crack tension benchmark used in the paper to validate
the **Double Gradient Correction Method (DGCM)**. The specimen is a square plate with a central
crack of half-length :math:`a_0 = 0.5` mm under remote vertical tension. Thanks to the double
symmetry of the problem, only one quarter of the domain is modeled. The **AT2** regularization
(:math:`\alpha(\phi) = \phi^2`, :math:`c_0 = 2`) is used throughout.

The compliance of the specimen has an analytical LEFM solution, which provides an exact reference
for the true crack length. Each simulation compares three approaches for computing the crack area:
the uncorrected phase-field integral, the Bourdin mesh-dependent correction, and the proposed DGCM.

**Problem setup**

.. code-block::

   #           u/\/\/\/\/\/\       u/\/\/\/\/\/\ 
   #            ||||||||||||        ||||||||||||
   #            *----------*    o|\ *----------*
   #            |          |    o|/ |          |
   #            | 2a=1.0   |    o|\ | a=a0     |
   #            |   ----   |    o|\ *----------*
   #            |          |    o|/      /_\/_\ 
   #            |          |            oo oo oo
   #            *----------*
   #            /_\/_\/_\/_\       
   #     |Y    /////////////
   #     |
   #     *---X

- Domain (quarter model): :math:`1.0 \times 3.0` mm, discretized with quadrilateral elements.
- Boundary conditions: bottom edge (:math:`x \geq a_0`, :math:`y = 0`) fixed in :math:`y`; left
  edge (:math:`x = 0`) fixed in :math:`x` (symmetry); vertical traction applied on the top edge.
- Initial crack: Dirichlet condition :math:`\phi = 1` is not set explicitly; the crack is
  represented by leaving the bottom edge free for :math:`x < a_0`.

.. _table_properties_label:

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

**Summary of all simulations**

The normalized parameters :math:`\alpha = l\,/\,0.0125` and :math:`\theta = h\,/\,0.005` indicate
the refinement level relative to the coarsest simulation and are used as such in the paper's figures.

+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| #                   | :math:`\alpha` | :math:`\theta` | Length scale :math:`l` (mm)   | Mesh size :math:`h` (mm) | :math:`l/h` |
+=====================+================+================+===============================+==========================+=============+
| :ref:`ref_cc_sim1`  | 1.0            | 1.0            | 0.012500                      | 0.005000                 | 2.5         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim2`  | 0.2            | 0.2            | 0.002500                      | 0.001000                 | 2.5         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim3`  | 0.1            | 0.1            | 0.001250                      | 0.000500                 | 2.5         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim4`  | 0.05           | 0.05           | 0.000625                      | 0.000250                 | 2.5         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim5`  | 1.0            | 0.625          | 0.012500                      | 0.003125                 | 4.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim6`  | 0.2            | 0.125          | 0.002500                      | 0.000625                 | 4.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim7`  | 0.1            | 0.0625         | 0.001250                      | 0.0003125                | 4.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim8`  | 0.05           | 0.03125        | 0.000625                      | 0.00015625               | 4.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim9`  | 0.2            | 0.1666         | 0.002500                      | 0.000833                 | 3.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim10` | 0.2            | 0.1            | 0.002500                      | 0.000500                 | 5.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim11` | 0.2            | 0.0833         | 0.002500                      | 0.0004166                | 6.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+

**Study 1 — Convergence as** :math:`l \to 0` **(constant** :math:`l/h` **ratio)**

The length scale :math:`l` is progressively halved while the ratio :math:`l/h` is kept fixed,
testing whether each correction method converges to the analytical crack length as :math:`l \to 0`.
The normalized refinement factor :math:`\alpha = l / 0.0125` indicates the level of refinement
relative to the coarsest simulation.

*Group A —* :math:`l/h = 2.5`:

+---------------------+---------------------------+---------------------------+-------------+
| Simulation          | Length scale :math:`l` (mm)| Mesh size :math:`h` (mm)  | :math:`l/h` |
+=====================+===========================+===========================+=============+
| :ref:`ref_cc_sim1`  | 0.012500                  | 0.005000                  | 2.5         |
+---------------------+---------------------------+---------------------------+-------------+
| :ref:`ref_cc_sim2`  | 0.002500                  | 0.001000                  | 2.5         |
+---------------------+---------------------------+---------------------------+-------------+
| :ref:`ref_cc_sim3`  | 0.001250                  | 0.000500                  | 2.5         |
+---------------------+---------------------------+---------------------------+-------------+
| :ref:`ref_cc_sim4`  | 0.000625                  | 0.000250                  | 2.5         |
+---------------------+---------------------------+---------------------------+-------------+

*Group B —* :math:`l/h = 4.0`:

+---------------------+---------------------------+---------------------------+-------------+
| Simulation          | Length scale :math:`l` (mm)| Mesh size :math:`h` (mm)  | :math:`l/h` |
+=====================+===========================+===========================+=============+
| :ref:`ref_cc_sim5`  | 0.012500                  | 0.003125                  | 4.0         |
+---------------------+---------------------------+---------------------------+-------------+
| :ref:`ref_cc_sim6`  | 0.002500                  | 0.000625                  | 4.0         |
+---------------------+---------------------------+---------------------------+-------------+
| :ref:`ref_cc_sim7`  | 0.001250                  | 0.0003125                 | 4.0         |
+---------------------+---------------------------+---------------------------+-------------+
| :ref:`ref_cc_sim8`  | 0.000625                  | 0.00015625                | 4.0         |
+---------------------+---------------------------+---------------------------+-------------+

**Study 2 — Effect of the** :math:`l/h` **ratio (fixed** :math:`l`\ **)**

The length scale is fixed at :math:`l = 0.0025` mm while the mesh size :math:`h` is varied to
achieve different :math:`l/h` ratios. This isolates the influence of mesh density on the
overestimation of the crack area and on the performance of the correction methods. Simulations 2
and 6 (from Study 1) complete the set at :math:`l/h = 2.5` and :math:`4.0`, respectively.

+----------------------+---------------------------+---------------------------+-------------+
| Simulation           | Length scale :math:`l` (mm)| Mesh size :math:`h` (mm)  | :math:`l/h` |
+======================+===========================+===========================+=============+
| :ref:`ref_cc_sim9`   | 0.002500                  | 0.000833                  | 3.0         |
+----------------------+---------------------------+---------------------------+-------------+
| :ref:`ref_cc_sim10`  | 0.002500                  | 0.000500                  | 5.0         |
+----------------------+---------------------------+---------------------------+-------------+
| :ref:`ref_cc_sim11`  | 0.002500                  | 0.0004166                 | 6.0         |
+----------------------+---------------------------+---------------------------+-------------+

