#!/bin/bash
#SBATCH --partition=long
#SBATCH --gres=gpu:L4:1
#SBATCH --cpus-per-task=64


cd ~/exjobb/ml-analysis/jupyter_files/repo

source /data/users/omarala/miniforge3/etc/profile.d/conda.sh
conda activate exjobb_env

python3 -u run_multilayer_inference.py -d DP_50_Compressed_allaData_3ports_to_use_in_github.hdf5 -n trained_model_20260605_0057.pt