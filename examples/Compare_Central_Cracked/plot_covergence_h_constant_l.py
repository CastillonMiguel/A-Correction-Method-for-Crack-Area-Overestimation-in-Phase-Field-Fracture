r"""
.. _ref_compare_lh_constant_length_scale::

Influence of the mesh size for constant length scale l/h
--------------------------------------------------------

In this file the effect of the mesh size is studied for a constant length scale l.
So for all simulation under analisys a minimun relation of $l/h=2.5$ is kept, by this way avoinding the
effect finite element error related to the profile captured.

So here the following simulations that considered a lenght scale $l=0.0025$mm are compared:

+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| #                   | $\alpha$       | $\theta$       | Length scale $l$ (mm)         | Mesh size $h$ (mm)       | $l/h$       |
+=====================+================+================+===============================+==========================+=============+
| :ref:`ref_cc_sim2`  | 0.2            | 0.2            | 0.002500                      | 0.001000                 | 2.5         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim9`  | 0.2            | 0.1666         | 0.002500                      | 0.000833                 | 3.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim6`  | 0.2            | 0.125          | 0.002500                      | 0.000625                 | 4.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim10` | 0.2            | 0.1            | 0.002500                      | 0.000500                 | 5.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim11` | 0.2            | 0.0833         | 0.002500                      | 0.0004166                | 6.0         |
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

results_folder = "results_convergence_h_constant_l"
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
marker_lefm = '^'

label_reference = r"Reference"
linestyle_ref = '-'
marker_ref = 'o'

label_bourdin = r"Bourdin"
linestyle_bourdin = '-'
marker_bourdin = 's'

label_dgcm = r"DGCM"
linestyle_dgcm = '-'
marker_dgcm = 'D'

index_to_plot = index_2_9_6_10_11
x_values_ref = 1/results_ref["l_h"][index_to_plot]
x_values_bourdin = 1/results_bourdin["l_h"][index_to_plot]
x_values_dgcm = 1/results_DGCM["l_h"][index_to_plot]

x_label = r"$h/l$"

###############################################################################
# Maximum Force
# -------------
fig, gamma = plt.subplots()

adim_max_force = results_lefm["max_force"][0]

gamma.axhline(y=results_lefm["max_force"][0]/adim_max_force, color=color_lefm, linestyle=linestyle_lefm, label=label_lefm)

gamma.plot(x_values_ref, results_ref["max_force"][index_to_plot]/adim_max_force, color=color_ref, linestyle=linestyle_ref, label=label_reference, marker=marker_ref)
gamma.plot(x_values_bourdin, results_bourdin["max_force"][index_to_plot]/adim_max_force, color=color_bourdin, linestyle=linestyle_bourdin, label=label_bourdin,   marker=marker_bourdin)
gamma.plot(x_values_dgcm, results_DGCM["max_force"][index_to_plot]/adim_max_force, color=color_dgcm, linestyle=linestyle_dgcm, label=label_dgcm,      marker=marker_dgcm)

gamma.set_xlabel(x_label)
gamma.set_ylabel(pcfg.force_force_theory_label)
# gamma.legend()
plt.savefig(os.path.join(results_folder, "max_force"))



###############################################################################
# Ofactor at $\Gamma=0.9$
# -------------------------
fig, gamma = plt.subplots()

# gamma.plot(x_values_ref, results_ref["Ofactor_at_gamma_09"][index_to_plot], color=color_ref, linestyle=linestyle_ref, label=label_reference, marker=marker_ref)
gamma.plot(x_values_bourdin, results_bourdin["Ofactor_at_gamma_09"][index_to_plot], color=color_bourdin, linestyle=linestyle_bourdin, label=label_bourdin, marker=marker_bourdin)
gamma.plot(x_values_dgcm, results_DGCM["Ofactor_at_gamma_09"][index_to_plot], color=color_dgcm, linestyle=linestyle_dgcm, label=label_dgcm, marker=marker_dgcm)

gamma.set_xlabel(x_label)
gamma.set_ylabel(pcfg.correction_factor)
gamma.legend()
plt.savefig(os.path.join(results_folder, "Ofactor_at_gamma_09"))


###############################################################################
# 
# --------------------------
fig, gamma = plt.subplots()

adim_gamma_09 = results_lefm["gamma_at_stiffness_38_52514"][0]

gamma.axhline(y=results_lefm["gamma_at_stiffness_38_52514"][0]/adim_gamma_09, color=color_lefm, linestyle=linestyle_lefm, label=label_lefm)

gamma.plot(x_values_ref, results_ref["gamma_at_stiffness_38_52514"][index_to_plot]/adim_gamma_09, color=color_ref, linestyle=linestyle_ref, label=label_reference, marker=marker_ref)
gamma.plot(x_values_bourdin, results_bourdin["gamma_at_stiffness_38_52514"][index_to_plot]/adim_gamma_09, color=color_bourdin, linestyle=linestyle_bourdin, label=label_bourdin, marker=marker_bourdin)
gamma.plot(x_values_dgcm, results_DGCM["gamma_at_stiffness_38_52514"][index_to_plot]/adim_gamma_09, color=color_dgcm, linestyle=linestyle_dgcm, label=label_dgcm, marker=marker_dgcm)
gamma.set_xlabel(x_label)
gamma.set_ylabel(pcfg.gamma_gamma_theory_label)
gamma.legend()
plt.savefig(os.path.join(results_folder, "gamma_at_stiffness_38_52514"))


plt.show()
