r"""
.. _ref_central_cracked_3d_simulation_at2:

Central Cracked Specimen Simulation in 3D (AT2)
-----------------------------------------------

This example models a square plate with a central crack, as illustrated below.

Due to symmetry, only half of the model is considered. The bottom boundary is fixed in both the vertical and out-of-plane directions, while the left boundary is constrained in the horizontal direction. A force is applied at the top. The geometry and boundary conditions are depicted in the figure. The model is discretized using quadrilateral elements.

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

The material properties—Young's modulus, Poisson's ratio, and the critical energy release rate—are summarized in the table below (see also :ref:`Properties <table_properties_label>`). Young's modulus $E$ and Poisson's ratio $\nu$ can be expressed in terms of the Lamé parameters as follows: $\lambda = \frac{E\nu}{(1+\nu)(1-2\nu)}$ and $\mu = \frac{E}{2(1+\nu)}$.

.. _table_properties_label:

+----+---------+--------+
|    | VALUE   | UNITS  |
+====+=========+========+
| E  | 210     | kN/mm² |
+----+---------+--------+
| nu | 0.3     | [-]    |
+----+---------+--------+
| Gc | 0.0027  | kN/mm  |
+----+---------+--------+
| l  | 0.015   | mm     |
+----+---------+--------+

"""

###############################################################################
# Import necessary libraries
# --------------------------
import numpy as np
import dolfinx
import mpi4py
import petsc4py
import os

###############################################################################
# Import from phasefieldx package
# -------------------------------
from phasefieldx.Element.Phase_Field_Fracture.Input import Input
from phasefieldx.Element.Phase_Field_Fracture.solver.solver_ener_non_variational import solve
from phasefieldx.Boundary.boundary_conditions import bc_x, bc_y, bc_z, bc_xyz, get_ds_bound_from_marker
from phasefieldx.PostProcessing.ReferenceResult import AllResults


###############################################################################
# Parameters Definition
# ---------------------
# `Data` is an input object containing essential parameters for simulation setup
# and result storage:
#
# - `E`: Young's modulus, set to 210 $kN/mm^2$.
# - `nu`: Poisson's ratio, set to 0.3.
# - `Gc`: Critical energy release rate, set to 0.0027 $kN/mm$.
# - `l`: Length scale parameter, set to 0.025 $mm$.
# - `degradation`: Specifies the degradation type. Options are "isotropic" or "anisotropic".
# - `split_energy`: Controls how the energy is split; options include "no" (default), "spectral," or "deviatoric."
# - `degradation_function`: Specifies the degradation function; here, it is "quadratic."
# - `irreversibility`: Not used/implemented for this solver.
# - `save_solution_xdmf` and `save_solution_vtu`: Specify the file formats to save displacement results.
#   In this case, results are saved as `.vtu` files.
# - `results_folder_name`: Name of the folder for saving results. If it exists,
#   it will be replaced with a new empty folder.
Data = Input(E=210.0,                       
             nu=0.3,                        
             Gc=0.0027,                 
             l=0.00625,                     
             degradation="isotropic",     
             split_energy="not_applied",   
             degradation_function="quadratic", 
             irreversibility="not_applied", 
             fatigue=False,                
             fatigue_degradation_function="not_applied", 
             fatigue_val=None,              
             k=0.0,                       
             save_solution_xdmf=False,      
             save_solution_vtu=True,      
             results_folder_name="results_simulation_3d")

thickness = 0.05
###############################################################################
# Mesh Definition
# ---------------
# The mesh is a structured grid with quadrilateral elements:
#
# - `divx`, `divy`: Number of elements along the x and y axes.
# - `lx`, `ly`: Physical domain dimensions in x and y.
###############################################################################
# Mesh Definition
# ---------------
# The mesh is generated using Gmsh and saved as a 'mesh.msh' file. For more details 
# on how to create the mesh, refer to the :ref:`ref_example_geo_gomes` examples.
msh_file = os.path.join("../GmshGeoFiles/central_cracked_3D/central_cracked_3d.msh")  # Path to the mesh file
# msh_file = os.path.join("mesh.msh")  # Path to the mesh file
gdim = 3                                    # Geometric dimension of the mesh
gmsh_model_rank = 0                        # Rank of the Gmsh model in a parallel setting
mesh_comm = mpi4py.MPI.COMM_WORLD            # MPI communicator for parallel computation



# %%
# The mesh, cell markers, and facet markers are extracted from the 'mesh.msh' file
# using the `read_from_msh` function.
mesh_data = dolfinx.io.gmsh.read_from_msh(msh_file, mesh_comm, gmsh_model_rank, gdim)
msh = mesh_data.mesh
cell_markers = mesh_data.cell_tags
facet_markers = mesh_data.facet_tags

