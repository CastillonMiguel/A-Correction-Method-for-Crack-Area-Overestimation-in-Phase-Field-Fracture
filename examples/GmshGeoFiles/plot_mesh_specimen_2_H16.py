r"""
.. _ref_example_geo_specimen_2_H16:

Specimen 2
----------
This example demonstrates the procedure for generating a mesh for the compact tension specimen presented in :footcite:t:`example_Wagner2018_phd_thesis`, from which some of the simulation results will be compared. In this case, the mesh corresponds to an initial crack position of $H=1.6$ mm following the coordinate system presented in the .geo file.

The parameter $H$ represents the vertical position of the initial crack tip measured from the specimen centerline. This specific configuration ($H=1.6$ mm) represents one of the test cases used to study crack path deviation in specimens with multiple holes, where the asymmetric crack position leads to complex crack propagation behavior.

All dimensions are defined relative to the base dimension $b = 40$ mm, allowing for easy scaling of the geometry by modifying this parameter in the .geo file. The specimen includes three circular holes that influence the crack propagation path, making this a challenging test case for phase-field fracture analysis.

.. footbibliography::

Below is the .geo file used for the specimen 2:

Reference
---------

.. include::  ../../../../examples/GmshGeoFiles/Compact_specimen/specimen_2_H16.geo
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

folder = "Compact_specimen"

###############################################################################
# Reference
# ---------
# Initialize Gmsh
gmsh.initialize()

# %%
# Open the .geo file
geo_file = os.path.join(folder, "specimen_2_H16.geo")
gmsh.open(geo_file)

# %%
# Generate the mesh (2D example, for 3D use generate(3))
gmsh.model.mesh.generate(2)

# %%
# Write the mesh to a .vtk file for visualization
# Note that the input mesh file for the *phasefieldx* simulation should have the .msh extension.
# Use "output_mesh_for_view.msh" to generate the mesh for the simulation input.
# In this case, the mesh is saved in .vtk format to facilitate visualization with PyVista.
vtu_file = os.path.join(folder, "output_mesh_for_view_2.vtk")
gmsh.write(vtu_file)

# %%
# Finalize Gmsh
gmsh.finalize()

print(f"Mesh successfully written to {vtu_file}")

# pv.start_xvfb()
file_vtu = pv.read(vtu_file)
file_vtu.plot(cpos='xy', color='white', show_edges=True)

save_image=False
# Create a PyVista plotter
if save_image:
   plotter = pv.Plotter(off_screen=True)

   # Add the mesh with a light gray surface and visible edges
   plotter.add_mesh(file_vtu, color="lightgray", show_edges=True,
                         edge_color="darkblue", line_width=0.5, opacity=0.7)

   # Add the wireframe with darker lines to highlight the mesh structure
   plotter.add_mesh(file_vtu, style="wireframe", color="black",
                         line_width=1.2)

   # Set the view and background
   plotter.view_xy()
   plotter.set_background("white")
   plotter.camera.tight(padding=0.0)
   plotter.camera.clipping_range = (0.1, 1000.0)

   # Save the screenshot
   image_file = os.path.join(folder, "specimen_2_H16.png")
   plotter.screenshot(image_file, transparent_background=False, return_img=False)
   plotter.close()

   print(f"Image saved to {image_file}")