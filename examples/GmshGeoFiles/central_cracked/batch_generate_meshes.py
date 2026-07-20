r"""
.. _ref_generate_meshes:

Mesh Generation for Central Cracked Specimen
--------------------------------------------

"""

import numpy as np
import subprocess
import os

run=False

if run:
# Array of hcrack values
    h_array = np.array([0.01,
                        0.0075,
                        0.005,
                        0.0025,
                        0.001,
                        0.0008333333,
                        0.00075,
                        0.000625,
                        0.0005,
                        0.0004166666,
                        0.0003125,
                        0.00025,
                        0.0001,
                        0.00015625,
                        0.000075])


    geo_file = "central_cracked.geo"
    output_template = "central_cracked_h_{:04d}.msh"

    for h in h_array:
        h_str = str(h).replace('.', '_')
        output_file = f"h_{h_str}.msh"
        cmd = [
            "gmsh", geo_file, "-2",
            "-o", output_file,
            "-setnumber", "hcrack", str(2*h)
        ]
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
