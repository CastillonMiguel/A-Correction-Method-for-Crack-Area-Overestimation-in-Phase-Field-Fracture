r"""
.. _ref_compare_lenght_scale_at1:

Effect of length scale at constant :math:`l/h` ratio (AT1)
-----------------------------------------------------------

This script is the AT1 counterpart of :ref:`ref_compare_lenght_scale`. It compares the DGCM
correction factor and structural stiffness across the three AT1 convergence simulations
(see :ref:`ref_examples_phase_field_central_crack_at1`). The length scale :math:`l` is reduced
while keeping :math:`l/h = 2.5` fixed.

For the AT1 model the Bourdin correction factor reads
:math:`1 + h/(c_0 l)` with :math:`c_0 = 8/3`, so the horizontal reference line differs
from the AT2 case.

**Plots generated**

- DGCM correction factor :math:`\mathcal{F}` vs. crack length :math:`\Gamma` for the three AT1 simulations.
- Structural stiffness :math:`K` vs. applied force :math:`P`, compared against the LEFM reference.

**Simulations used** (from :ref:`ref_examples_phase_field_central_crack_at1`)

+-------------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| #                       | :math:`\alpha` | :math:`\theta` | Length scale :math:`l` (mm)   | Mesh size :math:`h` (mm) | :math:`l/h` |
+=========================+================+================+===============================+==========================+=============+
| :ref:`ref_cc_sim1_at1`  | 1.0            | 1.0            | 0.012500                      | 0.005000                 | 2.5         |
+-------------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim2_at1`  | 0.2            | 0.2            | 0.002500                      | 0.001000                 | 2.5         |
+-------------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim3_at1`  | 0.1            | 0.1            | 0.001250                      | 0.000500                 | 2.5         |
+-------------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
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

results_folder = "results_compare_lenght_scale_AT1"
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

# Define paths and load data
# Common base path for all simulation results
base_results_path = "../Central_cracked_all_at1"

# NOTE: All paths start with ../central_cracked_all_at1
# Define only the final part of each path, then prepend base_results_path to all
path_list_final = [
    "results_cc_sim_1",
    "results_cc_sim_2",
    "results_cc_sim_3"
]
path_list = [f"{base_results_path}/{final}" for final in path_list_final]


# l/h = 2.5 simulations
# alpha_lh_25 = np.array([1.0, 0.2, 0.1, 0.05])
# beta_lh_25  = np.array([1.0, 0.2, 0.1, 0.05])

simulation_1 = load_simulation_data(path_list[0])
simulation_2 = load_simulation_data(path_list[1])
simulation_3 = load_simulation_data(path_list[2])


label_lh_1 = r"$l=0.0125$"
label_lh_2 = r"$l=0.0025$"
label_lh_3 = r"$l=0.00125$"

color_1, linestyle_1, marker_1 = pcfg.color_blue, '-', 'o'
color_2, linestyle_2, marker_2 = pcfg.color_orangered, '--', 's'
color_3, linestyle_3, marker_3 = pcfg.color_gold, '--', '^'

markevery_1 = max(1, len(simulation_1["ref"]["displacement"])//20) if simulation_1["ref"] is not None else 1
markevery_2 = max(1, len(simulation_2["ref"]["displacement"])//20) if simulation_2["ref"] is not None else 1
markevery_3 = max(1, len(simulation_3["ref"]["displacement"])//20) if simulation_3["ref"] is not None else 1


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

label_reference = r"Reference"
label_bourdin = r"Bourdin"
label_dgcm = r"DGCM"

from phasefieldx.Element.Phase_Field.geometric_crack import geometric_crack_coefficient

c0 = geometric_crack_coefficient('AT1')

###############################################################################
# Plot: Gamma vs Correction Factor
# --------------------------------
hdivl=2.5
fig, ax_l1_uf = plt.subplots()

ax_l1_uf.axhline(y=1+2*1/(c0*hdivl), color=color_lefm, linestyle='-', label="Bourdin")

ax_l1_uf.plot(simulation_1["dgcm"]["gamma"], simulation_1["dgcm"]["Ofactor"], color=color_1, linestyle=linestyle_1, label=label_lh_1, markevery=markevery_1, marker=marker_1)
ax_l1_uf.plot(simulation_2["dgcm"]["gamma"], simulation_2["dgcm"]["Ofactor"], color=color_2, linestyle=linestyle_2, label=label_lh_2, markevery=markevery_2, marker=marker_2)
ax_l1_uf.plot(simulation_3["dgcm"]["gamma"], simulation_3["dgcm"]["Ofactor"], color=color_3, linestyle=linestyle_3, label=label_lh_3, markevery=markevery_3, marker=marker_3)

ax_l1_uf.set_xlabel(pcfg.gamma_label)
ax_l1_uf.set_ylabel(pcfg.correction_factor)
ax_l1_uf.legend()

ax_l1_uf.set_ylim(1.00, 1.4)
plt.savefig(os.path.join(results_folder, "compare_correction_factor_constant_l_h_2_5"))



###############################################################################
# Plot: Gamma vs Correction Factor
# --------------------------------
fig, ax_l1_uf = plt.subplots()


ax_l1_uf.plot(results_lefm["P"], results_lefm["P"]/results_lefm["u"], color=color_lefm, linestyle=linestyle_LEFM, label=LABEL_LEFM)
ax_l1_uf.plot(simulation_1["dgcm"]["force"], simulation_1["dgcm"]["stiffness"], color=color_1, linestyle=linestyle_1, label=label_lh_1, markevery=markevery_1, marker=marker_1)
ax_l1_uf.plot(simulation_2["dgcm"]["force"], simulation_2["dgcm"]["stiffness"], color=color_2, linestyle=linestyle_2, label=label_lh_2, markevery=markevery_2, marker=marker_2)
ax_l1_uf.plot(simulation_3["dgcm"]["force"], simulation_3["dgcm"]["stiffness"], color=color_3, linestyle=linestyle_3, label=label_lh_3, markevery=markevery_3, marker=marker_3)

ax_l1_uf.set_xlabel(pcfg.force_label)
ax_l1_uf.set_ylabel(pcfg.stiffness_label)
ax_l1_uf.legend()

ax_l1_uf.set_xlim(-0.05, 1.5)
ax_l1_uf.set_ylim(45, 70.0)

plt.savefig(os.path.join(results_folder, "force_stiffness_constant_l_h_2_5"))



plt.show()
