## FOR TASK fMRI -=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

## In this script, we use ntwx_iso_data.test(20) then ntwx_iso_data.test_realtime(720,0.04,0.04,60) ...

# Importage
import warnings
warnings.filterwarnings('ignore')

# os stuff
import os
import sys

import nibabel as nib
from nilearn.plotting import plot_surf, plot_surf_stat_map, plot_roi, plot_anat, plot_surf_roi
from nilearn.image import index_img

import seaborn as sns
import time
# whobpyt stuff
import whobpyt
from whobpyt.data.dataload import dataloader
from whobpyt.models.wong_wang import RNNRWW
from whobpyt.datatypes.modelparameters import ParamsModel
from whobpyt.optimization.modelfitting import Model_fitting

# array and pd stuff
import numpy as np
import pandas as pd
import pickle
# viz stuff
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------------------------------------------

# Setup stuff ...

start_time = time.time()

sub_id = int(sys.argv[1])

# task_choice = sys.argv[2]
# task_choice = str(task_choice)

ntwx_name = sys.argv[2]

a = int(sys.argv[3])
b = int(sys.argv[4])
c = int(sys.argv[5])
d = int(sys.argv[6])

# task_choice = sys.argv[7]
# task_choice = str(task_choice)

task_choice = 'REST'
# task_choice = 'MOTOR'
# task_choice = 'WM'
# task_choice = 'LANGUAGE'

# select your task ... or do it as user input.

print("Stuff setup ...")

# ----------------------------------------------------------------------------------------------------------------
# The remainder of this script is for task simulations.
# Please see the commented section below and/or the 'WhoBPyT_HCP_subs_rest_and_task_sims.py' script for the correct resting-state paths and REPLACE THE PATHS accordingly!

# FOR TASK DATA!


data_path = '/external/rprshnas01/netdata_kcni/jglab/MemberSpaces/Data/Shrey/WhoBPyT/200_subjects_WhoBPyT_task_run_pkls_real_time'

pconn_path = '/external/rprshnas01/netdata_kcni/jglab/MemberSpaces/Data/Shrey/Shrey_SS_parcellated_Func_Conns_IV/'


pconn1LR = pconn_path + '{0}_tfMRI_{1}_RL_200Schaefer_7Ntwx_cifti_parcellated.ptseries.nii'.format(sub_id, task_choice)
pconn_img1LR = nib.load(pconn1LR)
pconn_dat1LR = pconn_img1LR.get_data()
pconn_dat1LR = pconn_dat1LR/1
node_size = 200
mask = np.tril_indices(node_size, -1)
_var = np.corrcoef(pconn_dat1LR.T)

filename = data_path + '/Subj_{0}_fittingresults_{1}_stim_exp.pkl'.format(sub_id, task_choice)
with open(filename, 'rb') as f:
    ss_og_data = pickle.load(f)

filename1 = data_path + '/Subj_{0}_fittingresults_{1}_stim_exp.pkl'.format(sub_id, task_choice)
with open(filename1, 'rb') as f1:
    ntwx_iso_data = pickle.load(f1)

_test_var = np.corrcoef(np.corrcoef(ss_og_data.output_sim.bold_test)[mask],_var[mask])[0][1]
print('Correlation b/w empirical and original whobpyt simulation = ', _test_var)

original_sc = ss_og_data.model.sc.copy()

print('Data loaded')

# ---------------------------------------------------------------------------------------------------------------

# # FOR REST DATA!

# data_path = '/external/rprshnas01/netdata_kcni/jglab/MemberSpaces/Data/Shrey/WhoBPyT/200_subjects_WhoBPyT_run_pkls_real_time'
# pconn_path = '/external/rprshnas01/netdata_kcni/jglab/MemberSpaces/Data/Shrey/Shrey_SS_parcellated_Func_Conns_II/'


# pconn1LR = pconn_path + '{0}_rfMRI_REST1_RL_Schaefer200_cifti_parcellated.ptseries.nii'.format(sub_id)
# pconn_img1LR = nib.load(pconn1LR)
# pconn_dat1LR = pconn_img1LR.get_data()
# pconn_dat1LR = pconn_dat1LR/1
# node_size = 200
# mask = np.tril_indices(node_size, -1)
# _var = np.corrcoef(pconn_dat1LR.T)

# # filename = data_path + '/Subj_{0}_fittingresults_stim_exp_real_time.pkl'.format(sub_id)
# filename = data_path + '/Subj_{0}_fittingresults_stim_exp_fake_time.pkl'.format(sub_id)
# with open(filename, 'rb') as f:
#     ss_og_data = pickle.load(f)

# # filename1 = data_path + '/Subj_{0}_fittingresults_stim_exp_real_time.pkl'.format(sub_id)
# filename1 = data_path + '/Subj_{0}_fittingresults_stim_exp_fake_time.pkl'.format(sub_id)
# with open(filename1, 'rb') as f1:
#     ntwx_iso_data = pickle.load(f1)

