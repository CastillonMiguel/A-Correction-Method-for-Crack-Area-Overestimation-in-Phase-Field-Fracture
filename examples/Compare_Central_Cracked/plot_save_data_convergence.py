r"""
.. _ref_compare_save_data:

Pre-processing: extract and save convergence metrics (AT2)
----------------------------------------------------------

This script must be run **before** the convergence plot scripts. It loads the raw post-processed
results from all 11 AT2 simulations (see :ref:`ref_examples_phase_field_central_crack`) and
extracts a set of scalar convergence metrics from each, saving them as compact tabular files
in the ``results_convergence_data/`` folder.

The control flag ``run = True`` must be set to execute the data extraction.

**Metrics extracted per simulation**

- Peak force and corresponding crack length.
- Structural stiffness at :math:`\Gamma = 0.75` mm and :math:`\Gamma = 0.90` mm.
- Correction factor :math:`\mathcal{F}` at :math:`\Gamma = 0.55`, :math:`0.75`, and :math:`0.90` mm.
- Crack length at structural stiffness thresholds of 52.44 and 38.53 kN/mm.

**Output files** (saved to ``results_convergence_data/``)

- ``convergence_data.lefm`` — scalar LEFM reference values.
- ``convergence_reference.pff`` — metrics from the uncorrected simulations.
- ``convergence_bourdin.pff`` — metrics from the Bourdin-corrected simulations.
- ``convergence_dgcm.pff`` — metrics from the DGCM-corrected simulations.

**Simulations processed** (all from :ref:`ref_examples_phase_field_central_crack`)

:ref:`ref_cc_sim1` – :ref:`ref_cc_sim11`

+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| #                   | :math:`\alpha` | :math:`\theta` | Length scale :math:`l` (mm)   | Mesh size :math:`h` (mm) | :math:`l/h` |
+=====================+================+================+===============================+==========================+=============+
| :ref:`ref_cc_sim1`  | 1.0            | 1.0            | 0.012500                      | 0.005000                 | 2.5         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim2`  | 0.2            | 0.2            | 0.002500                      | 0.001000                 | 2.5         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim3`  | 0.1            | 0.1            | 0.001250                      | 0.000500                 | 2.5         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim4`  | 0.05           | 0.05           | 0.000625                      | 0.000250                 | 2.5         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim5`  | 1.0            | 0.625          | 0.012500                      | 0.003125                 | 4.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim6`  | 0.2            | 0.125          | 0.002500                      | 0.000625                 | 4.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim7`  | 0.1            | 0.0625         | 0.001250                      | 0.0003125                | 4.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim8`  | 0.05           | 0.03125        | 0.000625                      | 0.00015625               | 4.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim9`  | 0.2            | 0.1666         | 0.002500                      | 0.000833                 | 3.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim10` | 0.2            | 0.1            | 0.002500                      | 0.000500                 | 5.0         |
+---------------------+----------------+----------------+-------------------------------+--------------------------+-------------+
| :ref:`ref_cc_sim11` | 0.2            | 0.0833         | 0.002500                      | 0.0004166                | 6.0         |
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

results_folder = "results_convergence_data"
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

run = False

if run:
    ###############################################################################
    # Load results
    # ------------
    # Once the simulation finishes, the results are loaded from the results folder.
    # The AllResults class takes the folder path as an argument and stores all
    # the results, including logs, energy, convergence, and DOF files.
    # Note that it is possible to load results from other results folders to compare results.
    # It is also possible to define a custom label and color to automate plot labels.

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
    base_results_path = "../central_cracked_all_at2"

    # NOTE: All paths start with ../central_cracked_all_at2
    # Define only the final part of each path, then prepend base_results_path to all
    path_list_final = [
        "results_cc_sim_1",
        "results_cc_sim_2",
        "results_cc_sim_3",
        "results_cc_sim_4",
        "results_cc_sim_5",
        "results_cc_sim_6",
        "results_cc_sim_7",
        "results_cc_sim_8",
        "results_cc_sim_9",
        "results_cc_sim_10",
        "results_cc_sim_11",
    ]
    path_list = [f"{base_results_path}/{final}" for final in path_list_final]

    l0 = 0.0125
    h0 = 0.0050

    simulation = np.array([1, 2, 3, 4, 
                    5, 6, 7, 8, 
                    9, 10, 11])


    alpha = np.array([1.0, 0.2, 0.1, 0.05, 
                    1.0, 0.2, 0.1, 0.05, 
                    0.2, 0.2, 0.2])

    theta = np.array([1.0, 0.2, 0.1, 0.05, 
                    0.6250, 0.125, 0.0625, 0.03125, 
                    0.1666, 0.1, 0.0833])

    l_h   = np.array([2.5, 2.5, 2.5, 2.5, 
                    4.0, 4.0, 4.0, 4.0, 
                    3.0, 5.0, 6.0])

    l     = np.array([0.012500, 0.002500, 0.001250, 0.000625,
                    0.012500, 0.002500, 0.001250, 0.000625,
                        0.002500, 0.002500, 0.002500])

    h     = np.array([0.005000, 0.001000, 0.000500, 0.000250, 
                    0.003125, 0.000625, 0.0003125, 0.00015625,
                        0.000833, 0.000500, 0.0004166])

    simulation_1 = load_simulation_data(path_list[0])
    simulation_2 = load_simulation_data(path_list[1])
    simulation_3 = load_simulation_data(path_list[2])
    simulation_4 = load_simulation_data(path_list[3])
    simulation_5 = load_simulation_data(path_list[4])
    simulation_6 = load_simulation_data(path_list[5])
    simulation_7 = load_simulation_data(path_list[6])
    simulation_8 = load_simulation_data(path_list[7])
    simulation_9 = load_simulation_data(path_list[8])
    simulation_10 = load_simulation_data(path_list[9])
    simulation_11 = load_simulation_data(path_list[10])

    simulations_reference = [simulation_1["ref"],     simulation_2["ref"],     simulation_3["ref"],     simulation_4["ref"],     simulation_5["ref"],     simulation_6["ref"],     simulation_7["ref"],     simulation_8["ref"],     simulation_9["ref"],     simulation_10["ref"],     simulation_11["ref"]]
    simulations_bourdin   = [simulation_1["bourdin"], simulation_2["bourdin"], simulation_3["bourdin"], simulation_4["bourdin"], simulation_5["bourdin"], simulation_6["bourdin"], simulation_7["bourdin"], simulation_8["bourdin"], simulation_9["bourdin"], simulation_10["bourdin"], simulation_11["bourdin"]]
    simulations_dgcm      = [simulation_1["dgcm"],    simulation_2["dgcm"],    simulation_3["dgcm"],    simulation_4["dgcm"],    simulation_5["dgcm"],    simulation_6["dgcm"],    simulation_7["dgcm"],    simulation_8["dgcm"],    simulation_9["dgcm"],    simulation_10["dgcm"],    simulation_11["dgcm"]]


    ###############################################################################
    # Save LEFM data for comparison
    # -----------------------------
    # From Linear elastic fracture mechanics theory
    results_lefm =  pd.read_csv("../Papers_Data/A_Phase_Field_Approach_to_Fatigue/results_central_cracked/a0_05.lefm_problem", delimiter="\t", comment="#", header=0)

    # Save LEFM data
    header_lefm = ["max_force", 
                "max_u", 
                "max_gamma",
                "max_stiffness",
                "gamma_at_max_force",
                "stiffness_at_gamma_075",
                "stiffness_at_gamma_09",
                "gamma_at_stiffness_52_43768",
                "gamma_at_stiffness_38_52514"]

    stiffness = results_lefm["P"]/results_lefm["u"]
    max_force_lefm = results_lefm["P"].max()
    max_u_lefm = results_lefm["u"].max()
    max_gamma_lefm = results_lefm["a"].max()
    max_stiffness_lefm = stiffness.iloc[1]
    gamma_at_maxforce_lefm = 0.5

    # Find the index where results_lefm["a"] is closest to 0.75 and 0.9, then get the corresponding stiffness value
    idx_gamma_075 = (np.abs(results_lefm["a"] - 0.75)).argmin()
    stiffness_at_gamma_075_lefm = stiffness.iloc[idx_gamma_075]

    idx_gamma_09 = (np.abs(results_lefm["a"] - 0.9)).argmin()
    stiffness_at_gamma_09_lefm = stiffness.iloc[idx_gamma_09]

    # Find the index where stiffness is closest to 52.43768 and 38.52514, then get the corresponding "a" value
    idx_52_43768 = (np.abs(stiffness - 52.43768)).argmin()
    gamma_at_stiffness_52_43768_lefm = results_lefm["a"].iloc[idx_52_43768]

    idx_38_52514 = (np.abs(stiffness - 38.52514)).argmin()
    gamma_at_stiffness_38_52514_lefm = results_lefm["a"].iloc[idx_38_52514]

    data_to_save_lefm = np.column_stack((
            max_force_lefm,
            max_u_lefm,
            max_gamma_lefm,
            max_stiffness_lefm,
            gamma_at_maxforce_lefm,
            stiffness_at_gamma_075_lefm,
            stiffness_at_gamma_09_lefm,
            gamma_at_stiffness_52_43768_lefm,
            gamma_at_stiffness_38_52514_lefm,
        ))

    output_path_lefm = os.path.join(results_folder, "convergence_data.lefm")
    np.savetxt(output_path_lefm, data_to_save_lefm, fmt="%.6e", delimiter="\t", header="\t".join(header_lefm), comments="")



    ###############################################################################
    # Save PFF data for comparison
    # ----------------------------


    def process_and_save_data(simulations, simulation_ids, file_name, results_folder):
        """
        Processes simulation data to extract key metrics and saves them to a file.

        Args:
            simulations (list): A list of pandas DataFrames, each containing simulation results.
            simulation_ids (np.array): An array of simulation identifiers.
            file_name (str): The name of the file to save the results to.
            results_folder (str): The path to the folder where the file will be saved.
        """
        header = ["simulation", 
                "alpha",
                "theta", 
                "l", 
                "h", 
                "l_h",
                "max_force",
                "max_u", 
                "max_gamma", 
                "max_stiffness", 
                "gamma_at_max_force",
                "stiffness_at_gamma_075",
                "stiffness_at_gamma_09",
                "Ofactor_at_gamma_055",
                "Ofactor_at_gamma_075",
                "Ofactor_at_gamma_09",
                "gamma_at_stiffness_52_43768",
                "gamma_at_stiffness_38_52514",]

        max_force = np.array([df["force"].max() for df in simulations])
        max_u = np.array([df["displacement"].max() for df in simulations])
        max_gamma = np.array([df["gamma"].max() for df in simulations])
        max_stiffness = np.array([df["stiffness"].max() for df in simulations])
        # For each simulation, find the index of the max force, then get the corresponding gamma value
        gamma_at_maxforce = np.array([
            df["gamma"].iloc[df["force"].idxmax()] if df is not None and not df.empty else np.nan
            for df in simulations
        ])

        # For each simulation, find the stiffness value where gamma is closest to 0.75 and 0.9
        stiffness_at_gamma_075 = np.array([
            df["stiffness"].iloc[(np.abs(df["gamma"] - 0.75)).argmin()] if df is not None and not df.empty else np.nan
            for df in simulations
        ])
        stiffness_at_gamma_09 = np.array([
            df["stiffness"].iloc[(np.abs(df["gamma"] - 0.9)).argmin()] if df is not None and not df.empty else np.nan
            for df in simulations
        ])

        # For each simulation, find the Ofactor value where gamma is closest to 0.55
        Ofactor_at_gamma_055 = np.array([
            df["Ofactor"].iloc[(np.abs(df["gamma"] - 0.55)).argmin()] if df is not None and not df.empty and "Ofactor" in df.columns else np.nan
            for df in simulations
        ])

        Ofactor_at_gamma_075 = np.array([
            df["Ofactor"].iloc[(np.abs(df["gamma"] - 0.75)).argmin()] if df is not None and not df.empty and "Ofactor" in df.columns else np.nan
            for df in simulations
        ])
        Ofactor_at_gamma_09 = np.array([
            df["Ofactor"].iloc[(np.abs(df["gamma"] - 0.9)).argmin()] if df is not None and not df.empty and "Ofactor" in df.columns else np.nan
            for df in simulations
        ])



        # For each simulation, find the gamma value where stiffness is closest to 52.43768 and 38.52514
        gamma_at_stiffness_52_43768 = np.array([
            df["gamma"].iloc[(np.abs(df["stiffness"] - 52.43768)).argmin()] if df is not None and not df.empty else np.nan
            for df in simulations
        ])
        gamma_at_stiffness_38_52514 = np.array([
            df["gamma"].iloc[(np.abs(df["stiffness"] - 38.52514)).argmin()] if df is not None and not df.empty else np.nan
            for df in simulations
        ])


        data_to_save = np.column_stack((
            simulation_ids,
            alpha,
            theta,
            l,
            h,
            l_h,
            max_force,
            max_u,
            max_gamma,
            max_stiffness,
            gamma_at_maxforce,
            stiffness_at_gamma_075,
            stiffness_at_gamma_09,
            Ofactor_at_gamma_055,
            Ofactor_at_gamma_075,
            Ofactor_at_gamma_09,
            gamma_at_stiffness_52_43768,
            gamma_at_stiffness_38_52514,
        ))
        
        output_path = os.path.join(results_folder, file_name)
        np.savetxt(output_path, data_to_save, fmt="%.6e", delimiter="\t", header="\t".join(header), comments="")
        print(f"Saved convergence data to {output_path}")

    # Process and save data for each simulation type
    process_and_save_data(simulations_reference, simulation, "convergence_reference.pff", results_folder)
    process_and_save_data(simulations_bourdin, simulation, "convergence_bourdin.pff", results_folder)
    process_and_save_data(simulations_dgcm, simulation, "convergence_dgcm.pff", results_folder)
