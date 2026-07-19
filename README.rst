A Correction Method for Crack Area Overestimation in Phase-Field Fracture
=========================================================================

.. image:: https://raw.githubusercontent.com/CastillonMiguel/A-Correction-Method-for-Crack-Area-Overestimation-in-Phase-Field-Fracture/main/docs/source/_static/logo_name.png
   :target: https://DoubleGradientCorrectionMethod.readthedocs.io/en/latest/
   :alt: A Correction Method for Crack Area Overestimation in Phase-Field Fracture

.. image:: https://readthedocs.org/projects/DoubleGradientCorrectionMethod/badge/?version=latest
    :target: https://DoubleGradientCorrectionMethod.readthedocs.io/en/latest/
    :alt: Documentation Status

Repository code
---------------
The code in this repository is the same version used for the paper `https://arxiv.org/abs/2605.03731 <https://arxiv.org/abs/2605.03731>`_. For a more visual and faster experience we recommend using the generated documentation, which provides interactive views and graphs: `Documentation and interactive views <https://doublegradientcorrectionmethod.readthedocs.io/en/latest/>`_.

Overview
--------
Phase-field fracture models are known to overestimate the crack area, a discrepancy that affects the accuracy of fracture predictions. This issue stems from the diffuse crack representation and numerical artifacts, such as strain localization, where the phase-field variable artificially saturates across finite elements.

Existing correction strategies, including mesh-dependent factors and skeletonization algorithms, have limitations. Mesh-based corrections are often unreliable for unstructured meshes, while skeletonization can be complex and inaccurate for intricate crack topologies, especially in three dimensions.

This paper introduces a correction framework to address this overestimation. Our approach is founded on the principle of energy equipartition, where the energy contributions from the phase-field and its gradient are equal as the length-scale parameter approaches zero. Since numerical artifacts primarily affect the phase-field term while leaving the gradient term largely unperturbed, we propose that the crack area can be approximated as twice the gradient-dependent energy. This method is inherently mesh-independent and readily applicable to the entire domain, including 3D simulations.

.. highlights::

    - **Novel Correction Method**: Introduces a new method to correct the overestimation of crack area in phase-field fracture simulations, a common issue that affects the accuracy of physical quantities.
    - **Energy Equipartition Principle**: The correction is based on the analytical observation that energy from the phase-field and its gradient are equal. It approximates the crack area as twice the gradient-dependent energy, which is unaffected by numerical artifacts.
    - **Mesh-Independent and 3D-Ready**: The proposed method is inherently mesh-independent and easily applicable to 3D simulations, avoiding the complexity of alternative techniques like skeletonization.
    - **Improved Physical Predictions**: Effectively mitigates the non-physical peak force artifact in force-displacement curves, leading to more accurate and conservative load predictions that converge with mesh refinement.
    - **Robust and Versatile**: The method shows less sensitivity to mesh resolution compared to other corrections and is adaptable to various phase-field models (e.g., AT1 and AT2).
    - **Computationally Efficient**: The correction adds no significant computational cost, as it relies on energy quantities already computed during the simulation.

This repository is designed to ensure complete reproducibility of the results by providing all simulation data, parameter sets, meshes, and detailed numerical configurations.

.. code:: latex

    @misc{castillon_dgcm2026,
        title={A Correction Method for Crack Area Overestimation in Phase-Field Fracture}, 
        author={M. Castillón and J. Segurado and I. Romero},
        year={2026},
        eprint={2605.03731},
        archivePrefix={arXiv},
        primaryClass={cond-mat.mtrl-sci},
        url={https://arxiv.org/abs/2605.03731}, 
    }

PhaseFieldX
-----------
All simulations in this work were produced with the open-source PhaseFieldX package.
Implementation details, examples and the API documentation can be found at:

- Project repository: `PhaseFieldX on GitHub <https://github.com/CastillonMiguel/phasefieldx>`_
- Documentation: `PhaseFieldX documentation <https://phasefieldx.readthedocs.io>`_
- Software paper (JOSS): `Castillón et al., JOSS (doi:10.21105/joss.07307) <https://doi.org/10.21105/joss.07307>`_

See the repository examples and the documentation for instructions to reproduce the simulations and to inspect the model implementations.