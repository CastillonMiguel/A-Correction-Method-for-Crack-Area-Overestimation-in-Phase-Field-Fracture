"""
.. _ref_example_geo_central_cracked:

Central Cracked
---------------
This example demonstrates the procedure for generating a mesh for the quarter part of the central cracked specimen used for several simulations.

Below is the .geo file for the central cracked mesh generation.

Reference
---------

.. include::  ../../../../examples/GmshGeoFiles/Central_cracked_h_0_005/file.geo
   :literal:

"""

###############################################################################
# Mesh Visualization
# ------------------
# The purpose of this code is to visualize the mesh. The mesh is generated from
# the .geo file and saved as output_mesh_for_view.vtu. It is then loaded and
# visualized using PyVista.

import os
import gmsh
import pyvista as pv

folder = "central_cracked"

###############################################################################
# Reference
# ---------
# Initialize Gmsh
gmsh.initialize()

# %%
# Open the .geo file
geo_file = os.path.join(folder, "central_cracked_h_0_005.geo")

# If you want to set hcrack, you can use gmsh.option.setNumber before opening the .geo file.
# For example, to set the mesh element size (if hcrack controls mesh size), use:
gmsh.open(geo_file)


# %%
# Generate the mesh (2D example, for 3D use generate(3))
gmsh.model.mesh.generate(2)

# %%
# Write the mesh to a .vtk file for visualization
# Note that the input mesh file for the *phasefieldx* simulation should have the .msh extension.
# Use "output_mesh_for_view.msh" to generate the mesh for the simulation input.
# In this case, the mesh is saved in .vtk format to facilitate visualization with PyVista.
vtu_file = os.path.join(folder, "output_mesh_for_view.vtk")
gmsh.write(vtu_file)

# %%
# Finalize Gmsh
gmsh.finalize()

print(f"Mesh successfully written to {vtu_file}")

# pv.start_xvfb()
file_vtu = pv.read(vtu_file)
file_vtu.plot(cpos='xy', color='white', show_edges=True)
