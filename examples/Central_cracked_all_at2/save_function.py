r"""
.. _ref_function:

Simulation
----------
The following code is used to save the results of the simulation in a format that can be easily read by other programs. The results are saved in a tab-separated format with a header that describes the columns.

"""

import numpy as np
import os


def save_central_crack(S, h, Data, a0=0.5):

    header = ["Ofactor", "displacement", "force", "gamma","gamma_phi", "gamma_gradphi", "compliance", "stiffness", "dCda"]

    ###############################################################################
    # Plot: Displacement vs Fracture Energy
    # -------------------------------------
    force_quarter        = abs(S.reaction_files['bottom.reaction']["Ry"])
    displacement_quarter = abs(2*S.energy_files['total.energy']["E"]/(S.reaction_files['bottom.reaction']["Ry"]))
    stiffness_quarter    = abs(S.reaction_files['bottom.reaction']["Ry"]/displacement_quarter)
    compliance_quarter   = 1/stiffness_quarter
    dCda_quarter         = 2*Data.Gc/S.reaction_files['bottom.reaction']["Ry"]**2
    gamma_quarter        = a0/2 + S.energy_files['total.energy']["gamma"]
    lambda_quarter       = S.dof_files["lambda.dof"]["lambda"]
    one_factor = np.full_like(displacement_quarter, 1.0)

    ###############################################################################
    # Complete model without corrections
    # ----------------------------------
    displacement_complete  = 2*displacement_quarter
    force_complete         = 2*force_quarter
    compliance_complete    = compliance_quarter
    stiffness_complete     = stiffness_quarter
    dCda_complete          = dCda_quarter/2.0
    gamma_complete         = a0 + 2.0 * S.energy_files['total.energy']["gamma"]
    gamma_phi_complete     = a0/2 + 2.0 * S.energy_files['total.energy']["gamma_phi"]
    gamma_gradphi_complete = a0/2 + 2.0 * S.energy_files['total.energy']["gamma_gradphi"]


    data_save_reference = np.column_stack((one_factor, 
                                 displacement_complete, 
                                 force_complete, 
                                 gamma_complete,
                                 gamma_phi_complete,
                                 gamma_gradphi_complete,
                                 compliance_complete, 
                                 stiffness_complete, 
                                 dCda_complete))
    save_path_reference = os.path.join(Data.results_folder_name, "results.pff")
    np.savetxt(save_path_reference, data_save_reference, fmt="%.6e", delimiter="\t", header="\t".join(header), comments="")


    ###############################################################################
    # Complete model with Gc corrections
    # ----------------------------------
    gc_factor = np.full_like(displacement_quarter, 1 + 2*h/(2*Data.l))
    displacement_complete_corrected_gc  = displacement_complete/np.sqrt(gc_factor)
    force_complete_corrected_gc         = force_complete/np.sqrt(gc_factor)
    compliance_complete_corrected_gc    = compliance_complete
    stiffness_complete_corrected_gc     = stiffness_complete
    dCda_complete_corrected_gc          = dCda_complete*gc_factor
    gamma_complete_corrected_gc         = a0 + 2.0 * S.energy_files['total.energy']["gamma"]/gc_factor
    gamma_phi_complete_corrected_gc     = a0/2 + 2.0 * S.energy_files['total.energy']["gamma_phi"]/gc_factor
    gamma_gradphi_complete_corrected_gc = a0/2 + 2.0 * S.energy_files['total.energy']["gamma_gradphi"]/gc_factor


    data_save_gc = np.column_stack((gc_factor, 
                                 displacement_complete_corrected_gc, 
                                 force_complete_corrected_gc, 
                                 gamma_complete_corrected_gc,
                                 gamma_phi_complete_corrected_gc,
                                 gamma_gradphi_complete_corrected_gc, 
                                 compliance_complete_corrected_gc,
                                 stiffness_complete_corrected_gc, 
                                 dCda_complete_corrected_gc))
    save_path_gc = os.path.join(Data.results_folder_name, "results_corrected_bourdin.pff")
    np.savetxt(save_path_gc, data_save_gc, fmt="%.6e", delimiter="\t", header="\t".join(header), comments="")

    ###############################################################################
    # Complete model with Gradient correction 
    # ---------------------------------------
    int_phi2 = S.energy_files['total.energy']["gamma_phi"]/(1/(2*Data.l))
    int_gradphi2 = S.energy_files['total.energy']["gamma_gradphi"]/(Data.l/2)

    gradient_factor = 0.5 * (1.0 + 1/Data.l**2 *int_phi2/int_gradphi2)
    # gradient_factor = 0.5*0.5*S.energy_files['total.energy']["gamma"]/S.energy_files['total.energy']["gamma_gradphi"]
    displacement_complete_corrected_gradient  = displacement_complete/np.sqrt(gradient_factor)
    force_complete_corrected_gradient         = force_complete/np.sqrt(gradient_factor)
    compliance_complete_corrected_gradient    = compliance_complete
    stiffness_complete_corrected_gradient     = stiffness_complete
    dCda_complete_corrected_gradient          = dCda_complete*gradient_factor
    gamma_complete_corrected_gradient         = a0   + 2*S.energy_files['total.energy']["gamma"]/gradient_factor
    gamma_phi_complete_corrected_gradient     = a0/2 + 2*S.energy_files['total.energy']["gamma_gradphi"]
    gamma_gradphi_complete_corrected_gradient = a0/2 + 2*S.energy_files['total.energy']["gamma_gradphi"]


    data_save_miguel = np.column_stack((gradient_factor,
                                 displacement_complete_corrected_gradient,
                                 force_complete_corrected_gradient,
                                 gamma_complete_corrected_gradient,
                                 gamma_phi_complete_corrected_gradient,
                                 gamma_gradphi_complete_corrected_gradient,
                                 compliance_complete_corrected_gradient,
                                 stiffness_complete_corrected_gradient,
                                 dCda_complete_corrected_gradient))
    
    save_path_miguel = os.path.join(Data.results_folder_name, "results_corrected_gradient.pff")
    np.savetxt(save_path_miguel, data_save_miguel, fmt="%.6e", delimiter="\t", header="\t".join(header), comments="")




