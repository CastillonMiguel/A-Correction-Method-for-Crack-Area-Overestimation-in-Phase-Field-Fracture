r"""

.. _ref_TheoryPhaseField_plot_profiles:

Phase-Field Profiles for a 1D Bar (AT2/AT2)
-------------------------------------------

This script calculates and plots theoretical phase-field profiles for a crack
in a one-dimensional bar. The crack is centered at x=0 within a domain of [-a, a].

The profiles represent the analytical solutions to the ordinary differential
equations (ODEs) that govern the phase-field variable for different models (AT1, AT2, and Wu).
The script demonstrates how varying the length-scale parameter `l` affects the
solution, including boundary effects.

When the length-scale parameter is small relative to the domain size, the
phase-field solution approximates the sharp crack profile.

"""

###############################################################################
# Import necessary libraries
# --------------------------
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

sys.path.insert(0, os.path.abspath('../../'))
plt.style.use('../../graph.mplstyle')
import plot_config as pcfg

save_figures = True
if save_figures:
    results_folder = "results_plot_profiles"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

###############################################################################
# Phase field profile functions
# ------------------------------
# These functions define the phase field profiles and their gradients for different formulations.
def phi_at2(x, length_scale, a):
    """
    Phase field profile AT2

    Parameters:
    - x: Position along the bar.
    - length_scale: Length scale parameter controlling the width of the transition zone.
    - a: Half-length of the bar [-a, a].

    Returns:
    - Phase field value at position x.
    """
    one_div_exp2adivl_one = 1 / (np.exp(2 * a / length_scale) + 1)
    return np.exp(-abs(x) / length_scale) + one_div_exp2adivl_one * 2 * np.sinh(np.abs(x) / length_scale)


def gradphi_at2(x, length_scale, a):
    """
    Gradient of the phase field for the phi_at2 formulation.

    Parameters:
    - x: Position along the bar.
    - length_scale: Length scale parameter controlling the width of the transition zone.
    - a: Half-length of the bar [-a, a].

    Returns:
    - Gradient of the phase field at position x.
    """
    one_div_exp2adivl_one = 1 / (np.exp(2 * a / length_scale) + 1)
    return -np.sign(x) / length_scale * np.exp(-abs(x) / length_scale) \
        + one_div_exp2adivl_one * np.sign(x) / length_scale * 2 * np.cosh(np.abs(x) / length_scale)


def phi_at1(x, length_scale, a):
    """
    Phase field profile AT1

    Parameters:
    - x: Position along the bar.
    - length_scale: Length scale parameter controlling the width of the transition zone.
    - a: Half-length of the bar [-a, a].

    Returns:
    - Phase field value at position x.
    """
    control1 = np.heaviside(2 * length_scale - abs(x), 0)
    control2 = np.heaviside(2 * length_scale - a, 0)
    phi = (abs(x**2) / (4 * length_scale**2) - abs(x) / (length_scale) + 1) * control1
    phi += abs(x) / length_scale * (1 - a / (2 * length_scale)) * control2
    return phi


def gradphi_at1(x, length_scale, a):
    """
    Gradient of the phase field for the phi_at1 formulation.

    Parameters:
    - x: Position along the bar.
    - length_scale: Length scale parameter controlling the width of the transition zone.
    - a: Half-length of the bar [-a, a].

    Returns:
    - Gradient of the phase field at position x.
    """
    control1 = np.heaviside(2 * length_scale - abs(x), 0)
    control2 = np.heaviside(2 * length_scale - a, 0)
    gradphi = ((x) / (2 * length_scale**2) - np.sign(x) / length_scale) * control1
    gradphi += np.sign(x) / length_scale * (1 - a / (2 * length_scale)) * control2
    return gradphi

###############################################################################
# Parameters definitions
# ----------------------
# These parameters define the length scale and the half-length of the bar for the phase field profiles.

