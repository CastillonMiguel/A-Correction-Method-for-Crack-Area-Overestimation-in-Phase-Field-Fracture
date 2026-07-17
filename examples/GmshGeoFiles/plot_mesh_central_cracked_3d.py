r"""
.. _ref_example_geo_central_cracked_3d:

3D Central Cracked Specimen
---------------------------
This example demonstrates how to generate a 3D mesh for a half-model of a central cracked specimen.

The geometry is defined in the following ``.geo`` file, which is then meshed using Gmsh.

Gmsh Geometry File
------------------

.. include::  ../../../../examples/GmshGeoFiles/Central_cracked_3D/central_cracked_3d.geo
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

folder = "central_cracked_3D"

###############################################################################
# Reference
# ---------
# Initialize Gmsh
gmsh.initialize()

# %%
# Open the .geo file
geo_file = os.path.join(folder, "central_cracked_3d.geo")
gmsh.open(geo_file)

# %%
# Generate the mesh (2D example, for 3D use generate(3))
gmsh.model.mesh.generate(3)

# %%
# Write the mesh to a .vtk file for visualization
# Note that the input mesh file for the *phasefieldx* simulation should have the .msh extension.
# Use "output_mesh_for_view.msh" to generate the mesh for the simulation input.
# In this case, the mesh is saved in .vtk format to facilitate visualization with PyVista.
vtu_file = os.path.join(folder, "output_mesh_for_view_1.vtk")
gmsh.write(vtu_file)

# %%
# Finalize Gmsh
gmsh.finalize()

print(f"Mesh successfully written to {vtu_file}")

# pv.start_xvfb()
file_vtu = pv.read(vtu_file)
file_vtu.plot(color='white', show_edges=True)