fdim = msh.topology.dim - 1 # Dimension of the mesh facets
h = 0.0025

# h = 1/divx
a0 = 0.5
ly = 3.0

fdim = msh.topology.dim - 1 # Dimension of the mesh facets
# %%
# The variable `a0` defines the initial crack length in the mesh. This parameter
# is crucial for setting up the simulation, as it determines the starting point
# of the crack in the domain.
a0 = 0.5*thickness  # Initial crack length in the mesh


###############################################################################
# Boundary Identification Functions
# ---------------------------------
def bottom(x):
    return np.isclose(x[1], -ly)

def top(x):
    return np.isclose(x[1], ly)

def left_top(x):
    return np.logical_and(np.isclose(x[0], -0.5), np.greater_equal(x[1], 0.001))

def left_bottom(x):
    return np.logical_and(np.isclose(x[0], -0.5), np.less_equal(x[1], -0.001))


# %%
# Using the `bottom`, `top`, and `left` functions, we locate the facets on the respective boundaries of the mesh:
# - `bottom`: Identifies facets on the bottom boundary where `y = 0` and `x >= a0`.
# - `top`: Identifies facets on the top boundary where `y = ly`.
# - `left`: Identifies facets on the left boundary where `x = 0`.
# The `locate_entities_boundary` function returns an array of facet indices representing these identified boundary entities.
bottom_facet_marker = dolfinx.mesh.locate_entities_boundary(msh, fdim, bottom)
top_facet_marker = dolfinx.mesh.locate_entities_boundary(msh, fdim, top)
left_top_facet_marker = dolfinx.mesh.locate_entities_boundary(msh, fdim, left_top)
left_bottom_facet_marker = dolfinx.mesh.locate_entities_boundary(msh, fdim, left_bottom)

# %%
# The `get_ds_bound_from_marker` function generates a measure for applying boundary conditions 
# specifically to the surface marker where the load will be applied, identified by `top_facet_marker`. 
# This measure is then assigned to `ds_top`.
ds_top = get_ds_bound_from_marker(top_facet_marker, msh, fdim)

# %%
# `ds_list` is an array that stores boundary condition measures along with names 
# for each boundary, simplifying result-saving processes. Each entry in `ds_list` 
# is formatted as `[ds_, "name"]`, where `ds_` represents the boundary condition measure, 
# and `"name"` is a label used for saving. Here, `ds_bottom` and `ds_top` are labeled 
# as `"bottom"` and `"top"`, respectively, to ensure clarity when saving results.
ds_list = np.array([
                   [ds_top, "top"],
                   ])


###############################################################################
# Function Space Definition
# -------------------------
# Define function spaces for displacement and phase-field using Lagrange elements.
V_u = dolfinx.fem.functionspace(msh, ("Lagrange", 1, (msh.geometry.dim, )))
V_phi = dolfinx.fem.functionspace(msh, ("Lagrange", 1))

###############################################################################
# Boundary Conditions
# -------------------
# Dirichlet boundary conditions are defined as follows:
#
# - `bc_bottom`: Constrains the vertical displacement (y-direction) on the bottom boundary
#   where y = 0 and x >= a0, fixing those nodes in the y-direction.
# - `bc_left`: Constrains the horizontal displacement (x-direction) on the left boundary
#   where x = 0, fixing those nodes in the x-direction.
#
# These boundary conditions ensure that the bottom boundary is fixed vertically (except at the crack)
# and the left boundary is fixed horizontally, enforcing symmetry and physical constraints.
# bc_bottom = bc_xyz(bottom_facet_marker, V_u, fdim)
bc_bottom_y = bc_y(bottom_facet_marker, V_u, fdim)
bc_bottom_z = bc_z(bottom_facet_marker, V_u, fdim)
bc_left_top = bc_x(left_top_facet_marker, V_u, fdim)
bc_left_bottom = bc_x(left_bottom_facet_marker, V_u, fdim)
# %%
# The bcs_list_u variable is a list that stores all boundary conditions for the displacement
# field $\boldsymbol u$. This list facilitates easy management of multiple boundary
# conditions and can be expanded if additional conditions are needed.
bcs_list_u = [bc_bottom_y, bc_bottom_z, bc_left_bottom, bc_left_top]
bcs_list_u_names = ["bottom", "bottom_z", "left_bottom", "left_top"]