a = 1.0
x = np.linspace(-a, a, 10000)
x_left = np.linspace(-a, 0.0, 10000)
x_right = np.linspace(0.0, a, 10000)
h = 0.1
left_mask = x <= -h
right_mask = x >= h

l = 0.1*a
l1 = 0.1*a
l2 = 0.5*a
l3 = 1.2*a

l1_label = r"$l/a=0.1$"
l2_label = r"$l/a=0.5$"
l3_label = r"$l/a=1.2$"

color_l1 = pcfg.color_blue
color_l2 = pcfg.color_orangered
color_l3 = pcfg.color_purple


label_1 = r"AT1"
color_1 = pcfg.color_black
markevery_1 = max(1, len(x)//20)

###############################################################################
# AT2 Phase-field model
# ---------------------
label_2 = r"AT2"
color_2 = pcfg.color_red
markevery_2 = max(1, len(x)//20)

# Split left/right as in AT1
phi_at2_profile_l1_left = phi_at2(x_left, l1, a)
phi_at2_profile_l1_right = phi_at2(x_right, l1, a)
gradphi_at2_profile_l1_left = gradphi_at2(x_left, l1, a)
gradphi_at2_profile_l1_right = gradphi_at2(x_right, l1, a)
label_at2_l1 = l1_label

# Split left/right as in AT1
phi_at1_profile_l1_left = phi_at1(x_left, l1, a)
phi_at1_profile_l1_right = phi_at1(x_right, l1, a)
gradphi_at1_profile_l1_left = gradphi_at1(x_left, l1, a)
gradphi_at1_profile_l1_right = gradphi_at1(x_right, l1, a)
label_at1_l1 = l1_label


# %%
# AT2 Phase Field Profile
fig, ax_at2_phi = plt.subplots()

ax_at2_phi.plot(x_left-h, phi_at1_profile_l1_left, color=color_1, linestyle='-', label=label_1, markevery=markevery_1)
ax_at2_phi.plot(x_right+h, phi_at1_profile_l1_right, color=color_1, linestyle='-', markevery=markevery_1)
ax_at2_phi.hlines(1.0, -h, h, colors=color_1, linestyles='-')

ax_at2_phi.plot(x_left-h, phi_at2_profile_l1_left, color=color_2, linestyle='--', label=label_2, markevery=markevery_2)
ax_at2_phi.plot(x_right+h, phi_at2_profile_l1_right, color=color_2, linestyle='--', markevery=markevery_2)
ax_at2_phi.hlines(1.0, -h, h, colors=color_2, linestyles='--')

ax_at2_phi.set_xlabel(r"$x/a$")
ax_at2_phi.set_ylabel(r"$\phi(x)$")
ax_at2_phi.legend()
if save_figures:
    plt.savefig(os.path.join(results_folder, "phi_profile"))

# %%
# AT2 Phase Field gradient Profile
fig, ax_at2_gradphi = plt.subplots()

ax_at2_gradphi.plot(x_left[:-1]-h, gradphi_at1_profile_l1_left[:-1], color=color_1, linestyle='-', label=label_1, markevery=markevery_1)
ax_at2_gradphi.plot(x_right[1:]+h, gradphi_at1_profile_l1_right[1:], color=color_1, linestyle='-', markevery=markevery_1)
ax_at2_gradphi.hlines(0.0, -h, h, colors=color_1, linestyles='-')

ax_at2_gradphi.plot(x_left[:-1]-h, gradphi_at2_profile_l1_left[:-1], color=color_2, linestyle='--', label=label_2, markevery=markevery_2)
ax_at2_gradphi.plot(x_right[1:]+h, gradphi_at2_profile_l1_right[1:], color=color_2, linestyle='--', markevery=markevery_2)
ax_at2_gradphi.hlines(0.0, -h, h, colors=color_2, linestyles='--')

ax_at2_gradphi.set_xlabel(r"$x/a$")
ax_at2_gradphi.set_ylabel((r"$\phi'(x)$"))
if save_figures:
    plt.savefig(os.path.join(results_folder, "gradphi_profile"))


plt.show()
