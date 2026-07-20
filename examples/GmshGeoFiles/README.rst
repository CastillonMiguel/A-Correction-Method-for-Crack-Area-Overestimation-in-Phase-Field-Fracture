.. _ref_examples_geo_files:

Gmsh Geometry Files for Meshing
-------------------------------

This directory contains the Gmsh ``.geo`` files used to generate the finite element meshes for all simulations presented in the paper. These geometry scripts are essential for reproducing the exact specimen models analyzed in the study.

For detailed information on Gmsh and its scripting language, please refer to the official `Gmsh documentation <https://gmsh.info>`_.

To generate a 2D mesh from a ``.geo`` file, you can use the following command in your terminal:

.. code-block:: bash
   
   gmsh your_file.geo -2 -o your_mesh.msh

**Command Breakdown:**

*   ``gmsh your_file.geo``: Runs Gmsh on your specified geometry file.
*   ``-2``: Instructs Gmsh to generate a 2D mesh.  
*   ``-3``: Instructs Gmsh to generate a 3D mesh.
*   ``-o your_mesh.msh``: Specifies the output file name for the generated mesh.

This command will create a ``.msh`` file that can be used in the finite element simulations.
