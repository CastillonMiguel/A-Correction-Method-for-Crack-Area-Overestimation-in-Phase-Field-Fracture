.. _ref_fem_error:

Crack Surface FEM Error
------------------------

This directory studies the finite element discretization error in the crack
surface density functional for the AT1 and AT2 regularization models.

The one-dimensional bar problem (half-domain :math:`[0, a]` with :math:`\phi=1`
at the symmetry plane representing the crack) is solved with FEM using linear
elements for a range of mesh resolutions. The relative error in the computed
energy components :math:`\Gamma`, :math:`\Gamma_\phi`, and
:math:`\Gamma_{\nabla\phi}` is plotted as a function of the resolution ratio
:math:`l/h`.

With parameters :math:`l=0.1`\ mm and :math:`a=1.0`\ mm (:math:`a/l=10`,
boundary effects negligible), the reference values are :math:`\Gamma=1.0`
and :math:`\Gamma_\phi = \Gamma_{\nabla\phi} = 0.5`.

* **plot_error_at2.py:** Convergence study for the AT2 regularization.
* **plot_error_at1.py:** Convergence study for the AT1 regularization.
  A penalization approach with :math:`\rho=10^8` is used to enforce
  :math:`\phi \ge 0`, as required by the AT1 model.

