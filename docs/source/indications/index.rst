Indications
===========

* **Phase-Field Simulations:** This component involves simulations using phase-field, energy-controlled schemes. The results are saved in files with the ``.pff`` extension for comparison with other methods. These files contain information such as forces, energies, crack area, and other relevant quantities at each simulation step.

    Three different correction methods are applied to the phase-field results, generating separate ``.pff`` files for each method:

    * ``results.pff``: Uncorrected results (equivalent to a constant correction factor of 1).
    * ``results_dgcm.pff``: Results using the Double Gradient Correction Method (DGCM).
    * ``results_bourdin.pff``: Results using the Bourdin method.
    * ``results_skeleton.pff``: Results using the Skeletonization method.

* **Reference Data:** This component consists of additional data from articles or other references, saved in files with the ``.databib`` extension.

For all simulations and calculations, the following unit system is considered:

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
| Poisson's ratio  $\nu$              | dimensionless                               |
+-------------------------------------+---------------------------------------------+
| Energy release rate: $G$            | $kN/mm$                                     |
+-------------------------------------+---------------------------------------------+
| Crack length                        | $mm$                                        |
+-------------------------------------+---------------------------------------------+
| Crack area                          | $mm^2$                                      |
+-------------------------------------+---------------------------------------------+
