r"""
.. _ref_paper_miguel_fatigue:

Visualization papers resuls: A Phase Field Approach to Fatigue
--------------------------------------------------------------

This script reproduces several key figures from the paper :footcite:t:`phase_field_Castillon2025`. In concrete some of the lefm results for the center cracked specimen.

.. footbibliography::

"""

###############################################################################
# Import required libraries
# -------------------------
# Import standard libraries for numerical operations and plotting, and set up the
# project-specific plotting style and configuration.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add the parent directory to the system path to allow imports from the project root.
sys.path.insert(0, os.path.abspath('../../'))
plt.style.use('../../graph.mplstyle')
import plot_config as pcfg


path = "A_Phase_Field_Approach_to_Fatigue/results_central_cracked"
results_a0_05  = pd.read_csv(os.path.join(path, "a0_05.lefm_problem"), delimiter="\t", comment="#", header=0)


###############################################################################
# Figure: Force vs Displacement
# -----------------------------
fig, ax0 = plt.subplots()

ax0.plot(results_a0_05["u"], results_a0_05["P"], 'k-')

ax0.set_xlabel("displacement (mm)")
ax0.set_ylabel("force (kN)")
ax0.legend()


###############################################################################
# Figure: Stiffness vs crack length
# ---------------------------------
fig, ax0 = plt.subplots()

ax0.plot(results_a0_05["a"], results_a0_05["P"]/results_a0_05["u"], 'k-')

ax0.set_xlabel("crack length (mm)")
ax0.set_ylabel("stiffness (kN/mm)")
ax0.legend()


###############################################################################
# Figure: Stiffness vs crack length
# ---------------------------------
fig, ax0 = plt.subplots()

ax0.plot(results_a0_05["a"], results_a0_05["P"], 'k-')

ax0.set_xlabel("crack length (mm)")
ax0.set_ylabel("force (kN)")
ax0.legend()


plt.show()
