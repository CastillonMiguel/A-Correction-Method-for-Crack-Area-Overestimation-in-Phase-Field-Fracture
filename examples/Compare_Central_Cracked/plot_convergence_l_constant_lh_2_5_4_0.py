r"""
.. _ref_convergence_l_constant_lh_2_5::

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
from matplotlib.lines import Line2D

results_folder = "results_convergence_l_constant_lh_2_5_4_0"
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
linestyle_ref_2 = '--'
marker_ref = 'o'

label_bourdin = r"Bourdin"
linestyle_bourdin = '-'
linestyle_bourdin_2 = '--'
marker_bourdin = '^'

label_dgcm = r"DGCM"
linestyle_dgcm = '-'
linestyle_dgcm_2 = '--'
marker_dgcm = 'D'

index_to_plot = index_1_2_3_4
x_values_ref = results_ref["l"][index_to_plot]
x_values_bourdin = results_bourdin["l"][index_to_plot]
x_values_dgcm = results_DGCM["l"][index_to_plot]


index_to_plot_2 = index_5_6_7_8
x_values_ref_2 = results_ref["l"][index_to_plot_2]
x_values_bourdin_2 = results_bourdin["l"][index_to_plot_2]
x_values_dgcm_2 = results_DGCM["l"][index_to_plot_2]

x_label = r"$l$"
###############################################################################
# Helper function for consistent legends
# --------------------------------------
def add_legends(ax, main_lines, main_labels, linestyle1, linestyle2, loc1="upper right", loc2="lower left"):
    # Legend for solution types (marker and color)
    legend1 = ax.legend(main_lines,
                         main_labels, 
                         loc=loc1,)
                        #  title="Solution")
    # Legend for line styles (l/h ratio)
    legend2 = ax.legend(
        [
            Line2D([0], [0], color='k', linestyle=linestyle1, label="l/h=2.5"),
            Line2D([0], [0], color='k', linestyle=linestyle2, label="l/h=4.0"),
        ],
        ["l/h=2.5", "l/h=4.0"],
        loc=loc2,
        # title="Line style"
    )
    ax.add_artist(legend1)
    return legend1, legend2

###############################################################################
# Maximum Force
# -------------
fig, gamma = plt.subplots()

adim_max_force = results_lefm["max_force"][0]

# gamma.axhline(y=results_lefm["max_force"][0]/adim_max_force, color=color_lefm, linestyle=linestyle_lefm, label=label_lefm)

# Main solution lines (l/h=2.5, solid lines)
l1, = gamma.loglog(x_values_ref, results_ref["max_force"][index_to_plot]/adim_max_force, color=color_ref, linestyle=linestyle_ref, marker=marker_ref, label=label_reference)
l2, = gamma.loglog(x_values_bourdin, results_bourdin["max_force"][index_to_plot]/adim_max_force, color=color_bourdin, linestyle=linestyle_bourdin, marker=marker_bourdin, label=label_bourdin)
l3, = gamma.loglog(x_values_dgcm, results_DGCM["max_force"][index_to_plot]/adim_max_force, color=color_dgcm, linestyle=linestyle_dgcm, marker=marker_dgcm, label=label_dgcm)

# Additional solution lines (l/h=4.0, dashed lines)
gamma.loglog(x_values_ref_2, results_ref["max_force"][index_to_plot_2]/adim_max_force, color=color_ref, linestyle=linestyle_ref_2, marker=marker_ref, label='_nolegend_')
gamma.loglog(x_values_bourdin_2, results_bourdin["max_force"][index_to_plot_2]/adim_max_force, color=color_bourdin, linestyle=linestyle_bourdin_2, marker=marker_bourdin, label='_nolegend_')
gamma.loglog(x_values_dgcm_2, results_DGCM["max_force"][index_to_plot_2]/adim_max_force, color=color_dgcm, linestyle=linestyle_dgcm_2, marker=marker_dgcm, label='_nolegend_')

gamma.set_xlabel(x_label)
gamma.set_ylabel(pcfg.force_force_theory_label)

# add_legends(
#     gamma,
#     [l1, l2, l3],
#     [label_reference, label_bourdin, label_dgcm],
#     linestyle_ref, linestyle_ref_2
# )

plt.savefig(os.path.join(results_folder, "max_force"))






###############################################################################
# $\Gamma$ at stiffness = 38.52514
# --------------------------------
fig, gamma = plt.subplots()

adim_gamma_09 = results_lefm["gamma_at_stiffness_38_52514"][0]
# gamma.axhline(y=results_lefm["gamma_at_stiffness_38_52514"][0]/adim_gamma_09, color=color_lefm, linestyle=linestyle_lefm, label=label_lefm)

l1, = gamma.loglog(x_values_ref, results_ref["gamma_at_stiffness_38_52514"][index_to_plot]/adim_gamma_09, color=color_ref, linestyle=linestyle_ref, marker=marker_ref, label=label_reference)
l2, = gamma.loglog(x_values_bourdin, results_bourdin["gamma_at_stiffness_38_52514"][index_to_plot]/adim_gamma_09, color=color_bourdin, linestyle=linestyle_bourdin, marker=marker_bourdin, label=label_bourdin)
l3, = gamma.loglog(x_values_dgcm, results_DGCM["gamma_at_stiffness_38_52514"][index_to_plot]/adim_gamma_09, color=color_dgcm, linestyle=linestyle_dgcm, marker=marker_dgcm, label=label_dgcm)

gamma.loglog(x_values_ref_2, results_ref["gamma_at_stiffness_38_52514"][index_to_plot_2]/adim_gamma_09, color=color_ref, linestyle=linestyle_ref_2, marker=marker_ref, label='_nolegend_')
gamma.loglog(x_values_bourdin_2, results_bourdin["gamma_at_stiffness_38_52514"][index_to_plot_2]/adim_gamma_09, color=color_bourdin, linestyle=linestyle_bourdin_2, marker=marker_bourdin, label='_nolegend_')
gamma.loglog(x_values_dgcm_2, results_DGCM["gamma_at_stiffness_38_52514"][index_to_plot_2]/adim_gamma_09, color=color_dgcm, linestyle=linestyle_dgcm_2, marker=marker_dgcm, label='_nolegend_')
gamma.set_xlabel(x_label)
gamma.set_ylabel(pcfg.gamma_gamma_theory_label)

add_legends(
    gamma,
    [l1, l2, l3],
    [label_reference, label_bourdin, label_dgcm],
    linestyle_ref, linestyle_ref_2,
    loc1=(0.65, 0.25),  # ~65% right, 25% up
    loc2=(0.05, 0.25)   # ~5% right, 25% up
)

plt.savefig(os.path.join(results_folder, "gamma_at_stiffness_38_52514"))


plt.show()
