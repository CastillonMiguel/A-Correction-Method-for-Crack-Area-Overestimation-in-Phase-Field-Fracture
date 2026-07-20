.. _ref_examples_phase_field_central_crack_at1:

Central cracked specimen (AT1)
------------------------------

These simulations correspond to the central crack tension benchmark used in the paper to validate
the **Double Gradient Correction Method (DGCM)** for the **AT1** regularization
(:math:`\alpha(\phi) = \phi`, :math:`c_0 = 8/3`). The specimen is a square plate with a central
crack of half-length :math:`a_0 = 0.5` mm under remote vertical tension. Thanks to the double
symmetry of the problem, only one quarter of the domain is modeled.

Unlike the AT2 model, the AT1 phase-field has compact support: it decays to zero within a finite
distance proportional to :math:`l`. Once this compact support is fully developed (i.e.
:math:`l/a \leq 0.5`), energy equipartition holds exactly without needing :math:`l \to 0`.
The lower bound :math:`\phi \geq 0` is enforced via penalization with parameter :math:`\rho`.

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

.. _table_properties_label_at1:

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

**Convergence study — constant** :math:`l/h = 2.5`

The length scale :math:`l` is progressively halved while the ratio :math:`l/h = 2.5` is kept
fixed, testing whether each correction method converges to the analytical crack length as
:math:`l \to 0`. The normalized parameters :math:`\alpha = l\,/\,0.0125` and
:math:`\theta = h\,/\,0.005` indicate the refinement level relative to the coarsest simulation
and are used as such in the paper’s figures.

+-------------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| #                       | :math:`\alpha` | :math:`\theta` | Length scale :math:`l` (mm)   | Mesh size :math:`h` (mm) | :math:`l/h` |
+=========================+================+================+===============================+==========================+=============+
| :ref:`ref_cc_sim1_at1`  | 1.0            | 1.0            | 0.012500                      | 0.005000                 | 2.5         |
+-------------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim2_at1`  | 0.2            | 0.2            | 0.002500                      | 0.001000                 | 2.5         |
+-------------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim3_at1`  | 0.1            | 0.1            | 0.001250                      | 0.000500                 | 2.5         |
+-------------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
