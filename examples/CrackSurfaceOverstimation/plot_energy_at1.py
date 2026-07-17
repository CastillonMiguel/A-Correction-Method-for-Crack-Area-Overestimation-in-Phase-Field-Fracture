r"""

.. _ref_TheoryPhaseField_plot_energy_at1:

Phase-field energies (1D bar) AT1
---------------------------------

This script provides functions and plots for the analytical energy expressions of phase-field fracture models (AT1, AT2, Wu) for a 1D bar with a centered crack. The phase-field approach models cracks as smooth transitions, and the energy is split into phase, gradient, and total contributions.

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
    results_folder = "results_plot_energy_at1"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)


###############################################################################
# Energy computation functions
# ----------------------------
# These functions compute the phase, gradient, and total energy contributions
# for the AT1, AT2, and Wu phase-field models.

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

def gamma_at1(length_scale, bar_half_length):
    """
    Compute the total energy for the AT2 phase-field model.

    Parameters
    ----------
    length_scale : array_like
        Length scale parameter(s).
    bar_half_length : float
        Half-length of the bar [-a, a].

    Returns
    -------
    ndarray
        Total energy for the AT1 model.
    """
    return gamma_phi_at1(length_scale, bar_half_length) + gamma_gradphi_at1(length_scale, bar_half_length)


def gamma_at1_stl(length_scale, bar_half_length, h):
    """
    Compute the total energy for the AT2 phase-field model.

    Parameters
    ----------
    length_scale : array_like
        Length scale parameter(s).
    bar_half_length : float
        Half-length of the bar [-a, a].

    Returns
    -------
    ndarray
        Total energy for the AT2 model.
    """
    # a_div_l = bar_half_length / length_scale
    # tanh_a_div_l = np.tanh(a_div_l) + h/(2*length_scale)
    c0 = 8.0/3.0
    return gamma_at1(length_scale, bar_half_length) + h/(c0*length_scale)


def gamma_phi_at1_stl(length_scale, bar_half_length, h):
    """
    Compute the phase-field energy contribution for the AT2 model.

    Parameters
    ----------
    length_scale : array_like
        Length scale parameter(s).
    bar_half_length : float
        Half-length of the bar [-a, a].

    Returns
    -------
    ndarray
        Phase-field energy for the AT2 model.
    """
    a_div_l = bar_half_length / length_scale
    c0=8.0/3.0
    return gamma_phi_at1(length_scale, bar_half_length) + h/(c0*length_scale)


def gamma_gradphi_at1_stl(length_scale, bar_half_length):
    """
    Compute the gradient energy contribution for the AT2 model.

    Parameters
    ----------
    length_scale : array_like
        Length scale parameter(s).
    bar_half_length : float
        Half-length of the bar [-a, a].

    Returns
    -------
    ndarray
        Gradient energy for the AT2 model.
    """
    a_div_l = bar_half_length / length_scale
    tanh_a_div_l = np.tanh(a_div_l)
    return gamma_gradphi_at1(length_scale, bar_half_length)


###############################################################################
# Parameters definitions
# ----------------------
# Define the length scale and the half-length of the bar for the energy models.
bar_half_length = 1.0  #: Half-length of the bar [-a, a]
step_size = 0.005  #: Step size for the length scale array
length_scale = np.arange(0.005, 2 * bar_half_length,
                         step_size)  #: Length scale array
length_scale_div_a = length_scale / bar_half_length


###############################################################################
# AT2 Phase-field model
# ---------------------
label_2 = r"AT1"
color_2 = pcfg.color_red if hasattr(pcfg, 'color_red') else 'red'
markevery_2 = max(1, len(length_scale)//10)
markevery_22 = max(1, len(length_scale)//12)

phi_at1_energy = gamma_phi_at1(length_scale, bar_half_length)
gradphi_at1_energy = gamma_gradphi_at1(length_scale, bar_half_length)
total_at1_energy = gamma_at1(length_scale, bar_half_length)

# Plot: AT2 Model Energies
fig, ax = plt.subplots(figsize=(11.69, 5.85))
ax.plot(length_scale_div_a, total_at1_energy, color=pcfg.color_black,
        linestyle='-', label=pcfg.energy_1d, markevery=markevery_2,
        marker='^')  # square marker for total energy
ax.plot(length_scale_div_a, phi_at1_energy, color=pcfg.color_blue,
        linestyle='-', label=pcfg.phi_energy_1d, markevery=markevery_2,
        marker='o')  # triangle marker for phi energy
ax.plot(length_scale_div_a, gradphi_at1_energy, color=pcfg.color_red,
        linestyle='-', label=pcfg.gradphi_energy_1d, markevery=markevery_22,
        marker='s', markerfacecolor='none')  # diamond marker for gradphi energy, not filled

ax.plot(length_scale_div_a,  gamma_at1_stl(length_scale, bar_half_length,h=0.1), color='green',
        linestyle='--', label="$h/a = 0.1$", markevery=markevery_2,
        marker='^')  # square marker for total energy
ax.plot(length_scale_div_a,  gamma_phi_at1_stl(length_scale, bar_half_length,h=0.1), color='orange',
        linestyle='--', label="$h/a = 0.1$", markevery=markevery_2,
        marker='o')  # triangle marker for phi energy
ax.plot(length_scale_div_a, gamma_gradphi_at1_stl(length_scale, bar_half_length), color='brown',
        linestyle='--', label="$h/a = 0.1$", markevery=markevery_22,
        marker='s', markerfacecolor='none')  # diamond marker for gradphi energy, not filled

ax.set_ylim(0.0, 1.2)
ax.set_xlabel(pcfg.length_l_div_a)
ax.set_ylabel(pcfg.gamma_label)
ax.legend()


###############################################################################
# AT2 Phase-field model
# ---------------------
label_2 = r"AT2"
color_2 = pcfg.color_red if hasattr(pcfg, 'color_red') else 'red'
markevery_2 = max(1, len(length_scale)//10)
markevery_22 = max(1, len(length_scale)//12)

# Plot: AT2 Model Energies
fig, ax = plt.subplots()

ax.plot(length_scale_div_a, phi_at1_energy, color=pcfg.color_black,
        linestyle='-', label="Theory", markevery=markevery_2,
        marker='o')  # triangle marker for phi energy


ax.plot(length_scale_div_a, gamma_phi_at1_stl(length_scale, bar_half_length, h=0.1),
    color='orange', linestyle='--', label="$h/a = 0.1$", markevery=markevery_2,
    marker='D')  # diamond marker, orange

ax.plot(length_scale_div_a, gamma_phi_at1_stl(length_scale, bar_half_length, h=0.01),
    color='green', linestyle='-.', label="$h/a = 0.01$", markevery=markevery_2,
    marker='^')  # triangle up marker, green

ax.plot(length_scale_div_a, gamma_phi_at1_stl(length_scale, bar_half_length, h=0.001),
    color='purple', linestyle=':', label="$h/a = 0.001$", markevery=markevery_2,
    marker='v')  # triangle down marker, purple

ax.plot(length_scale_div_a, gamma_phi_at1_stl(length_scale, bar_half_length, h=0.0001),
    color='brown', linestyle='--', label="$h/a = 0.0001$", markevery=markevery_2,
    marker='s')  # square marker, brown

ax.set_ylim(0.4, 0.8)
ax.set_xlabel(pcfg.length_l_div_a)
ax.set_ylabel(pcfg.gamma_phi_label)
# ax.legend()
if save_figures:
    plt.savefig(os.path.join(results_folder, "at1_phi_strain_energy"))




# Plot: AT2 Model Energies
fig, ax = plt.subplots()

ax.plot(length_scale_div_a, total_at1_energy, color=pcfg.color_black,
        linestyle='-', label="Theory", markevery=markevery_2,
        marker='o')  # triangle marker for phi energy

ax.plot(length_scale_div_a, gamma_at1_stl(length_scale, bar_half_length, h=0.1),
    color='orange', linestyle='--', label="$h/a = 0.1$", markevery=markevery_2,
    marker='D')  # diamond marker, orange

ax.plot(length_scale_div_a, gamma_at1_stl(length_scale, bar_half_length, h=0.01),
    color='green', linestyle='-.', label="$h/a = 0.01$", markevery=markevery_2,
    marker='^')  # triangle up marker, green

ax.plot(length_scale_div_a, gamma_at1_stl(length_scale, bar_half_length, h=0.001),
    color='purple', linestyle=':', label="$h/a = 0.001$", markevery=markevery_2,
    marker='v')  # triangle down marker, purple

ax.plot(length_scale_div_a, gamma_at1_stl(length_scale, bar_half_length, h=0.0001),
    color='brown', linestyle='--', label="$h/a = 0.0001$", markevery=markevery_2,
    marker='s')  # square marker, brown

ax.set_ylim(0.4, 1.2)
ax.set_xlabel(pcfg.length_l_div_a)
ax.set_ylabel(pcfg.energy_1d)
ax.legend()
if save_figures:
    plt.savefig(os.path.join(results_folder, "at1_strain_energy"))


plt.show()
