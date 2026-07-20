r"""
.. _ref_TheoryPhaseField_plot_profiles:

Phase-Field Profiles for a 1D Bar
---------------------------------
This script computes and plots the analytical phase-field profiles for a crack
centered at :math:`x = 0` in a one-dimensional bar of half-length :math:`a`,
i.e., the domain :math:`[-a, a]`.

For both the AT1 and AT2 regularization models, the script generates two figures:

* The phase-field profile :math:`\phi(x)` as a function of normalized position :math:`x/a`.
* The gradient :math:`\phi'(x)` of the phase-field profile.

Three values of the dimensionless ratio :math:`l/a` are compared in each figure
to illustrate how the length-scale parameter controls the width of the
transition zone and how boundary effects arise when :math:`l` is comparable
to the bar half-length :math:`a`.
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


###############################################################################
# Parameters definitions
# ----------------------
# These parameters define the length scale and the half-length of the bar for the phase field profiles.

a = 1.0
x_div_a = np.linspace(-a, a, 10000)/a

l1 = 0.1*a
l2 = 0.5*a
l3 = 1.2*a

l1_label = r"$l/a=0.1$"
l2_label = r"$l/a=0.5$"
l3_label = r"$l/a=1.2$"


###############################################################################
# AT2 Phase-field model
# ---------------------
color_2 = pcfg.color_red
markevery_2 = max(1, len(x_div_a)//20)

phi_at2_profile_l1 = phi_at2(x_div_a, l1, a)
gradphi_at2_profile_l1 = gradphi_at2(x_div_a, l1, a)
label_at2_l1 = l1_label

phi_at2_profile_l2 = phi_at2(x_div_a, l2, a)
gradphi_at2_profile_l2 = gradphi_at2(x_div_a, l2, a)
label_at2_l2 = l2_label

phi_at2_profile_l3 = phi_at2(x_div_a, l3, a)
gradphi_at2_profile_l3 = gradphi_at2(x_div_a, l3, a)
label_at2_l3 = l3_label


###############################################################################
# Figure: x/a vs. Phase-field
# ---------------------------
color_l1 = pcfg.color_blue
color_l2 = pcfg.color_orangered
color_l3 = pcfg.color_purple

fig, ax_at2_phi = plt.subplots()
ax_at2_phi.plot(x_div_a, phi_at2_profile_l1, color=color_l1, linestyle='--', label=label_at2_l1, markevery=markevery_2, marker='o')
ax_at2_phi.plot(x_div_a, phi_at2_profile_l2, color=color_l2, linestyle='-.', label=label_at2_l2, markevery=markevery_2, marker='s')
ax_at2_phi.plot(x_div_a, phi_at2_profile_l3, color=color_l3, linestyle=':', label=label_at2_l3, markevery=markevery_2, marker='^')

ax_at2_phi.set_xlabel(pcfg.length_div_a_1d_label)
ax_at2_phi.set_ylabel((pcfg.phi_profile_1d))
# ax_at2_phi.legend()
if save_figures:
    plt.savefig(os.path.join(results_folder, "at2_phi_profile_l1_l2_l3"))


###############################################################################
# Figure: x/a vs. Phase-field Gradient
# ------------------------------------
fig, ax_at2_gradphi = plt.subplots()

# l/a = 0.1
ax_at2_gradphi.plot(x_div_a[0:int(len(x_div_a)/2)], gradphi_at2_profile_l1[0:int(len(x_div_a)/2)], color=color_l1, linestyle='--', label=label_at2_l1, markevery=markevery_2, marker='o')
ax_at2_gradphi.plot(x_div_a[1+int(len(x_div_a)/2):], gradphi_at2_profile_l1[1+int(len(x_div_a)/2):], color=color_l1, linestyle='--', markevery=markevery_2, marker='o')

# l/a = 0.2
ax_at2_gradphi.plot(x_div_a[0:int(len(x_div_a)/2)], gradphi_at2_profile_l2[0:int(len(x_div_a)/2)], color=color_l2, linestyle='-.', label=label_at2_l2, markevery=markevery_2, marker='s')
ax_at2_gradphi.plot(x_div_a[1+int(len(x_div_a)/2):], gradphi_at2_profile_l2[1+int(len(x_div_a)/2):], color=color_l2, linestyle='-.', markevery=markevery_2, marker='s')

# l/a = 1.2
ax_at2_gradphi.plot(x_div_a[0:int(len(x_div_a)/2)], gradphi_at2_profile_l3[0:int(len(x_div_a)/2)], color=color_l3, linestyle=':', label=label_at2_l3, markevery=markevery_2, marker='^')
ax_at2_gradphi.plot(x_div_a[1+int(len(x_div_a)/2):], gradphi_at2_profile_l3[1+int(len(x_div_a)/2):], color=color_l3, linestyle=':', markevery=markevery_2, marker='^')

ax_at2_gradphi.set_xlabel(pcfg.length_div_a_1d_label)
ax_at2_gradphi.set_ylabel(pcfg.gradphi_profile_1d)
ax_at2_gradphi.legend()
if save_figures:
    plt.savefig(os.path.join(results_folder, "at2_gradphi_profile_l1_l2_l3"))



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
x_div_a = np.linspace(-a, a, 10000)/a

l1 = 0.1*a
l2 = 0.5*a
l3 = 1.2*a

l1_label = r"$l/a=0.1$"
l2_label = r"$l/a=0.5$"
l3_label = r"$l/a=1.2$"


###############################################################################
# AT1 Phase-field model
# ---------------------
color_2 = pcfg.color_red
markevery_2 = max(1, len(x_div_a)//20)

phi_at2_profile_l1 = phi_at1(x_div_a, l1, a)
gradphi_at2_profile_l1 = gradphi_at1(x_div_a, l1, a)
label_at2_l1 = l1_label

phi_at2_profile_l2 = phi_at1(x_div_a, l2, a)
gradphi_at2_profile_l2 = gradphi_at1(x_div_a, l2, a)
label_at2_l2 = l2_label

phi_at2_profile_l3 = phi_at1(x_div_a, l3, a)
gradphi_at2_profile_l3 = gradphi_at1(x_div_a, l3, a)
label_at2_l3 = l3_label


###############################################################################
# Figure: x/a vs. Phase-field
# ---------------------------
color_l1 = pcfg.color_blue
color_l2 = pcfg.color_orangered
color_l3 = pcfg.color_purple

fig, ax_at1_phi = plt.subplots()
ax_at1_phi.plot(x_div_a, phi_at2_profile_l1, color=color_l1, linestyle='--', label=label_at2_l1, markevery=markevery_2, marker='o')
ax_at1_phi.plot(x_div_a, phi_at2_profile_l2, color=color_l2, linestyle='-.', label=label_at2_l2, markevery=markevery_2, marker='s')
ax_at1_phi.plot(x_div_a, phi_at2_profile_l3, color=color_l3, linestyle=':', label=label_at2_l3, markevery=markevery_2, marker='^')

ax_at1_phi.set_xlabel(pcfg.length_div_a_1d_label)
ax_at1_phi.set_ylabel((pcfg.phi_profile_1d))
# ax_at2_phi.legend()
if save_figures:
    plt.savefig(os.path.join(results_folder, "at1_phi_profile_l1_l2_l3"))


###############################################################################
# Figure: x/a vs. Phase-field Gradient
# ------------------------------------
fig, ax_at1_gradphi = plt.subplots()

# l/a = 0.1
ax_at1_gradphi.plot(x_div_a[0:int(len(x_div_a)/2)], gradphi_at2_profile_l1[0:int(len(x_div_a)/2)], color=color_l1, linestyle='--', label=label_at2_l1, markevery=markevery_2, marker='o')
ax_at1_gradphi.plot(x_div_a[1+int(len(x_div_a)/2):], gradphi_at2_profile_l1[1+int(len(x_div_a)/2):], color=color_l1, linestyle='--', markevery=markevery_2, marker='o')

# l/a = 0.5
ax_at1_gradphi.plot(x_div_a[0:int(len(x_div_a)/2)], gradphi_at2_profile_l2[0:int(len(x_div_a)/2)], color=color_l2, linestyle='-.', label=label_at2_l2, markevery=markevery_2, marker='s')
ax_at1_gradphi.plot(x_div_a[1+int(len(x_div_a)/2):], gradphi_at2_profile_l2[1+int(len(x_div_a)/2):], color=color_l2, linestyle='-.', markevery=markevery_2, marker='s')

# l/a = 1.2
ax_at1_gradphi.plot(x_div_a[0:int(len(x_div_a)/2)], gradphi_at2_profile_l3[0:int(len(x_div_a)/2)], color=color_l3, linestyle=':', label=label_at2_l3, markevery=markevery_2, marker='^')
ax_at1_gradphi.plot(x_div_a[1+int(len(x_div_a)/2):], gradphi_at2_profile_l3[1+int(len(x_div_a)/2):], color=color_l3, linestyle=':', markevery=markevery_2, marker='^')

ax_at1_gradphi.set_xlabel(pcfg.length_div_a_1d_label)
ax_at1_gradphi.set_ylabel(pcfg.gradphi_profile_1d)
ax_at1_gradphi.legend()
if save_figures:
    plt.savefig(os.path.join(results_folder, "at1_gradphi_profile_l1_l2_l3"))

plt.show()
