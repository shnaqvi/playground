import os
import re
import subprocess

tmesh_path = '/Volumes/flamingo_data/_GCAM/GCAM_20230322/matlab_output_w_fused/target-mesh-port-rotp90.json'
data_dir = '/Volumes/flamingo_data-1/_Salman/_calibration/Jan23_loft/dataset_mar22-2'
bin_dir = '/Users/salman_naqvi/Documents/Project-Display/t288_display_incubation/platform-calibration'
subdirs = [name for name in os.listdir(data_dir) if name not in ['pattern', '.DS_Store']]

#%% Generate Rays, Fit Model, Validate
for subdir in subdirs:
    data_path = f'{data_dir}/{subdir}'
    cmd_dec  = f'{bin_dir}/bin/dgcb decode-all  {data_path}/captures --l-target={tmesh_path} --r-target={tmesh_path} -n=8 -o={data_path}/rays-cp90.rays'
    out = subprocess.run(cmd_dec, shell=True, capture_output=True, text=True)
    if out.stderr:
        if not re.search('Finished all tasks', out.stdout):
            raise Exception(out.stderr)
    print(out.stdout)

    cmd_fit = f'{bin_dir}/bin/lens-model-tools fit-model-omfc -r={data_path}/rays-cp90.rays -e=0 -c=1 -n=20 -o={data_path}/left-omfc.json'
    out = subprocess.run(cmd_fit, shell=True, capture_output=True, text=True)
    if out.stderr:
        raise Exception(out.stderr)
    print(out.stdout)

    cmd_val = f'{bin_dir}/bin/lens-model-tools validate-model-omfc -m={data_path}/left-omfc.json -e=0 -r={data_path}/rays-cp90.rays -j={data_path}/error-left-omfc.json'
    out = subprocess.run(cmd_val, shell=True, capture_output=True, text=True)
    if out.stderr:
        if not re.search('Validation complete', out.stdout):
            raise Exception(out.stderr)
    print(out.stdout)   

#%% Fit Rigid Model, Validate, Generate Rays
for subdir in subdirs:
    data_path = f'{data_dir}/{subdir}'
    cmd_frg = f'{bin_dir}/bin/lens-model-tools fit-rigid-parts-omfc -r={data_path}/rays-cp90.rays -m={data_dir}/p.0p0p0_p0p0p0/left-omfc.json -n=20 -e=0 -o={data_path}/left-omfc-rgd.json'
    out = subprocess.run(cmd_frg, shell=True, capture_output=True, text=True)
    if out.stderr:
        raise Exception(out.stderr)
    print(out.stdout)

    cmd_val = f'{bin_dir}/bin/lens-model-tools validate-model-omfc -m={data_path}/left-omfc-rgd.json -e=0 -r={data_path}/rays-cp90.rays -j={data_path}/error-left-omfc-rgd.json'
    out = subprocess.run(cmd_val, shell=True, capture_output=True, text=True)
    if out.stderr:
        if not re.search('Validation complete', out.stdout):
            raise Exception(out.stderr)
    print(out.stdout)   

    cmd_rays = f'{bin_dir}/bin/lens-model-tools generate-rays -m={data_path}/left-omfc.json -e=0 -r={data_path}/rays-cp90.rays -o={data_path}/rays-tf.rays'
    out = subprocess.run(cmd_rays, shell=True, capture_output=True, text=True)
    if out.stderr:
        if not re.search('done.', out.stdout):
            raise Exception(out.stderr)
    print(out.stdout)

    cmd_rays = f'{bin_dir}/bin/lens-model-tools generate-rays -m={data_path}/left-omfc-rgd.json -e=0 -r={data_path}/rays-cp90.rays -o={data_path}/rays-tf-rgd.rays'
    out = subprocess.run(cmd_rays, shell=True, capture_output=True, text=True)
    if out.stderr:
        if not re.search('done.', out.stdout):
            raise Exception(out.stderr)
    print(out.stdout)