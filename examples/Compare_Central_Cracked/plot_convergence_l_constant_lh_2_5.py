r"""
.. _ref_convergence_l_constant_lh_2_5:

Influence of the lenght scale parameter for constants l/h
---------------------------------------------------------

In this file the effect of the length scale parameter is studied for a constant ratio $l/h$.
So for all simulation under analisys a minimun relation of $l/h=2.5$ is kept, by this way avoinding the
effect finite element error related to the profile captured.

+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| #                   | $\alpha$       | $\theta$       | Length scale $l$ (mm)         | Mesh size $h$ (mm)       | $l/h$       |
+=====================+================+================+===============================+==========================+=============+
| :ref:`ref_cc_sim1`  | 1.0            | 1.0            | 0.012500                      | 0.005000                 | 2.5         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim2`  | 0.2            | 0.2            | 0.002500                      | 0.001000                 | 2.5         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim3`  | 0.1            | 0.1            | 0.001250                      | 0.000500                 | 2.5         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim4`  | 0.05           | 0.05           | 0.000625                      | 0.000250                 | 2.5         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+

"""

###############################################################################
# Import necessary libraries
# --------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyvista as pv
import os
import sys

sys.path.insert(0, os.path.abspath('../../'))
plt.style.use('../../graph.mplstyle') 
import plot_config as pcfg
from scipy.optimize import curve_fit

results_folder = "results_convergence_l_constant_lh_2_5"
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

results_data = "results_convergence_data"

###############################################################################
# Load and visualize convergence results
# --------------------------------------
# Load the saved data from the convergence study for plotting and analysis.
# This includes LEFM reference data and results from the three simulation approaches.
results_lefm = pd.read_csv(os.path.join(results_data, "convergence_data.lefm"), delimiter="\t", comment="#", header=0)
results_ref = pd.read_csv(os.path.join(results_data, "convergence_reference.pff"), delimiter="\t", comment="#", header=0)
results_bourdin = pd.read_csv(os.path.join(results_data, "convergence_bourdin.pff"), delimiter="\t", comment="#", header=0)
results_DGCM = pd.read_csv(os.path.join(results_data, "convergence_dgcm.pff"), delimiter="\t", comment="#", header=0)

# Define indices for grouping simulations by parameter sets for plotting convenience
index_1_2_3_4 = [0, 1, 2, 3]
index_5_6_7_8 = [4, 5, 6, 7]
index_2_9_6_10_11 = [1, 8, 5, 9, 10]

color_lefm = pcfg.color_black
color_ref = pcfg.color_orangered
color_bourdin = pcfg.color_green
color_dgcm = pcfg.color_red

label_lefm = r"LEFM"
linestyle_lefm = '-'
marker_lefm = 'o'

label_reference = r"Reference"
linestyle_ref = '-'
marker_ref = 's'

label_bourdin = r"Bourdin"
linestyle_bourdin = '-'
marker_bourdin = '^'

label_dgcm = r"DGCM"
linestyle_dgcm = '-'
marker_dgcm = 'x'

index_to_plot = index_1_2_3_4
x_values_ref = results_ref["l"][index_to_plot]
x_values_bourdin = results_bourdin["l"][index_to_plot]
x_values_dgcm = results_DGCM["l"][index_to_plot]
x_label = r"$l$"




###############################################################################
# Ofactor
# -------
fig, gamma = plt.subplots()

# gamma.axhline(y=results_lefm["Ofactor_at_gamma_075"][0], color=color_lefm, linestyle=linestyle_lefm, label=label_lefm)

gamma.loglog(x_values_bourdin, results_bourdin["Ofactor_at_gamma_055"][index_to_plot], color=pcfg.color_black, linestyle="--", label=label_bourdin)

# gamma.loglog(x_values_ref, results_ref["Ofactor_at_gamma_055"][index_to_plot], color=color_ref, linestyle=linestyle_ref, label=label_reference, marker=marker_ref)
gamma.loglog(x_values_dgcm, results_DGCM["Ofactor_at_gamma_055"][index_to_plot], color=pcfg.color_orangered, linestyle=linestyle_bourdin, label=r"$\Gamma=0.55$mm", marker=marker_dgcm)
gamma.loglog(x_values_dgcm, results_DGCM["Ofactor_at_gamma_075"][index_to_plot], color=pcfg.color_green, linestyle=linestyle_bourdin, label=r"$\Gamma=0.75$mm", marker=marker_ref)
gamma.loglog(x_values_dgcm, results_DGCM["Ofactor_at_gamma_09"][index_to_plot], color=pcfg.color_blue, linestyle=linestyle_bourdin, label=r"$\Gamma=0.90$mm", marker=marker_lefm)


gamma.set_xlabel(x_label)
gamma.set_ylabel(pcfg.correction_factor)
gamma.legend()
plt.savefig(os.path.join(results_folder, "Ofactor_at_gammas"))


plt.show()
