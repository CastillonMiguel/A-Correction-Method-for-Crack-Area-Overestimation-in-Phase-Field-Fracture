Indications
===========

The simulation results and reference data are organized into two components:

* **Phase-Field Fracture Results:** Simulation results saved in files with the ``.pff`` extension, containing quantities such as forces, energies, crack area, and other relevant data at each simulation step.

    Three different correction methods are applied to the phase-field results, generating separate ``.pff`` files for each method:

    * ``results.pff``: Uncorrected results (equivalent to a constant correction factor of 1).
    * ``results_dgcm.pff``: Results using the Double Gradient Correction Method (DGCM).
    * ``results_bourdin.pff``: Results using the Bourdin method.
    * ``results_skeleton.pff``: Results using the Skeletonization method.

* **Reference Data:** Additional data from articles or other references, saved in files with the ``.databib`` extension.

For all simulations and calculations, the following unit system is used:

+-------------------------------------+---------------------------------------------+
| **Quantity**                        | **Unit**                                    |
+=====================================+=============================================+
| Length                              | $mm$                                        |
+-------------------------------------+---------------------------------------------+
| Force: $P$                          | $kN$                                        |
+-------------------------------------+---------------------------------------------+
| Area                                | $mm^2$                                      |
+-------------------------------------+---------------------------------------------+
| Energy                              | $kN \cdot mm$                               |
+-------------------------------------+---------------------------------------------+
| Young's modulus: $E$                | $kN/mm^2$                                   |
+-------------------------------------+---------------------------------------------+
| Poisson's ratio: $\nu$              | dimensionless                               |
+-------------------------------------+---------------------------------------------+
| Critical energy release rate: $G_c$ | $kN/mm$                                     |
+-------------------------------------+---------------------------------------------+
| Crack length                        | $mm$                                        |
+-------------------------------------+---------------------------------------------+
| Crack area                          | $mm^2$                                      |
+-------------------------------------+---------------------------------------------+
