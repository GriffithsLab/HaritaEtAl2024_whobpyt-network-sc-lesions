# Welcome to the Code folder!  

Here you can find all the relevant code used to analyze the data and arrive at the results (+ produce the figures) reported in the manuscript.  

1) The `connectome_workbench_revisited.sh` script takes the HCP resting-state `*_dtseries.nii` data and converts it into parcellated (Schaefer Atlas, 200 brain regions, see *Methods*) `*_pconn.nii`.
   
2) The `WhoBPyT_HCP_subs_rest_and_task_sims.py` script can simulate resting-state and task-based fMRI time-series. This script uses the `ptseries.nii` and `pconn.nii` (obtained from (1)) as the empirical FC.

3) The `WhoBPyT_Ntwx_isolation.py` script contains code that creates virtual SC lesions and isolates the given functional network.

4) The `WhoBPyT_Code` folder contains the relevant functions used in (2) and (3) to carry out the simulations.
   
5) The `Ntwx_interactions_after_SC_lesions_resting_state.ipynb` jupyter notebook shows how to get the results obtained in the study. Figures 4, 5, 6, and 7 (panels A and B) can be obtained from this notebook. However, please note that this notebook uses resting-state data only (Figure 4). If you want to generate the figures for task data (Figures 5-7), you can use the same code in this notebook, but please CHANGE the data path to the corresponding task data.