###############################################################################
# External Load Definition
# ------------------------
# Here, we define the external load to be applied to the top boundary (`ds_top`).
# `T_top` represents the external force applied in the y-direction.
surface_aplication_force = 1.0
T_top = dolfinx.fem.Constant(msh, petsc4py.PETSc.ScalarType((0.0, thickness*surface_aplication_force,0.0)))

# %%
# The load is added to the list of external loads, `T_list_u`.
T_list_u = [
           [T_top, ds_top]
           ]
f = None

###############################################################################
# Boundary Conditions for phase field
bcs_list_phi = []


###############################################################################
# Solver Call for a Phase-Field Fracture Problem
# ----------------------------------------------
final_gamma = 200.0

# %%
# Uncomment the following lines to run the solver with the specified parameters.
c1 = 1.5
c2 = 1.0

# solve(Data,
#       msh,
#       final_gamma,
#       V_u,
#       V_phi,
#       bcs_list_u,
#       bcs_list_phi,
#       f,
#       T_list_u,
#       ds_list,
#       dtau=0.0001*thickness,
#       dtau_min=1e-12,
#       dtau_max=1.0,
#       path=None,
#       bcs_list_u_names=bcs_list_u_names,
#       c1=c1,
#       c2=c2,
#       threshold_gamma_save=0.01*thickness)



###############################################################################
# Load results
# ------------
# Once the simulation finishes, the results are loaded from the results folder.
# The AllResults class takes the folder path as an argument and stores all
# the results, including logs, energy, convergence, and DOF files.
# Note that it is possible to load results from other results folders to compare results.

S = AllResults(Data.results_folder_name)

# # pv.start_xvfb()
# file_vtu = pv.read(os.path.join(Data.results_folder_name, "paraview-solutions_vtu", "phasefieldx_p0_000034.vtu"))
# file_vtu.plot(scalars='phi', cpos='xy', show_scalar_bar=True, show_edges=False)


# from save_function import save_central_crack, plot_comparison_results
# save_central_crack(S, h, Data, a0=0.5)
# plot_comparison_results(Data)




