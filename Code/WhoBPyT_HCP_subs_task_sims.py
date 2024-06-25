# For task fMRI.

# Here I combine all the tasks using a second user input which is one of: 'WM', 'MOTOR', or 'LANGUAGE' for the different tasks
# Dropped Tasks: 'SOCIAL', 'GAMBLING'
# ------------------------------------

# Resolution: 200 Schaefer Parcellations (possible with higher).

# Importage

import warnings
warnings.filterwarnings('ignore')

# os stuff
import os
import sys
# sys.path.append('..')

import nibabel as nib
from nilearn.plotting import plot_surf, plot_surf_stat_map, plot_roi, plot_anat, plot_surf_roi
from nilearn.image import index_img

import seaborn as sns

# whobpyt stuff
import whobpyt
from whobpyt.data.dataload import dataloader
from whobpyt.models.wong_wang import RNNRWW
from whobpyt.datatypes.modelparameters import ParamsModel
from whobpyt.optimization.modelfitting import Model_fitting

# array and pd stuff
import numpy as np
import pandas as pd

# viz stuff
import matplotlib.pyplot as plt

import pickle

import time

print("Imports done ...")

# ----------------------------------------------------------------------------------------------------------------

# Setup stuff ...

start_time = time.time()

sub_id = sys.argv[1]  
sub_id = int(sub_id)

task_choice = sys.argv[2]
task_choice = str(task_choice)

print("Stuff setup ...")

# print(sub_id)
# print(task_choice)

# ----------------------------------------------------------------------------------------------------------------

# Paths

Wts_Path = '/external/rprshnas01/netdata_kcni/jglab/MemberSpaces/Data/Shrey/Improved_WWD_HCP_model_runs/All_Subs_SC_Wts/Davide_HCP_Data_Matrix'
# replace the above with your weights path!

parcs = np.arange(0,200,1)

print("Paths set ...")

# ----------------------------------------------------------------------------------------------------------------

# define options for the wong-wang model
node_size = 200
mask = np.tril_indices(node_size, -1)
num_epoches = 60 #40 #20 #50 
# for resting-state we used 20, but fits b/w emp task and whobpyt tasks are approx. 0.3 with 20 epochs., so trying 40 and then 60; original epoch val = 50
batch_size = 60 #20 for resting-state
step_size = 0.04
input_size = 2
tr = 0.72 #2.0 # the correct TR for HCP is 720 msec not 2 seconds!
repeat_size = 5

print("Set options ...")

# ----------------------------------------------------------------------------------------------------------------

# Load SC

_df = pd.read_csv(Wts_Path + '/{0}/{0}_new_atlas_Yeo.nii.csv'.format(sub_id), delimiter=' ',header=None)
df_trimmed = _df.iloc[:-31, :-31]
np_array = df_trimmed.values
sc_mtx = np_array + np_array.T # --> Symmetric

pre_laplachian_HCP_SC = sc_mtx.copy()

HCP_SC = pre_laplachian_HCP_SC.copy()

SC = HCP_SC.copy()
sc = np.log1p(SC) / np.linalg.norm(np.log1p(SC))

print("Loaded SC ...")

# ----------------------------------------------------------------------------------------------------------------

# Load FC

pconn_path = '/external/rprshnas01/netdata_kcni/jglab/MemberSpaces/Data/Shrey/Shrey_SS_parcellated_Func_Conns_IV/'
# The above path contains parcellated empirical fMRI data. See the connectome workbench script for more information.  

if task_choice == 'MOTOR':
    pconn1LR = pconn_path + '{0}_tfMRI_MOTOR_RL_200Schaefer_7Ntwx_cifti_parcellated.ptseries.nii'.format(sub_id)
elif task_choice == 'WM':
    pconn1LR = pconn_path + '{0}_tfMRI_WM_RL_200Schaefer_7Ntwx_cifti_parcellated.ptseries.nii'.format(sub_id)
elif task_choice == 'LANGUAGE':
    pconn1LR = pconn_path + '{0}_tfMRI_LANGUAGE_RL_200Schaefer_7Ntwx_cifti_parcellated.ptseries.nii'.format(sub_id)
else:
    print('Error!! Task specified is invalid!')
    sys.exit(1)

_pconn_img1LR = nib.load(pconn1LR)
_pconn_dat1LR = _pconn_img1LR.get_data()
_pconn_dat1LR = _pconn_dat1LR/1

ts = _pconn_dat1LR.copy() # ts_pd.values
ts = ts / np.max(ts)
fc_emp = np.corrcoef(ts.T)

print("Loaded FC ...")

# ----------------------------------------------------------------------------------------------------------------

# %%
# prepare data structure of the model
data_mean = dataloader(ts, num_epoches, batch_size)

# %%
# get model parameters structure and define the fitted parameters by setting non-zero variance for the model
par = ParamsModel('RWW',  g=[400, 1/np.sqrt(10)], g_EE=[1.5, 1/np.sqrt(50)], g_EI =[0.8,1/np.sqrt(50)], \
                          g_IE=[0.6,1/np.sqrt(50)], I_0 =[0.2, 0], I_external=[0.02,0], std_in=[0.0,0], std_out=[0.00,0])

# note that I_external has been set to 0.02 in the above params as this is task sims (see Deco et al., 2014). 
# Quick observation (based on comparison with 1st 10 subjects): I_ext has *no significant* (p >> 0.05) effect on model fit to empirical task data. It is practically identical when I_ext = 0.  
# I_ext = 0 for the rest sims. 

print("Loaded other Stuff ...Running WhoBPyT... ")

# ----------------------------------------------------------------------------------------------------------------

# %%
# call model you want to fit
model = RNNRWW(node_size, batch_size, step_size, repeat_size, tr, sc, True, par)

# %%
# initial model parameters and set the fitted model parameter in Tensors
model.setModelParameters()

# %%
# call model fit
F = Model_fitting(model, data_mean, num_epoches, 2)

# %%
# model training
F.train(learningrate= 0.05)

# %%
# model test with real_time
F.test_realtime(720,0.04,0.04,60)
# F.test(20)


print("Finished running WhoBPyT ...")

# ----------------------------------------------------------------------------------------------------------------


# output_path = '/external/rprshnas01/netdata_kcni/jglab/MemberSpaces/Data/Shrey/WhoBPyT/200_subjects_WhoBPyT_task_run_pkls_real_time'

filename = output_path + '/Subj_{0}_fittingresults_{1}_task_stim_exp.pkl'.format(sub_id, task_choice)

with open(filename, 'wb') as f:
    pickle.dump(F, f)
    
print("Output saved!")

# ----------------------------------------------------------------------------------------------------------------
    
print("Time taken to complete : --- %s seconds ---" % (time.time() - start_time))
