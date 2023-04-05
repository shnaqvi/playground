#%%
import os
import matplotlib.pyplot as plt
import numpy as np
import re
import subprocess
import json
import pandas as pd
import seaborn as sns

data_dir = '/Volumes/flamingo_data-1/_Salman/_calibration/Jan23_loft/dataset_mar22-2'
subdirs = [name for name in os.listdir(data_dir) if name not in ['pattern', '.DS_Store', 'p.0p0p0_p0p0p0']]

def pos_from_str(v):
    return float(v[1:]) if v[0] == 'p' else float(v[1:])*-1

pos_delta = pd.DataFrame(columns=['x', 'y', 'z', 'gx', 'gy', 'gz', 'lx', 'ly', 'lz'])
for subdir in subdirs:
    str_tr = re.findall('(.*?)_', subdir)[0]
    [x, y, z] = [pos_from_str(val) for val in re.findall('[a-z]?[0-9]*\.?[0-9]', str_tr)]
    

    tf_nom = json.load(open(f'{data_dir}/p.0p0p0_p0p0p0/left-omfc.json'))
    tf_rgd = json.load(open(f'{data_dir}/{subdir}/left-omfc-rgd.json'))
    del_gcam = (np.array(tf_rgd['pose_gcam'][1]) - np.array(tf_nom['pose_gcam'][1])).tolist()
    del_lens = (np.array(tf_rgd['pose_lens'][1]) - np.array(tf_nom['pose_lens'][1])).tolist()

    pos_delta = pd.concat([pd.DataFrame([[x, y, z, *del_gcam, *del_lens]],
                                      columns=pos_delta.columns), pos_delta], ignore_index=True)
    
del_x = pos_delta[pos_delta['x']!=0]
del_z = pos_delta[pos_delta['z']!=0]

plt.rcParams["figure.autolayout"] = True
fig, ax = plt.subplots(1,2)
tt = del_x.melt(id_vars=['x'], value_vars=['gx', 'lx'])
sns.lineplot(data=tt, x='x', y='value', err_style='band', errorbar='sd', ax=ax[0]) 
ax[0].plot(del_x['x'], del_x['gx'], 'o', label='gcam'), ax[0].plot(del_x['x'], del_x['lx'], 'rx', label='lens') 
ax[0].set_xlabel('delta_panel_x (mm)')
ax[0].set_ylabel('delta_gcam-lens (mm)') 
ax[0].legend()
ax[0].axis('image'); ax[0].grid('on')

tt = del_z.melt(id_vars=['z'], value_vars=['gz', 'lz'])
sns.lineplot(data=tt, x='z', y='value', err_style='band', errorbar='sd', ax=ax[1]) 
ax[1].plot(del_z['z'], del_z['gz'], 'o'), ax[1].plot(del_z['z'], del_z['lz'], 'rx')
ax[1].set_ylabel('')
ax[1].set_xlabel('delta_panel_z (mm)')
ax[1].axis('image'); plt.grid('on')
plt.show()

# plt.savefig('/Users/salman_naqvi/Documents/Project-Display/t288_display_incubation/_data/Mar23_timefall-valid.png', dpi=300,
#             transparent=True, edgecolor=None)
# %%