def save_central_crack(S, h, Data, a0=0.5):

    header = ["Ofactor", "displacement", "force", "gamma","gamma_phi", "gamma_gradphi", "compliance", "stiffness", "dCda"]

    ###############################################################################
    # Plot: Displacement vs Fracture Energy
    # -------------------------------------
    force_quarter        = abs(S.reaction_files['bottom.reaction']["Ry"])
    displacement_quarter = abs(2*S.energy_files['total.energy']["E"]/(S.reaction_files['bottom.reaction']["Ry"]))
    stiffness_quarter    = abs(S.reaction_files['bottom.reaction']["Ry"]/displacement_quarter)
    compliance_quarter   = 1/stiffness_quarter
    dCda_quarter         = 2*Data.Gc/S.reaction_files['bottom.reaction']["Ry"]**2
    gamma_quarter        = a0 + S.energy_files['total.energy']["gamma"]
    lambda_quarter       = S.dof_files["lambda.dof"]["lambda"]
    one_factor = np.full_like(displacement_quarter, 1.0)

    ###############################################################################
    # Complete model without corrections
    # ----------------------------------
    displacement_complete  = displacement_quarter
    force_complete         = 2*force_quarter/0.05
    stiffness_complete     = force_complete/displacement_complete
    compliance_complete    = 1/stiffness_complete
    dCda_complete          = dCda_quarter/2.0
    gamma_complete         = a0 + S.energy_files['total.energy']["gamma"]
    gamma_phi_complete     = a0/2 + S.energy_files['total.energy']["gamma_phi"]
    gamma_gradphi_complete = a0/2 + S.energy_files['total.energy']["gamma_gradphi"]


    data_save_reference = np.column_stack((one_factor, 
                                 displacement_complete, 
                                 force_complete, 
                                 gamma_complete,
                                 gamma_phi_complete,
                                 gamma_gradphi_complete,
                                 compliance_complete, 
                                 stiffness_complete, 
                                 dCda_complete))
    save_path_reference = os.path.join(Data.results_folder_name, "results.pff")
    np.savetxt(save_path_reference, data_save_reference, fmt="%.6e", delimiter="\t", header="\t".join(header), comments="")


    ###############################################################################
    # Complete model with Gc corrections
    # ----------------------------------
    gc_factor = np.full_like(displacement_quarter, 1 + h/(2*Data.l))
    displacement_complete_corrected_gc  = displacement_complete/np.sqrt(gc_factor)
    force_complete_corrected_gc         = force_complete/np.sqrt(gc_factor)
    compliance_complete_corrected_gc    = compliance_complete
    stiffness_complete_corrected_gc     = stiffness_complete
    dCda_complete_corrected_gc          = dCda_complete*gc_factor
    gamma_complete_corrected_gc         = a0 + S.energy_files['total.energy']["gamma"]/gc_factor
    gamma_phi_complete_corrected_gc     = a0/2 + S.energy_files['total.energy']["gamma_phi"]/gc_factor
    gamma_gradphi_complete_corrected_gc = a0/2 + S.energy_files['total.energy']["gamma_gradphi"]/gc_factor


    data_save_gc = np.column_stack((gc_factor, 
                                 displacement_complete_corrected_gc, 
                                 force_complete_corrected_gc, 
                                 gamma_complete_corrected_gc,
                                 gamma_phi_complete_corrected_gc,
                                 gamma_gradphi_complete_corrected_gc, 
                                 compliance_complete_corrected_gc,
                                 stiffness_complete_corrected_gc, 
                                 dCda_complete_corrected_gc))
    save_path_gc = os.path.join(Data.results_folder_name, "results_corrected_bourdin.pff")
    np.savetxt(save_path_gc, data_save_gc, fmt="%.6e", delimiter="\t", header="\t".join(header), comments="")

    ###############################################################################
    # Complete model with Gradient correction 
    # ---------------------------------------
    int_phi2 = S.energy_files['total.energy']["gamma_phi"]/(1/(2*Data.l))
    int_gradphi2 = S.energy_files['total.energy']["gamma_gradphi"]/(Data.l/2)

    gradient_factor = 0.5 * (1.0 + 1/Data.l**2 *int_phi2/int_gradphi2)
    # gradient_factor = 0.5*0.5*S.energy_files['total.energy']["gamma"]/S.energy_files['total.energy']["gamma_gradphi"]
    displacement_complete_corrected_gradient  = displacement_complete/np.sqrt(gradient_factor)
    force_complete_corrected_gradient         = force_complete/np.sqrt(gradient_factor)
    compliance_complete_corrected_gradient    = compliance_complete
    stiffness_complete_corrected_gradient     = stiffness_complete
    dCda_complete_corrected_gradient          = dCda_complete*gradient_factor
    gamma_complete_corrected_gradient         = a0   + S.energy_files['total.energy']["gamma"]/gradient_factor
    gamma_phi_complete_corrected_gradient     = a0/2 + S.energy_files['total.energy']["gamma_gradphi"]
    gamma_gradphi_complete_corrected_gradient = a0/2 + S.energy_files['total.energy']["gamma_gradphi"]


    data_save_miguel = np.column_stack((gradient_factor,
                                 displacement_complete_corrected_gradient,
                                 force_complete_corrected_gradient,
                                 gamma_complete_corrected_gradient,
                                 gamma_phi_complete_corrected_gradient,
                                 gamma_gradphi_complete_corrected_gradient,
                                 compliance_complete_corrected_gradient,
                                 stiffness_complete_corrected_gradient,
                                 dCda_complete_corrected_gradient))
    
    save_path_miguel = os.path.join(Data.results_folder_name, "results_corrected_gradient.pff")
    np.savetxt(save_path_miguel, data_save_miguel, fmt="%.6e", delimiter="\t", header="\t".join(header), comments="")


    ###############################################################################
    # Skeleton correction
    # -------------------
    measure=True
    if measure:
        results_a_measured = np.loadtxt(os.path.join(Data.results_folder_name,"crack_measurement/interpolated_step_time_crack_length.txt"), skiprows=1)
        crack_measured = results_a_measured[:,1]*thickness
        F_Skeleton = S.energy_files['total.energy']["gamma"][0:len(crack_measured)]/crack_measured

        displacement_Skeleton  = displacement_complete[0:len(crack_measured)]/np.sqrt(F_Skeleton)
        force_Skeleton         = force_complete[0:len(crack_measured)]/np.sqrt(F_Skeleton)
        compliance_Skeleton    = compliance_complete[0:len(crack_measured)]
        stiffness_Skeleton     = stiffness_complete[0:len(crack_measured)]
        dCda_Skeleton          = dCda_complete[0:len(crack_measured)]*F_Skeleton
        gamma_Skeleton         = a0 + S.energy_files['total.energy']["gamma"][0:len(crack_measured)]/F_Skeleton
        gamma_phi_Skeleton     = a0/2 + S.energy_files['total.energy']["gamma_phi"][0:len(crack_measured)]/F_Skeleton
        gamma_gradphi_Skeleton = a0/2 + S.energy_files['total.energy']["gamma_gradphi"][0:len(crack_measured)]/F_Skeleton


        data_save_skeleton = np.column_stack((F_Skeleton,
                                    displacement_Skeleton,
                                    force_Skeleton,
                                    gamma_Skeleton,
                                    gamma_phi_Skeleton,
                                    gamma_gradphi_Skeleton,
                                    compliance_Skeleton,
                                    stiffness_Skeleton,
                                    dCda_Skeleton))
    
        save_path_Skeleton = os.path.join(Data.results_folder_name, "results_corrected_skeleton.pff")
        np.savetxt(save_path_Skeleton, data_save_skeleton, fmt="%.6e", delimiter="\t", header="\t".join(header), comments="")

