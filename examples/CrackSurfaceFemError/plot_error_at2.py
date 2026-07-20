r"""
.. _ref_CrackSurfaceFemError_plot_convergence_at2:

FEM Discretization Error in the Crack Surface Density Functional: AT2
----------------------------------------------------------------------

This script evaluates the finite element discretization error in the crack
surface density functional for the AT2 regularization model.

The one-dimensional bar is solved on the half-domain :math:`[0, a]` with a
Dirichlet condition :math:`\phi=1` at the symmetry plane :math:`x=0`
(representing the crack) and a zero-flux condition at :math:`x=a`. Linear
Lagrange elements are used for the phase-field approximation.

With :math:`l=0.1`\ mm and :math:`a=1.0`\ mm (:math:`a/l=10`), boundary
effects are negligible and the reference values are :math:`\Gamma=1.0`,
:math:`\Gamma_\phi=\Gamma_{\nabla\phi}=0.5`. Mesh divisions from 1 to 99
elements are tested, sweeping :math:`l/h` from ~0.1 to ~10. The relative
error in each energy component is plotted on a log-log scale. The gradient
energy :math:`\Gamma_{\nabla\phi}` is consistently more accurate than the
phase-field energy :math:`\Gamma_\phi`; at :math:`l/h \approx 2`, the total
energy error is approximately :math:`1\%`.

"""

###############################################################################
# Import necessary libraries
# --------------------------
import numpy as np

import pyvista as pv
import dolfinx
import mpi4py
import os


###############################################################################
# Import from phasefieldx package
# -------------------------------
from phasefieldx.Element.Phase_Field.Input import Input
from phasefieldx.Element.Phase_Field.solver.solver import solve
from phasefieldx.Boundary.boundary_conditions import bc_phi, get_ds_bound_from_marker


###############################################################################
# Parameters definition
# ---------------------
# An input object is created with the simulation parameters.
#
# - `l`: Length scale parameter, set to :math:`l = 0.1`\ mm. With
#   :math:`a = 1.0`\ mm this gives a ratio :math:`a/l = 10`, so boundary
#   effects are negligible and the theoretical reference values
#   :math:`\Gamma=1.0`, :math:`\Gamma_\phi=\Gamma_{\nabla\phi}=0.5` apply.
#
# - `save_solution_vtu`: Saves the phase-field result in VTU format for
#   optional visualization in ParaView or PyVista.
#
# - `results_folder_name`: Folder where results and logs are stored.
#   If the folder already exists, it is replaced with a fresh empty one.


