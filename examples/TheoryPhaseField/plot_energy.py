r"""
.. _ref_TheoryPhaseField_plot_energy:

Phase-field energies (1D bar)
-----------------------------

This script computes and plots analytical expressions for the phase-field crack
surface density functional (AT2/AT1) for a one-dimensional bar with a centered
crack. The phase-field method represents cracks as smooth transitions and
splits the energy into three contributions: phase (potential) energy,
gradient energy, and total energy.

The file provides functions that return closed-form energy contributions for
the AT2/AT1 models and produces plots of each contribution as a function of the
length-scale parameter.
"""


###############################################################################
# Import necessary libraries
# --------------------------
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Import plotting configuration
sys.path.insert(0, os.path.abspath('../../'))
plt.style.use('../../graph.mplstyle')
import plot_config as pcfg

# -- Output folder setup --
save_figures = True
if save_figures:
    results_folder = "results_plot_energy"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)


###############################################################################
# Parameters definitions
# ----------------------
# Define the length scale and the half-length of the bar for the energy models.
bar_half_length = 1.0  #: Half-length of the bar [-a, a]
step_size = 0.001  #: Step size for the length scale array
length_scale = np.arange(0.001, 2 * bar_half_length,
                         step_size)  #: Length scale array
l_div_a = length_scale / bar_half_length
a_div_l = 1/l_div_a

###############################################################################
# AT2 Phase-field model
# ---------------------
phi_at2_energy = 0.5 * np.tanh(a_div_l) + 0.5 * a_div_l * (1.0 - np.tanh(a_div_l)**2)
gradphi_at2_energy = 0.5 * np.tanh(a_div_l) - 0.5 * a_div_l * (1.0 - np.tanh(a_div_l)**2)
total_at2_energy = np.tanh(a_div_l)


###############################################################################
# Figure: l/a vs. Phase-field energies
# ------------------------------------

markevery_gamma = max(1, len(length_scale)//10)
markevery_gamma_phi = max(1, len(length_scale)//10)
markevery_gamma_gradphi = max(1, len(length_scale)//12)

fig, ax = plt.subplots()
ax.plot(l_div_a, total_at2_energy, color=pcfg.color_black,
        linestyle='-', label=pcfg.energy_1d, markevery=markevery_gamma,
        marker='^') 
ax.plot(l_div_a, phi_at2_energy, color=pcfg.color_blue,
        linestyle='--', label=pcfg.phi_energy_1d, markevery=markevery_gamma_phi,
        marker='o')
ax.plot(l_div_a, gradphi_at2_energy, color=pcfg.color_red,
        linestyle=':', label=pcfg.gradphi_energy_1d, markevery=markevery_gamma_gradphi,
        marker='s', markerfacecolor='none')
ax.set_xlabel(pcfg.length_l_div_a)
ax.set_ylabel("Energy")
ax.legend()
if save_figures:
    plt.savefig(os.path.join(results_folder, "at2_energy"))

###############################################################################
# AT1 Phase-field model
# ---------------------

def gamma_phi_at1(length_scale, bar_half_length):
    """
    Compute the phase-field energy contribution for the AT1 model.

    Parameters
    ----------
    length_scale : array_like
        Length scale parameter(s).
    bar_half_length : float
        Half-length of the bar [-a, a].

    Returns
    -------
    ndarray
        Phase-field energy for the AT1 model.
    """
    control = np.heaviside(2 * length_scale - bar_half_length, 0)
    w_phi_o_a = 0.5
    w_phi_o_b = (-(bar_half_length**3 / (8 * length_scale**3)) +
                 3 * bar_half_length / (4 * length_scale))
    return (1 - control) * w_phi_o_a + control * w_phi_o_b


def gamma_gradphi_at1(length_scale, bar_half_length):
    """
    Compute the gradient energy contribution for the AT1 model.

    Parameters
    ----------
    length_scale : array_like
        Length scale parameter(s).
    bar_half_length : float
        Half-length of the bar [-a, a].

    Returns
    -------
    ndarray
        Gradient energy for the AT1 model.
    """
    control = np.heaviside(2 * length_scale - bar_half_length, 0)
    w_gradphi_o_a = 0.5
    w_gradphi_o_b = (bar_half_length**3 / (16 * length_scale**3))
    return (1 - control) * w_gradphi_o_a + control * w_gradphi_o_b

phi_at1_energy = gamma_phi_at1(length_scale, bar_half_length)
gradphi_at1_energy = gamma_gradphi_at1(length_scale, bar_half_length)
total_at1_energy = phi_at1_energy + gradphi_at1_energy

fig, ax = plt.subplots()
ax.plot(l_div_a, total_at1_energy, color=pcfg.color_black,
        linestyle='-', label=pcfg.energy_1d, markevery=markevery_gamma,
        marker='^') 
ax.plot(l_div_a, phi_at1_energy, color=pcfg.color_blue,
        linestyle='--', label=pcfg.phi_energy_1d, markevery=markevery_gamma_phi,
        marker='o')
ax.plot(l_div_a, gradphi_at1_energy, color=pcfg.color_red,
        linestyle=':', label=pcfg.gradphi_energy_1d, markevery=markevery_gamma_gradphi,
        marker='s', markerfacecolor='none')
ax.set_xlabel(pcfg.length_l_div_a)
ax.set_ylabel("Energy")
ax.legend()
if save_figures:
    plt.savefig(os.path.join(results_folder, "at1_energy"))

plt.show()