import pyvista as pv
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, os.path.abspath('../../'))
plt.style.use('../../graph.mplstyle')
import plot_config as pcfg

def plot_comparison_results(data_obj):
    """
    Plots a comparison of simulation results from different correction methods.

    Args:
        data_obj: An object containing simulation data, including the results folder name.
        plot_config: An object containing plotting configuration like labels.
    """
    path = data_obj.results_folder_name

    results = pd.read_csv(os.path.join(path, "results.pff"), delimiter="\t", comment="#", header=0)
    results_bourdin = pd.read_csv(os.path.join(path, "results_corrected_bourdin.pff"), delimiter="\t", comment="#", header=0)
    results_DGCM = pd.read_csv(os.path.join(path, "results_corrected_gradient.pff"), delimiter="\t", comment="#", header=0)
    results_Skeleton = pd.read_csv(os.path.join(path, "results_corrected_skeleton.pff"), delimiter="\t", comment="#", header=0)

    color_1 = "black"
    color_2 = "blue"
    color_3 = "red"
    color_4 = "green"

    label_reference = "Reference"
    label_bourdin = "Bourdin"
    label_DGCM = "DGCM"
    label_Skeleton = "Skeleton"

    ###############################################################################
    # Plot: Crack Length vs Ofactor
    # -----------------------------
    fig, ax = plt.subplots()

    ax.plot(results["gamma"], results["Ofactor"], color=color_1, linestyle='-', label=label_reference)
    ax.plot(results_bourdin["gamma"], results_bourdin["Ofactor"], color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(results_DGCM["gamma"], results_DGCM["Ofactor"], color=color_3, linestyle=':', label=label_DGCM)
    ax.plot(results_Skeleton["gamma"], results_Skeleton["Ofactor"], color=color_4, linestyle='-.', label=label_Skeleton)

    ax.set_ylim(0.0, 20)
    ax.set_xlabel(pcfg.gamma_label)
    ax.set_ylabel(pcfg.correction_factor)
    ax.legend()

    ###############################################################################
    # Plot: Displacement vs Force
    # ---------------------------
    fig, ax = plt.subplots()

    ax.plot(results["displacement"], results["force"], color=color_1, linestyle='-', label=label_reference)
    ax.plot(results_bourdin["displacement"], results_bourdin["force"], color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(results_DGCM["displacement"], results_DGCM["force"], color=color_3, linestyle=':', label=label_DGCM)
    ax.plot(results_Skeleton["displacement"], results_Skeleton["force"], color=color_4, linestyle='-.', label=label_Skeleton)

    ax.set_xlabel(pcfg.displacement_label)
    ax.set_ylabel(pcfg.force_label)
    ax.legend()

    ###############################################################################
    # Plot: Gamma vs Stiffness
    # ------------------------
    fig, ax = plt.subplots()

    ax.plot(results["gamma"], results["stiffness"], color=color_1, linestyle='-', label=label_reference)
    ax.plot(results_bourdin["gamma"], results_bourdin["stiffness"], color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(results_DGCM["gamma"], results_DGCM["stiffness"], color=color_3, linestyle=':', label=label_DGCM)
    ax.plot(results_Skeleton["gamma"], results_Skeleton["stiffness"], color=color_4, linestyle='-.', label=label_Skeleton)

    ax.set_xlabel(pcfg.gamma_label)
    ax.set_ylabel(pcfg.stiffness_label)
    ax.legend()

    ###############################################################################
    # Plot: Displacement vs Stiffness
    # ---------------------------
    fig, ax = plt.subplots()

    ax.plot(results["displacement"], results["stiffness"], color=color_1, linestyle='-', label=label_reference)
    ax.plot(results_bourdin["displacement"], results_bourdin["stiffness"], color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(results_DGCM["displacement"], results_DGCM["stiffness"], color=color_3, linestyle=':', label=label_DGCM)
    ax.plot(results_Skeleton["displacement"], results_Skeleton["stiffness"], color=color_4, linestyle='-.', label=label_Skeleton)
    ax.set_xlabel(pcfg.displacement_label)

    ax.set_ylabel(pcfg.stiffness_label)
    ax.legend()

    ###############################################################################
    # Plot: Displacement vs Gamma
    # ---------------------------
    fig, ax = plt.subplots()

    ax.plot(results["displacement"], results["gamma"], color=color_1, linestyle='-', label=label_reference)
    ax.plot(results_bourdin["displacement"], results_bourdin["gamma"], color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(results_DGCM["displacement"], results_DGCM["gamma"], color=color_3, linestyle=':', label=label_DGCM)
    ax.plot(results_Skeleton["displacement"], results_Skeleton["gamma"], color=color_4, linestyle='-.', label=label_Skeleton)

    ax.set_xlabel(pcfg.displacement_label)
    ax.set_ylabel(pcfg.gamma_label)
    ax.legend()

    ###############################################################################
    # Plot: Gamma
    # ------------

    # Define the steps corresponding to the stages
    step_initial = 292 - 1       #20
    step_mid = 1030 - 1          #40
    step_final = 1762 - 1        #60

    fig, ax = plt.subplots()

    ax.plot(results["gamma"], color=color_1, linestyle='-', label=label_reference)
    ax.plot(results_bourdin["gamma"], color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(results_DGCM["gamma"], color=color_3, linestyle=':', label=label_DGCM)
    ax.plot(results_Skeleton["gamma"], color=color_4, linestyle='-.', label=label_Skeleton)

    ax.axvline(x=step_initial, color='gray', linestyle='--')
    ax.axvline(x=step_mid, color='gray', linestyle='--')
    ax.axvline(x=step_final, color='gray', linestyle='--')

    ax.set_xlabel(pcfg.displacement_label)
    ax.set_ylabel(pcfg.gamma_label)
    ax.legend()

    error_bourdin = abs((results_bourdin["gamma"] - results_Skeleton["gamma"])/results_Skeleton["gamma"])*100
    error_DGCM = abs((results_DGCM["gamma"] - results_Skeleton["gamma"])/results_Skeleton["gamma"])*100
    error_reference = abs((results["gamma"] - results_Skeleton["gamma"])/results_Skeleton["gamma"])*100

    fig, ax = plt.subplots()

    ax.plot(error_reference, color=color_1, linestyle='-', label=label_reference)
    ax.plot(error_bourdin, color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(error_DGCM, color=color_3, linestyle=':', label=label_DGCM)


    ax.axvline(x=step_initial, color='gray', linestyle='--')
    ax.axvline(x=step_mid, color='gray', linestyle='--')
    ax.axvline(x=step_final, color='gray', linestyle='--')
    ax.set_ylim(0, 100)
    ax.set_xlabel(pcfg.displacement_label)
    ax.set_ylabel(pcfg.gamma_label)
    ax.legend()


    # Extract crack area values (gamma) for each method at the specific steps
    # Note: The user prompt asks for "crack area", and the variable is 'gamma'.
    # In the previous print statements, the user was subtracting 'thickness*0.5' (initial crack area a0).
    # Assuming the table wants the *propagation* area (change in area) or total area?
    # The previous code printed: results["gamma"][step] - thickness*0.5.
    # Let's stick to that logic: Area_propagation = Total_Gamma - Initial_Crack_Area.
    # Initial crack area a0 = 0.5 * thickness.

    a0_val = 0.5 * thickness *0

    # Reference
    ref_initial = results["gamma"][step_initial] - a0_val
    ref_mid = results["gamma"][step_mid] - a0_val
    ref_final = results["gamma"][step_final] - a0_val
    # Reference Errors
    err_ref_initial = error_reference[step_initial]
    err_ref_mid = error_reference[step_mid]
    err_ref_final = error_reference[step_final]

    # Bourdin
    bourdin_initial = results_bourdin["gamma"][step_initial] - a0_val
    bourdin_mid = results_bourdin["gamma"][step_mid] - a0_val
    bourdin_final = results_bourdin["gamma"][step_final] - a0_val

    # Bourdin Errors
    err_bourdin_initial = error_bourdin[step_initial]
    err_bourdin_mid = error_bourdin[step_mid]
    err_bourdin_final = error_bourdin[step_final]

    # DGCM
    dgcm_initial = results_DGCM["gamma"][step_initial] - a0_val
    dgcm_mid = results_DGCM["gamma"][step_mid] - a0_val
    dgcm_final = results_DGCM["gamma"][step_final] - a0_val

    err_dgcm_initial = error_DGCM[step_initial]
    err_dgcm_mid = error_DGCM[step_mid]
    err_dgcm_final = error_DGCM[step_final]

    # Skeletonization (Hardcoded values from previous print statements)
    # Previous code:
    skel_initial = 1.41479584e-01 * thickness  - a0_val
    skel_mid = 2.98637943e-01 * thickness  - a0_val
    skel_final = 4.44317656e-01 * thickness  - a0_val

    print(r"\begin{table}[h!]")
    print(r"   \centering")
    print(r"   \caption{Evolution of the crack area in the 3D center-cracked specimen for different correction methods.}")
    print(r"   \label{tab:3d_crack_area_evolution}")
    print(r"   \renewcommand{\arraystretch}{1.2}")
    print(r"   \begin{tabular}{@{}lccc@{}}")
    print(r"      \toprule")
    print(r"      \textbf{Correction Method} & \textbf{Initial Prop.} (mm$^2$) & \textbf{Mid Prop.} (mm$^2$) & \textbf{Final Stage} (mm$^2$) \\")
    print(r"      \midrule")
    print(f"      Skeletonization         & {skel_initial:.5f} & {skel_mid:.5f} & {skel_final:.5f} \\\\")
    print(f"      Reference               & {ref_initial:.5f} & {ref_mid:.5f} & {ref_final:.5f} \\\\")
    print(f"      Bourdin                 & {bourdin_initial:.5f} & {bourdin_mid:.5f} & {bourdin_final:.5f} \\\\")
    print(f"      DGCM                    & {dgcm_initial:.5f} & {dgcm_mid:.5f} & {dgcm_final:.5f} \\\\")
    print(r"      \bottomrule")
    print(r"   \end{tabular}")
    print(r"\end{table}")

    # Calculate relative errors with respect to Skeletonization
    # Error = (Value - Skeleton) / Skeleton * 100


    print(r"\begin{table}[h!]")
    print(r"   \centering")
    print(r"   \caption{Evolution of the crack area and relative error (in parentheses) with respect to the Skeletonization method in the 3D center-cracked specimen.}")
    print(r"   \label{tab:3d_crack_area_evolution_with_error}")
    print(r"   \renewcommand{\arraystretch}{1.2}")
    print(r"   \begin{tabular}{@{}lccc@{}}")
    print(r"      \toprule")
    print(r"      \textbf{Correction Method} & \textbf{Initial Prop.} (mm$^2$) & \textbf{Mid Prop.} (mm$^2$) & \textbf{Final Stage} (mm$^2$) \\")
    print(r"      \midrule")
    print(f"      Skeletonization         & {skel_initial:.5f} & {skel_mid:.5f} & {skel_final:.5f} \\\\")
    print(f"      Reference               & {ref_initial:.5f} ({err_ref_initial:+.2f}\%) & {ref_mid:.5f} ({err_ref_mid:+.2f}\%) & {ref_final:.5f} ({err_ref_final:+.2f}\%) \\\\")
    print(f"      Bourdin                 & {bourdin_initial:.5f} ({err_bourdin_initial:+.2f}\%) & {bourdin_mid:.5f} ({err_bourdin_mid:+.2f}\%) & {bourdin_final:.5f} ({err_bourdin_final:+.2f}\%) \\\\")
    print(f"      DGCM                    & {dgcm_initial:.5f} ({err_dgcm_initial:+.2f}\%) & {dgcm_mid:.5f} ({err_dgcm_mid:+.2f}\%) & {dgcm_final:.5f} ({err_dgcm_final:+.2f}\%) \\\\")
    print(r"      \bottomrule")
    print(r"   \end{tabular}")
    print(r"\end{table}")

    plt.show()

save_central_crack(S, h, Data, a0=0.0)
plot_comparison_results(Data)


save_images_3d = False
if save_images_3d:

    ###############################################################################
    # Plot: Phase-Field with Crack Path Visualization
    # -----------------------------------------------
    # This 3D visualization combines the phase-field distribution with a theoretical
    # crack path line (red line) to compare the predicted crack trajectory with
    # the phase-field simulation results.

    vtu_folder = os.path.join(Data.results_folder_name, "paraview-solutions_vtu")
    vtu_files = sorted([f for f in os.listdir(vtu_folder) if f.endswith(".vtu")])

    if vtu_files:
        # Load the last file for interactive visualization
        last_vtu_file = os.path.join(vtu_folder, vtu_files[-1])
        file_vtu_interactive = pv.read(last_vtu_file)

        # Show the plot and allow interactive camera adjustment
        plotter = pv.Plotter()
        # Extract the y-coordinate array from the mesh points
        y_coords = file_vtu_interactive.points[:, 1]

        # Create a mask for points where -1 < y < 1
        mask = np.logical_and(y_coords > -0.25, y_coords < 0.25)

        # Extract the cells (elements) whose all points are within the y-range
        cells_in_range = []
        for cell in range(file_vtu_interactive.n_cells):
            point_ids = file_vtu_interactive.get_cell(cell).point_ids
            if np.all(mask[point_ids]):
                cells_in_range.append(cell)

        # Extract a sub-mesh containing only the selected cells
        specimen_region = file_vtu_interactive.extract_cells(cells_in_range)

        # Show cracked region (phi > 0.95) in red with edges, but only in the selected y-range
        cracked_region = specimen_region.threshold(0.95, scalars='phi')
        plotter.add_mesh(cracked_region, color='red', show_scalar_bar=False, show_edges=True)

        # Show the full mesh in light gray, semi-transparent, only in the selected y-range
        plotter.add_mesh(specimen_region, color="lightgray", show_edges=False,
                        edge_color="black", line_width=1.0, opacity=0.5)

        plotter.view_xy()
        plotter.show()
        print("Camera position:", plotter.camera_position)



    def save_vtu_visualization(vtu_file, output_filename, results_folder):
        """
        Generates and saves a visualization of the phase-field from a VTU file.

        Parameters:
        - vtu_file: PyVista mesh object loaded from a VTU file.
        - output_filename: The name of the output image file (e.g., 'visualization.png').
        - results_folder: The path to the folder where the image will be saved.
        """
        plotter = pv.Plotter(off_screen=True)

        # Add the cracked region (phi > 0.9) in red
        # Extract the y-coordinate array from the mesh points
        y_coords = vtu_file.points[:, 1]

        # Create a mask for points where -0.25 < y < 0.25
        mask = np.logical_and(y_coords > -0.25, y_coords < 0.25)

        # Extract the cells (elements) whose all points are within the y-range
        cells_in_range = []
        for cell in range(vtu_file.n_cells):
            point_ids = vtu_file.get_cell(cell).point_ids
            if np.all(mask[point_ids]):
                cells_in_range.append(cell)

        # Extract a sub-mesh containing only the selected cells
        specimen_region = vtu_file.extract_cells(cells_in_range)

        # Add the cracked region (phi > 0.95) in red, but only in the selected y-range
        cracked_region = specimen_region.threshold(0.95, scalars='phi')
        if cracked_region.n_points > 0:
            plotter.add_mesh(cracked_region, color='red', show_scalar_bar=False,
                            show_edges=True)

        # Add the full mesh in light gray, semi-transparent, only in the selected y-range
        plotter.add_mesh(specimen_region, color="lightgray", show_edges=False,
                        edge_color="black", line_width=2.0, opacity=0.35, show_scalar_bar=False)
        
        
        # # Set camera position and background
        # plotter.camera_position = [
        #     (0.75, 0.0, 0.25),  # position
        #     (0.15, 0.0, 0.0),  # focal_point
        #     (-0.15, 1.0, -0.15)    # view_up
        # ]

        plotter.camera_position =[(1.0152466639900397, 0.46516810129818353, 0.8396552699570612),
    (0.006765864455509224, -0.10148899804436526, -0.07809046177057155),
    (-0.24105474771079083, 0.9216175781110938, -0.3041605633916554)]

    #     Camera position: [(0.7311898020991889, 0.10495413302096798, 0.22824171879810334),
    #  (0.14547049006444135, -0.01957636639465496, -0.07992550279562541),
    #  (-0.1210163919750773, 0.9787558526359754, -0.16550532862768993)]
        
        plotter.set_background("white")

        # Enable anti-aliasing for better quality
        plotter.enable_anti_aliasing('ssaa')

        # Save the screenshot with a higher resolution
        image_path = os.path.join(results_folder, output_filename)
        plotter.screenshot(image_path, transparent_background=False, window_size=[1200, 1000], return_img=False)
        plotter.close()
        print(f"Image saved to {image_path}")

    save_image = True
    if save_image:
        # Iterate over all .vtu files in the directory
        for filename in vtu_files:
            file_path = os.path.join(vtu_folder, filename)
            vtu_file = pv.read(file_path)
            
            # Create output filename (replace .vtu with .png)
            output_filename = filename.replace(".vtu", ".png")
            
            save_vtu_visualization(vtu_file, output_filename, Data.results_folder_name+"/images")