# _test_var = np.corrcoef(np.corrcoef(ss_og_data.output_sim.bold_test)[mask],_var[mask])[0][1]
# print('Correlation b/w empirical and original whobpyt simulation = ', _test_var)

# original_sc = ss_og_data.model.sc.copy()

# print('Data loaded')

# ----------------------------------------------------------------------------------------------------------------

# Structurally isolate a functional network ...

# Create a new matrix with the same shape as the original matrix

def structurally_isolate_func_ntwx(a,b,c,d):
    
    modified_matrix = original_sc.copy()

    modified_matrix[a:b,0:a] = 0
    modified_matrix[a:b,b:c] = 0
    modified_matrix[a:b,d:200] = 0
    modified_matrix[c:d,0:a] = 0
    modified_matrix[c:d,b:c] = 0
    modified_matrix[c:d,d:200] = 0

    modified_matrix[0:a,a:b] = 0
    modified_matrix[b:c,a:b] = 0
    modified_matrix[d:200,a:b] = 0
    modified_matrix[0:a,c:d] = 0
    modified_matrix[b:c,c:d] = 0
    modified_matrix[d:200,c:d] = 0
    
    modified_matrix = modified_matrix/np.linalg.norm(modified_matrix)
    
    return modified_matrix


isolated_ntwx = structurally_isolate_func_ntwx(a,b,c,d)

print('Target Network isolated!')
      
# ----------------------------------------------------------------------------------------------------------------

ntwx_isolated_sc = isolated_ntwx.copy()
      
ntwx_iso_data.model.sc = ntwx_isolated_sc.copy()

ntwx_iso_data.test(20)
ntwx_iso_data.test_realtime(720,0.04,0.04,60)

# As per conversation with Zheng, doing F.test(20), and then F.test_realtime(), potentially yields better sims for the real-time timeseries but for lesioned SC. NOT original whobpyt sims for rest/task fMRI. 

ntwx_iso_fc_con_mat = np.corrcoef(ntwx_iso_data.output_sim.bold_test)

# ----------------------------------------------------------------------------------------------------------------

# TASK fMRI outputs

output_path = '/external/rprshnas01/netdata_kcni/jglab/MemberSpaces/Data/Shrey/WhoBPyT/Ntwx_Lesion_TASK_WhoBPyT_real_time_pkls_and_conn_mats'

np.savetxt(output_path + '/Subj_{0}_{1}_lesion_{2}_fc_con_mat.txt'.format(sub_id, ntwx_name, task_choice), ntwx_iso_fc_con_mat) 
# The above save file is for task and rest. You can change the name of the output save file to reflect this. My naming conventions are trash. please excuse my insolence!

lesion_g = ntwx_iso_data.output_sim.g
lesion_g_EE = ntwx_iso_data.output_sim.g_EE
lesion_g_EI = ntwx_iso_data.output_sim.g_EI
lesion_g_IE = ntwx_iso_data.output_sim.g_IE

lesion_fitted_sc = ntwx_iso_data.model.sc_fitted

my_dict = {'lesion_g': lesion_g, 'lesion_g_EE': lesion_g_EE, 'lesion_g_EI': lesion_g_EI, 'lesion_g_IE': lesion_g_IE, 'lesion_fitted_sc': lesion_fitted_sc}

with open(output_path + '/Subj_{0}_{1}_lesion_{2}_task_fc_con_mat.pkl'.format(sub_id, ntwx_name, task_choice), 'wb') as f:
    pickle.dump(my_dict, f)

# ----------------------------------------------------------------------------------------------------------------

# # REST fMRI outputs

# output_path = '/external/rprshnas01/netdata_kcni/jglab/MemberSpaces/Data/Shrey/WhoBPyT/200_subjects_WhoBPyT_run_pkls_real_time'

# np.savetxt(output_path + '/Subj_{0}_{1}_lesion_rest_fc_con_mat.txt'.format(sub_id, ntwx_name), ntwx_iso_fc_con_mat)

# lesion_g = ntwx_iso_data.output_sim.g
# lesion_g_EE = ntwx_iso_data.output_sim.g_EE
# lesion_g_EI = ntwx_iso_data.output_sim.g_EI
# lesion_g_IE = ntwx_iso_data.output_sim.g_IE

# lesion_fitted_sc = ntwx_iso_data.model.sc_fitted

# my_dict = {'lesion_g': lesion_g, 'lesion_g_EE': lesion_g_EE, 'lesion_g_EI': lesion_g_EI, 'lesion_g_IE': lesion_g_IE, 'lesion_fitted_sc': lesion_fitted_sc}

# with open(output_path + '/Subj_{0}_{1}_lesion_rest_fc_con_mat.pkl'.format(sub_id, ntwx_name), 'wb') as f:
#     pickle.dump(my_dict, f)


# ---------------------------------------------------------------------------------------------------------------- 

print("Time taken to complete : --- %s seconds ---" % (time.time() - start_time))


############################################################################################################################################################################################## 
