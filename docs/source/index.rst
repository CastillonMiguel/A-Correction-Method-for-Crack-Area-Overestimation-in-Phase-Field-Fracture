.. raw:: html

    <style type="text/css">
        .big-font {font-size: var(--pst-font-size-h2); color: var(--pst-color-primary)}
    </style>


.. .. line-break::

.. rst-class:: font-weight-bold big-font

        A Correction Method for Crack Area Overestimation in Phase-Field Fracture


.. raw:: html

    <div style="text-align: center; margin: 24px 0;">
        <img src="_static/logo_name.png"
             alt="Logo"
             style="max-width: 800px; width: 100%; height: auto;">
    </div>

Phase-field fracture models are known to overestimate the crack area, a discrepancy that affects the accuracy of fracture predictions. This issue stems from the diffuse crack representation and numerical artifacts, such as strain localization, where the phase-field variable artificially saturates across finite elements.

Existing correction strategies, including mesh-dependent factors and skeletonization algorithms, have limitations. Mesh-based corrections are often unreliable for unstructured meshes, while skeletonization can be complex and inaccurate for intricate crack topologies, especially in three dimensions.

This paper introduces a correction framework to address this overestimation. Our approach is founded on the principle of energy equipartition, where the energy contributions from the phase-field and its gradient are equal as the length-scale parameter approaches zero. Since numerical artifacts primarily affect the phase-field term while leaving the gradient term largely unperturbed, we propose that the crack area can be approximated as twice the gradient-dependent energy. This method is inherently mesh-independent and readily applicable to the entire domain, including 3D simulations.

The proposed methodology is validated against benchmarks with analytical solutions and compared with established methods like skeletonization to demonstrate its accuracy. It is then applied to complex geometries with curvilinear crack paths and evaluated in a three-dimensional simulation.


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

All the files are provided in the following `GitHub Repository <https://github.com/CastillonMiguel/A-Correction-Method-for-Crack-Area-Overestimation-in-Phase-Field-Fracture>`_

Since the simulations were conducted using the open-source **PhaseFieldX** :footcite:t:`code_phasefieldx` library, the implementation details of the models can be found in the **PhaseFieldX** documentation and source code.

- GitHub Repository: `https://github.com/CastillonMiguel/phasefieldx <https://github.com/CastillonMiguel/phasefieldx>`_
- Documentation: `https://phasefieldx.readthedocs.io <https://phasefieldx.readthedocs.io>`_
- Paper: `https://doi.org/10.21105/joss.07307 <https://doi.org/10.21105/joss.07307>`_

The **PhaseFieldX** project is designed to simulate and analyze material behavior using phase-field models, which provide a continuous approximation of interfaces, phase boundaries, and discontinuities such as cracks. Leveraging the robust capabilities of *FEniCSx*, a renowned finite element framework for solving partial differential equations, this project facilitates efficient and precise numerical simulations. It supports a wide range of applications, including phase-field fracture, solidification, and other complex material phenomena, making it an invaluable resource for researchers and engineers in materials science.

.. image:: _static/logo_phasefieldx.png
   :width: 600px
   :align: center

.. footbibliography::

.. toctree::

   indications/index
   auto_examples/index
   references/index.rst
   related/index.rst
