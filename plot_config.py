# filepath: ArticleDGCM/examples/plot_config.py
"""
Central configuration for plot labels and styles.
Import this module in your plotting scripts to ensure consistency.
"""

# General Plotting Labels
time_label = r"Time (s)"
crack_length_label   = r"Crack Length (a) [mm]"
stiffness_label      = r"Stiffness (K) [kN/mm]"
compliance_label     = r"Compliance (C) [mm/kN]"
dCda_label           = r"dC/da [(mm/kN)]"
dadN_label           = r"da/dN [mm/cycles]"
dCda_1_label         = r"1/(dC/da) [1/((mm/kN)/mm)]"
critical_force_label = r"Critical Force ($P_c$) [kN]"
displacement_label   = r"Displacement (u) [mm]"
force_label          = r"Force (P) [kN]"
critical_force_label = r"Critical Force ($P_c$) [kN]"
strain_energy_label  = r"Strain Energy [kN mm]"
cycles_label         = r"Fatigue Cycles (N)"
DeltaK_label         = r"Stress Intensity Factor Range ($\Delta K$)"
# gamma_label          = r"Gamma [$mm^2$]"
iterations_label     = r"Iterations [-]"
G_effective_label    = r"Effective Fracture Energy ($G_{eff}$) [kN/mm]"
lambda_label         = r"$\lambda$ [kN/mm]"

gamma_ref_label      = r"Gamma"
gamma_bourdin_label  = r"Gamma Bourdin"
gamma_geometry_label  = r"Gamma Geometry"
gamma_gradient_label  = r"Gamma Gradient"

correction_factor  = r"$\mathcal{F}$"
correction_factor_reference = r"Reference"
correction_factor_DGCM  = r"DGCM"
correction_factor_bourdin  = r"Bourdin"
correction_factor_skeleton  = r"Skeleton"

gamma_label_div_theory          = r"$\Gamma/\Gamma_{\text{theory}}$ [$mm^2$]"

# Color definitions (scientific publication style)
color_orangered = '#D55E00'   # Scientific orange-red
color_blue = '#0173B2'        # Scientific blue
color_gold = '#DE8F05'        # Scientific gold
color_green = '#029E73'       # Scientific green
color_purple = '#CC78BC'      # Scientific purple
color_brown = '#CA9161'       # Scientific brown
color_pink = '#FBAFE4'        # Scientific pink
color_grey = '#949494'        # Scientific grey
color_yellow = '#ECE133'      # Scientific yellow
color_lightblue = '#56B4E9'   # Scientific light blue
color_black = '#000000'       # Scientific black
color_red = '#FF0000'         # Bright red

# Example usage for plotting:
# colors = [color_blue, color_orangered, color_gold, color_green, color_purple, color_brown, color_pink, color_grey, color_yellow, color_lightblue]
# ax.plot(x, y, color=colors[i], label=labels[i])

# General Plotting Labels
length_1d_label      = r"$x$"
length_div_a_1d_label  = r"$x/a$"
phi_profile_1d       = r"$\phi(x)$"
gradphi_profile_1d   = r"$\phi'(x)$"
phi_energy_1d        = r"$\Gamma_{\phi}$"
gradphi_energy_1d    = r"$\Gamma_{\nabla \phi}$"
energy_1d            = r"$\Gamma$"
length_a_div_l       = r"$a/l$"
length_l_div_a       = r"$l/a$"
length_l_div_h       = r"$l/h$"


phi_label   = r"$\phi$"
alpha_label = r"$\alpha(\phi)$"
x_label     = r"$x$"
y_label     = r"$y$"

length_l_label       = r"$l [mm]$"
crack_length_label   = r"Crack Length (a) [mm]"
stiffness_label      = r"Stiffness (K) [kN/mm]"
compliance_label     = r"Compliance (C) [mm/kN]"
critical_force_label = r"Critical Force ($P_c$) [kN]"
displacement_label   = r"Displacement (u) [mm]"
force_label          = r"Force (P) [kN]"
strain_energy_label  = r"Strain Energy [kN mm]"
gamma_label          = r"$\Gamma$ [$mm^2$]"
gamma_phi_label      = r"$\Gamma_{\phi}$"
gamma_gradphi_label  = r"$\Gamma_{\nabla \phi}$"
iterations_label     = r"Iterations [-]"

gamma_gamma_theory_label = r"$\Gamma/\Gamma_{\mathrm{theory}}$"
force_force_theory_label = r"$P/P_{\mathrm{theory}}$"

gamma_ref_label      = r"Gamma"
gamma_bourdin_label  = r"Gamma Bourdin"
gamma_geometry_label  = r"Gamma Geometry"