def run_simulations(i, div, l, a, combo_folder_name, element_degree):
    Data = Input(
        l=l,
        save_solution_xdmf=False,
        save_solution_vtu=True,
        results_folder_name=os.path.join(combo_folder_name, str(i)))


    ###############################################################################
    # Mesh Definition
    # ---------------
    # We define the mesh parameters and set up a two-dimensional simulation. This setup 
    # supports various dimensions (‘1D’, ‘2D’, or ‘3D’) by creating a mesh that consists 
    # of either a line, rectangle, or box, depending on the selected dimension, with 
    # corresponding line, quadrilateral, or hexahedral elements.
    #
    # - `divx`, `divy`, and `divz` specify the number of divisions along the x, y, and z 
    # axes, respectively. Here, `divx=100`, `divy=1`, and `divz=1` are set to divide 
    # the x-axis primarily, as needed for a 2D or 1D mesh.
    #
    # - `lx`, `ly`, and `lz` define the physical dimensions of the domain in the x, y, and z 
    # directions. In this example, we set `lx=5.0`, `ly=1.0`, and `lz=1.0`.
    #
    # Specify the simulation dimension with the `dimension` variable (`"1d"`, `"2d"`, or `"3d"`).
    # Here, we choose `"2d"`.
    divx = div
    lx = a


    # Mesh creation based on specified dimension

    # Creates a 1D mesh, which consists of a line divided into `divx` line elements, 
    # extending from 0 to lx along the x-axis.
    msh = dolfinx.mesh.create_interval(
            mpi4py.MPI.COMM_WORLD,
            divx,
            np.array([0.0, lx])
        )



    ###############################################################################
    # Left Boundary Identification
    # ----------------------------
    # This function identifies points on the left side of the domain where the boundary 
    # condition will be applied. Specifically, it returns `True` for points where `x=0`,
    # and `False` otherwise. This allows us to selectively apply boundary conditions 
    # only to this part of the mesh.
    def left(x):
        return np.equal(x[0], 0)

    # %%
    # `fdim` represents the dimension of the boundary facets on the mesh, which is one 
    # less than the mesh's overall dimensionality (`msh.topology.dim`). For example, 
    # if the mesh is 2D, `fdim` will be 1, representing 1D boundary edges.
    fdim = msh.topology.dim - 1

    # %%
    # Using the `left` function, we locate the facets on the left side of the mesh 
    # where `x=0`. The `locate_entities_boundary` function returns an array of facet 
    # indices that represent the identified boundary entities.
    left_facet_marker = dolfinx.mesh.locate_entities_boundary(msh, fdim, left)

    # %%
    # `get_ds_bound_from_marker` is a function that generates a measure for integrating 
    # boundary conditions specifically on the facets identified by `left_facet_marker`. 
    # This measure is assigned to `ds_left` and will be used for applying boundary 
    # conditions on the left side.
    ds_left = get_ds_bound_from_marker(left_facet_marker, msh, fdim)

    # %%
    # `ds_list` is an array that stores boundary condition measures and associated 
    # names for each boundary to facilitate result-saving processes. Each entry in 
    # `ds_list` is an array in the form `[ds_, "name"]`, where `ds_` is the boundary 
    # condition measure, and `"name"` is a label for saving purposes. Here, `ds_left` 
    # is labeled as `"left"` for clarity when saving results.
    ds_list = np.array([
                    [ds_left, "left"],
                    ])


    ###############################################################################
    # Function Space Definition
    # -------------------------
    # Define function spaces for the phase-field using Lagrange elements of
    # degree 1.
    V_phi = dolfinx.fem.functionspace(msh, ("Lagrange", 1))
    V_gradient_phi = dolfinx.fem.functionspace(msh, ("Lagrange", 1, (msh.geometry.dim, )))


    ###############################################################################
    # Boundary Condition Setup for Scalar Field $\phi$
    # ------------------------------------------------
    # We define and apply a Dirichlet boundary condition for the scalar field $\phi$
    # on the left side of the mesh, setting $phi = 1$ on this boundary. This setup is 
    # for a simple, static linear problem, meaning the boundary conditions and loading 
    # are constant and do not change throughout the simulation.
    #
    # - `bc_phi` is a function that creates a Dirichlet boundary condition on a specified 
    #   facet of the mesh for the scalar field $\phi$.
    # - `bcs_list_phi` is a list that stores all the boundary conditions for $\phi$, 
    #   facilitating easy management and extension of conditions if needed.
    # - `update_boundary_conditions` and `update_loading` are set to `None` as they are 
    #   unused in this static case with constant boundary conditions and loading.

    bc_left = bc_phi(left_facet_marker, V_phi, fdim, value=1.0)
    bcs_list_phi = [bc_left]
    update_boundary_conditions = None
    update_loading = None


    ###############################################################################
    # Solver Call for a Static Linear Problem
    # ---------------------------------------
    # We define the parameters for a simple, static linear boundary value problem 
    # with a final time `t = 1.0` and a time step `Δt = 1.0`. Although this setup 
    # includes time parameters, they are primarily used for structural consistency 
    # with a generic solver function and do not affect the result, as the problem 
    # is linear and time-independent.
    #
    # Parameters:
    #
    # - `final_time`: The end time for the simulation, set to 1.0.
    # - `dt`: The time step for the simulation, set to 1.0. In a static context, this
    #   only provides uniformity with dynamic cases but does not change the results.
    # - `path`: Optional path for saving results; set to `None` here to use the default.
    # - `quadrature_degree`: Defines the accuracy of numerical integration; set to 2 
    #   for this problem.
    #
    # Function Call:
    # The `solve` function is called with:
    #
    # - `Data`: Simulation data and parameters.
    # - `msh`: Mesh of the domain.
    # - `V_phi`: Function space for `phi`.
    # - `bcs_list_phi`: List of boundary conditions.
    # - `update_boundary_conditions`, `update_loading`: Set to `None` as they are unused in this static problem.
    # - `ds_list`: Boundary measures for integration on specified boundaries.
    # - `dt` and `final_time` to define the static solution time window.

    final_time = 1.0
    dt = 1.0

    solve(Data,
        msh,
        final_time,
        V_phi,
        bcs_list_phi,
        update_boundary_conditions,
        update_loading,
        ds_list,
        dt,
        path=None,
        quadrature_degree=2,
        V_gradient_Φ=V_gradient_phi)


