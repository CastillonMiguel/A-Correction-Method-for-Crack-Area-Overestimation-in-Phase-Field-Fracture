r"""
.. _ref_cc_sim11:

Simulation 11
-------------
The model represents a square plate with a central crack, as shown in the figure below. The bottom part is fixed in all directions, while the upper part can slide vertically. A vertical displacement is applied at the top. The geometry and boundary conditions are depicted in the figure. We discretize the model with quadrilateral elements.

.. note::
   In this case, only one quarter of the model will be considered due to symmetry. Additionally, a regular mesh will be used.

.. code-block::

   #           u/\/\/\/\/\/\       u/\/\/\/\/\/\ 
   #            ||||||||||||        ||||||||||||
   #            *----------*    o|\ *----------*
   #            |          |    o|/ |          |
   #            | 2a=1.0   |    o|\ | a=a0     |
   #            |   ----   |    o|/ *----------*
   #            |          |             /_\/_\ 
   #            |          |            oo oo oo
   #            *----------*
   #            /_\/_\/_\/_\       
   #     |Y    /////////////
   #     |
   #     *---X


The Young's modulus, Poisson's ratio, and the critical energy release rate are given in the table :ref:`Properties <table_properties_label>`. Young's modulus $E$ and Poisson's ratio $\nu$ can be represented with the Lamé parameters as: $\lambda=\frac{E\nu}{(1+\nu)(1-2\nu)}$; $\mu=\frac{E}{2(1+\nu)}$.

.. _table_properties_label:

+----+---------+--------+
|    | VALUE   | UNITS  |
+====+=========+========+
| E  | 210     | kN/mm2 |
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
from phasefieldx.Boundary.boundary_conditions import bc_y, bc_x, get_ds_bound_from_marker
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
# - `l`: Length scale parameter, set to 0.0025 $mm$.
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
             l=0.0025,                    
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
             results_folder_name="results_cc_sim_11")


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
msh_file = os.path.join("../GmshGeoFiles/central_cracked/h_0_0004166666.msh")  # Path to the mesh file
# msh_file = os.path.join("mesh.msh")  # Path to the mesh file
gdim = 2                                    # Geometric dimension of the mesh
gmsh_model_rank = 0                        # Rank of the Gmsh model in a parallel setting
mesh_comm = mpi4py.MPI.COMM_WORLD            # MPI communicator for parallel computation

# %%
# The mesh, cell markers, and facet markers are extracted from the 'mesh.msh' file
# using the `read_from_msh` function.
msh, cell_markers, facet_markers = dolfinx.io.gmshio.read_from_msh(msh_file, mesh_comm, gmsh_model_rank, gdim)

fdim = msh.topology.dim - 1 # Dimension of the mesh facets
h=0.0004166666

# h = 1/divx
a0 = 0.5
ly = 3.0
###############################################################################
# Boundary Identification
# -----------------------
# Boundary conditions are applied to specific regions of the domain:
#
# - `bottom`: Identifies the $y=0$ and $x>a0$ boundary.
# - `top`: Identifies the $y=ly$ boundary.
# - `left`: Identifies the $x=0$ boundary.
# - `fdim` is the dimension of boundary facets (1D for a 2D mesh).
def bottom(x):
    return np.logical_and(np.isclose(x[1], 0), np.greater_equal(x[0], a0))

def top(x):
    return np.isclose(x[1], ly)

def left(x):
    return np.isclose(x[0], 0.0)

fdim = msh.topology.dim - 1 # Dimension of the mesh facets

# %%
# These markers are used to apply boundary conditions and external loads to specific regions of the domain:
#
# - `bottom_facet_marker`: Identifies the bottom boundary where y=0 and x >= a0.
# - `top_facet_marker`: Identifies the top boundary where y=ly.
# - `left_facet_marker`: Identifies the left boundary where x=0.
#
# The `locate_entities_boundary` function is used to locate the facets on the mesh that satisfy
# the specified conditions for each boundary.
bottom_facet_marker = dolfinx.mesh.locate_entities_boundary(msh, fdim, bottom)
top_facet_marker = dolfinx.mesh.locate_entities_boundary(msh, fdim, top)
left_facet_marker = dolfinx.mesh.locate_entities_boundary(msh, fdim, left)

# %%
# Selecting the `top` face marker as the target location
# where the external force will be applied during the simulation:
ds_top = get_ds_bound_from_marker(top_facet_marker, msh, fdim)

ds_list = np.array([
                   [ds_top, "top"],
                   ])


###############################################################################
# Function Space Definition
# -------------------------
# Define function spaces for displacement and phase-field using Lagrange elements.
V_u = dolfinx.fem.functionspace(msh, ("Lagrange", 1, (msh.geometry.dim, )))
V_phi = dolfinx.fem.functionspace(msh, ("Lagrange", 1))

# %%
# Boundary Conditions
# -------------------
# The boundary conditions are applied as follows:
#
# - The bottom nodes are constrained in the vertical direction (y), allowing horizontal movement (x displacement unconstrained).
# - The left nodes are constrained in the horizontal direction (x), allowing vertical movement (y displacement unconstrained).
bc_bottom = bc_y(bottom_facet_marker, V_u, fdim)
bc_left = bc_x(left_facet_marker, V_u, fdim)


# %%
# The bcs_list_u variable is a list that stores all boundary conditions for the displacement
# field $\boldsymbol u$. This list facilitates easy management of multiple boundary
# conditions and can be expanded if additional conditions are needed.
bcs_list_u = [bc_bottom,  bc_left]
bcs_list_u_names = ["bottom",  "left"]

###############################################################################
# External Load Definition
# ------------------------
# Here, we define the external load to be applied to the top boundary (`ds_top`).
# `T_top` represents the external force applied in the y-direction.
surface_aplication_force = 1.0
T_top = dolfinx.fem.Constant(msh, petsc4py.PETSc.ScalarType((0.0, 1.0/surface_aplication_force)))

# %%
# The load is added to the list of external loads, `T_list_u`, which will be updated
# incrementally in the `update_loading` function.
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
# This section sets up and calls the solver for a phase-field fracture problem.

final_gamma = 0.7

# %%
# Uncomment the following lines to run the solver with the specified parameters.

c1 = 1.0
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
#       dtau=0.00001,
#       dtau_min=1e-12,
#       dtau_max=0.01,
#       path=None,
#       bcs_list_u_names=bcs_list_u_names,
#       c1=c1,
#       c2=c2,
#       threshold_gamma_save=0.01)

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


from save_function import save_central_crack, plot_comparison_results
save_central_crack(S, h, Data, a0=0.5)
plot_comparison_results(Data)