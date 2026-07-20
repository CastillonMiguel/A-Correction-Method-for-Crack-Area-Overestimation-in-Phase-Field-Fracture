r"""
.. _ref_compare_pff_lefm:

Validation against LEFM — single simulation (AT2, sim 8)
---------------------------------------------------------

This script compares the three correction approaches against the analytical Linear Elastic
Fracture Mechanics (LEFM) solution for the central cracked specimen. It uses
:ref:`ref_cc_sim8` (:math:`l = 0.000625` mm, :math:`h = 0.00015625` mm, :math:`l/h = 4.0`),
the finest AT2 simulation, which minimizes strain localization error and provides the closest
phase-field representation of the sharp-crack limit.

The LEFM reference provides the exact structural compliance
:math:`C(a) = 2a\,F(a/W)/(Eh)`, from which the stiffness and force are derived analytically.

**Plots generated**

- Correction factor :math:`\mathcal{F}` vs. crack length :math:`\Gamma` for the three methods.
- Force vs. displacement curves (with inset zoom on the peak-force region).
- Structural stiffness :math:`K = P/u` vs. crack length :math:`\Gamma` (with inset zoom).

**Simulations used**

- :ref:`ref_cc_sim8` — AT2, :math:`l = 0.000625` mm, :math:`l/h = 4.0`
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
sys.path.insert(0, os.path.abspath('../'))
plt.style.use('../../graph.mplstyle') 
import plot_config as pcfg

results_folder = "results_compare_pff_lefm"
if not os.path.exists(results_folder):
    os.makedirs(results_folder)


###############################################################################
# Load results
# ------------
# Once the simulation finishes, the results are loaded from the results folder.
# The AllResults class takes the folder path as an argument and stores all
# the results, including logs, energy, convergence, and DOF files.
# Note that it is possible to load results from other results folders to compare results.
# It is also possible to define a custom label and color to automate plot labels.


###############################################################################
# Load simulation data
# --------------------

def load_simulation_data(path):
    """Load all three types of results for a simulation path."""
    try:
        data = {
            "ref": pd.read_csv(os.path.join(path, "results.pff"), delimiter="\t", comment="#", header=0),
            "bourdin": pd.read_csv(os.path.join(path, "results_corrected_bourdin.pff"), delimiter="\t", comment="#", header=0),
            "dgcm": pd.read_csv(os.path.join(path, "results_corrected_gradient.pff"), delimiter="\t", comment="#", header=0)
        }
        return data
    except Exception as e:
        print(f"Warning: Could not load data for {path}: {e}")
        return {"ref": None, "bourdin": None, "dgcm": None}

simulation = load_simulation_data("../Central_cracked_all_at2/results_cc_sim_8")


color_1, linestyle_1, marker_1 = pcfg.color_orangered, '-', 'o' #ref
color_2, linestyle_2, marker_2 = pcfg.color_green, '-.', 's' #bourdin
color_3, linestyle_3, marker_3 = pcfg.color_red, '--', '^' #dgcm

markevery_1 = max(1, len(simulation["ref"]["displacement"])//20) if simulation["ref"] is not None else 1

# %%
# From Linear elastic fracture mechanics theory
lefm_solution = np.loadtxt("../Papers_Data/A_Phase_Field_Approach_to_Fatigue/results_central_cracked/center_cracked.lefm", delimiter="\t", skiprows=1)
a_lefm = lefm_solution[:,0]
k_lefm = 1/lefm_solution[:,2]
c_lefm = lefm_solution[:,2]
dcda_lefm = lefm_solution[:,3]
color_lefm = pcfg.color_black

results_lefm =  pd.read_csv("../Papers_Data/A_Phase_Field_Approach_to_Fatigue/results_central_cracked/a0_05.lefm_problem", delimiter="\t", comment="#", header=0)

LABEL_LEFM = r"LEFM"
color_var = pcfg.color_black
linestyle_LEFM = '-'

label_reference = r"No correction"
label_bourdin = r"Bourdin"
label_dgcm = r"DGCM"



###############################################################################
# Plot: Gamma vs Correction Factor
# --------------------------------
fig, ax_l1_uf = plt.subplots()
ax_l1_uf.plot(simulation["ref"]["gamma"], simulation["ref"]["Ofactor"], color=color_1, linestyle=linestyle_1, label=label_reference)
ax_l1_uf.plot(simulation["bourdin"]["gamma"], simulation["bourdin"]["Ofactor"], color=color_2, linestyle=linestyle_2, label=label_bourdin)
ax_l1_uf.plot(simulation["dgcm"]["gamma"], simulation["dgcm"]["Ofactor"], color=color_3, linestyle=linestyle_3, label=label_dgcm)

ax_l1_uf.set_xlabel(pcfg.crack_length_label)
ax_l1_uf.set_ylabel(pcfg.correction_factor)
ax_l1_uf.legend()
ax_l1_uf.set_ylim(0.75, 2.0)
# plt.savefig(os.path.join(results_folder, "compare_correction_factor"))


###############################################################################
# Plot: Displacement vs Force
# ---------------------------
fig, ax_ref0 = plt.subplots()
ax_ref0.plot(results_lefm["u"], results_lefm["P"], color=color_lefm, linestyle=linestyle_LEFM, label=LABEL_LEFM, linewidth=3)
ax_ref0.plot(simulation["ref"]["displacement"], simulation["ref"]["force"], color=color_1, linestyle=linestyle_1, label=label_reference)
ax_ref0.plot(simulation["bourdin"]["displacement"], simulation["bourdin"]["force"], color=color_2, linestyle=linestyle_2, label=label_bourdin)
ax_ref0.plot(simulation["dgcm"]["displacement"], simulation["dgcm"]["force"], color=color_3, linestyle=linestyle_3, label=label_dgcm)

ax_ref0.set_xlabel(pcfg.displacement_label)
ax_ref0.set_ylabel(pcfg.force_label)
# inset axes....
axins = ax_ref0.inset_axes([0.05, 0.525, 0.4, 0.4])
axins.plot(results_lefm["u"], results_lefm["P"], color=color_lefm, linestyle=linestyle_LEFM, label=LABEL_LEFM, linewidth=3)
axins.plot(simulation["ref"]["displacement"], simulation["ref"]["force"], color=color_1, linestyle=linestyle_1)
axins.plot(simulation["bourdin"]["displacement"], simulation["bourdin"]["force"], color=color_2, linestyle=linestyle_2)
axins.plot(simulation["dgcm"]["displacement"], simulation["dgcm"]["force"], color=color_3, linestyle=linestyle_3)

# sub region of the original image
x1, x2, y1, y2 = 0.01406, 0.019, 0.93, 1.26
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticks([])
axins.set_yticks([])

axins.spines['top'].set_visible(True)
axins.spines['right'].set_visible(True)

ax_ref0.indicate_inset_zoom(axins)
# ax_ref0.legend()
plt.savefig(os.path.join(results_folder, "force_displacement"))



###############################################################################
# Plot: Gamma vs Stiffness
# ------------------------
fig, ax_ref0 = plt.subplots()
ax_ref0.plot(results_lefm["a"], results_lefm["P"]/results_lefm["u"], color=color_lefm, linestyle=linestyle_LEFM, label=LABEL_LEFM,linewidth=2)
ax_ref0.plot(simulation["ref"]["gamma"], simulation["ref"]["stiffness"], color=color_1, linestyle=linestyle_1, label=label_reference)
ax_ref0.plot(simulation["bourdin"]["gamma"], simulation["bourdin"]["stiffness"], color=color_2, linestyle=linestyle_2, label=label_bourdin)
ax_ref0.plot(simulation["dgcm"]["gamma"], simulation["dgcm"]["stiffness"], color=color_3, linestyle=linestyle_3, label=label_dgcm)

# inset axes....
axins = ax_ref0.inset_axes([0.1, 0.1, 0.4, 0.4])
axins.plot(results_lefm["a"], results_lefm["P"]/results_lefm["u"], color=color_lefm, linestyle=linestyle_LEFM, label=LABEL_LEFM,linewidth=2)
axins.plot(simulation["ref"]["gamma"], simulation["ref"]["stiffness"], color=color_1, linestyle=linestyle_1)
axins.plot(simulation["bourdin"]["gamma"], simulation["bourdin"]["stiffness"], color=color_2, linestyle=linestyle_2)
axins.plot(simulation["dgcm"]["gamma"], simulation["dgcm"]["stiffness"], color=color_3, linestyle=linestyle_3)

# sub region of the original image
x1, x2, y1, y2 = 0.4999, 0.5025, 66.4, 66.7
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticks([])
axins.set_yticks([])

axins.spines['top'].set_visible(True)
axins.spines['right'].set_visible(True)

ax_ref0.indicate_inset_zoom(axins)


ax_ref0.set_xlabel(pcfg.crack_length_label)
ax_ref0.set_ylabel(pcfg.stiffness_label)

ax_ref0.legend()
plt.savefig(os.path.join(results_folder, "stiffness_area"))


plt.show()