a=1.0
l=0.1
combo_folder_name = "results_convergence_at2"
div = np.arange(1, 100)

run_combo = False

if run_combo==True:  
    for i in range(0,len(div)):
        run_simulations(i, div[i], l=l, a=a, combo_folder_name=combo_folder_name, element_degree=1)


import matplotlib.pyplot as plt
import numpy as np
from phasefieldx.PostProcessing.ReferenceResult import AllResults
import os
import pandas as pd

###############################################################################
# Load results
if run_combo==True: 
    energy = np.zeros(len(div))
    energy_phi = np.zeros(len(div))
    energy_gradphi= np.zeros(len(div))
    for i in range(0,len(div)):
        simulation_folder = os.path.join(combo_folder_name, str(i))
        S = AllResults(simulation_folder)

        energy[i] = 2*S.energy_files["total.energy"]["gamma"][0]
        energy_phi[i] = 2*S.energy_files["total.energy"]["gamma_phi"][0]
        energy_gradphi[i] = 2*S.energy_files["total.energy"]["gamma_gradphi"][0]
else:
    energy = pd.read_csv(os.path.join(combo_folder_name, "energy.num_crack_surface"), usecols=[1], delimiter="\t").to_numpy().flatten()
    energy_phi = pd.read_csv(os.path.join(combo_folder_name, "energy.num_crack_surface"), usecols=[2], delimiter="\t").to_numpy().flatten()
    energy_gradphi = pd.read_csv(os.path.join(combo_folder_name, "energy.num_crack_surface"), usecols=[3], delimiter="\t").to_numpy().flatten()



import sys
# Import plotting configuration
sys.path.insert(0, os.path.abspath('../../'))
plt.style.use('../../graph.mplstyle')
import plot_config as pcfg

h = a/div

###############################################################################
# Figure: l/h vs. relative error in energy components
# ----------------------------------------------------
l_div_h = l/h
markevery_gamma = max(1, len(h)//10)
markevery_gamma_phi = max(1, len(h)//10)
markevery_gamma_gradphi = max(1, len(h)//12)

# fig, ax = plt.subplots(figsize=(11.69, 5.85))
fig, ax = plt.subplots()
ax.loglog(l_div_h, abs(energy - 1.0)/1.0*100, color=pcfg.color_black,
        linestyle='-', label=pcfg.energy_1d + "=2"+pcfg.gradphi_energy_1d, markevery=markevery_gamma,
        marker='^') 
ax.loglog(l_div_h, abs(energy_phi - 0.5)/0.5*100, color=pcfg.color_blue,
        linestyle='--', label=pcfg.phi_energy_1d, markevery=markevery_gamma_phi,
        marker='o')
ax.loglog(l_div_h, abs(energy_gradphi - 0.5)/0.5*100, color=pcfg.color_red,
        linestyle=':', label=pcfg.gradphi_energy_1d, markevery=markevery_gamma_gradphi,
        marker='s', markerfacecolor='none')
ax.set_xlabel(pcfg.length_l_div_h)
ax.set_ylabel(r"Relative Error [$\%$]")
ax.legend()

plt.savefig(os.path.join(combo_folder_name, "compare_fem_error"))


# Combine the arrays into a 2D array with 2 columns
header = ["div", "gamma", "gamma_phi", "gamma_gradphi"]
data_save = np.column_stack((div, energy, energy_phi, energy_gradphi))
save_path = os.path.join(combo_folder_name, "energy.num_crack_surface")
np.savetxt(save_path, data_save, fmt="%.6e", delimiter="\t", header="\t".join(header), comments="")

plt.show()