import pyvista as pv
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, os.path.abspath('../../'))
plt.style.use('../../graph.mplstyle')
import plot_config as pcfg

def plot_comparison_results(data_obj):
    """
    Plots a comparison of simulation results from different correction methods.

    Args:
        data_obj: An object containing simulation data, including the results folder name.
        plot_config: An object containing plotting configuration like labels.
    """
    path = data_obj.results_folder_name

    results = pd.read_csv(os.path.join(path, "results.pff"), delimiter="\t", comment="#", header=0)
    results_bourdin = pd.read_csv(os.path.join(path, "results_corrected_bourdin.pff"), delimiter="\t", comment="#", header=0)
    results_DGCM = pd.read_csv(os.path.join(path, "results_corrected_gradient.pff"), delimiter="\t", comment="#", header=0)

    color_1 = "black"
    color_2 = "blue"
    color_3 = "red"

    label_reference = "Reference"
    label_bourdin = "Bourdin"
    label_DGCM = "DGCM"

    ###############################################################################
    # Plot: Crack Length vs Ofactor
    # -----------------------------
    fig, ax = plt.subplots()

    ax.plot(results["gamma"], results["Ofactor"], color=color_1, linestyle='-', label=label_reference)
    ax.plot(results_bourdin["gamma"], results_bourdin["Ofactor"], color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(results_DGCM["gamma"], results_DGCM["Ofactor"], color=color_3, linestyle=':', label=label_DGCM)

    ax.set_xlabel(pcfg.gamma_label)
    ax.set_ylabel(pcfg.correction_factor)
    ax.legend()

    ###############################################################################
    # Plot: Displacement vs Force
    # ---------------------------
    fig, ax = plt.subplots()

    ax.plot(results["displacement"], results["force"], color=color_1, linestyle='-', label=label_reference)
    ax.plot(results_bourdin["displacement"], results_bourdin["force"], color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(results_DGCM["displacement"], results_DGCM["force"], color=color_3, linestyle=':', label=label_DGCM)

    ax.set_xlabel(pcfg.displacement_label)
    ax.set_ylabel(pcfg.force_label)
    ax.legend()

    ###############################################################################
    # Plot: Gamma vs Stiffness
    # ------------------------
    fig, ax = plt.subplots()

    ax.plot(results["gamma"], results["stiffness"], color=color_1, linestyle='-', label=label_reference)
    ax.plot(results_bourdin["gamma"], results_bourdin["stiffness"], color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(results_DGCM["gamma"], results_DGCM["stiffness"], color=color_3, linestyle=':', label=label_DGCM)

    ax.set_xlabel(pcfg.gamma_label)
    ax.set_ylabel(pcfg.stiffness_label)
    ax.legend()

    ###############################################################################
    # Plot: Displacement vs Stiffness
    # ---------------------------
    fig, ax = plt.subplots()

    ax.plot(results["displacement"], results["stiffness"], color=color_1, linestyle='-', label=label_reference)
    ax.plot(results_bourdin["displacement"], results_bourdin["stiffness"], color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(results_DGCM["displacement"], results_DGCM["stiffness"], color=color_3, linestyle=':', label=label_DGCM)

    ax.set_xlabel(pcfg.displacement_label)
    ax.set_ylabel(pcfg.stiffness_label)
    ax.legend()

    ###############################################################################
    # Plot: Displacement vs Gamma
    # ---------------------------
    fig, ax = plt.subplots()

    ax.plot(results["displacement"], results["gamma"], color=color_1, linestyle='-', label=label_reference)
    ax.plot(results_bourdin["displacement"], results_bourdin["gamma"], color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(results_DGCM["displacement"], results_DGCM["gamma"], color=color_3, linestyle=':', label=label_DGCM)

    ax.set_xlabel(pcfg.displacement_label)
    ax.set_ylabel(pcfg.gamma_label)
    ax.legend()

    ###############################################################################
    # Plot: Displacement vs Force
    # ---------------------------
    fig, ax = plt.subplots()

    ax.plot(results["force"], color=color_1, linestyle='-', label=label_reference)
    ax.plot(results_bourdin["force"], color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(results_DGCM["force"], color=color_3, linestyle=':', label=label_DGCM)

    ax.set_xlabel("step")
    ax.set_ylabel(pcfg.force_label)
    ax.legend()


    ###############################################################################
    # Plot: Crack Length
    # -----------------------------
    fig, ax = plt.subplots()

    ax.plot(results["gamma"], color=color_1, linestyle='-', label=label_reference)
    ax.plot(results_bourdin["gamma_phi"], color=color_2, linestyle='--', label=label_bourdin)
    ax.plot(results_DGCM["gamma_gradphi"], color=color_3, linestyle=':', label=label_DGCM)

    ax.set_ylabel(pcfg.gamma_label)
    ax.set_xlabel("step")
    ax.legend()

    plt.show()
