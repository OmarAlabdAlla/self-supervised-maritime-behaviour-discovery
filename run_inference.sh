#!/bin/bash
#SBATCH --partition=long
#SBATCH --gres=gpu:L4:1
#SBATCH --cpus-per-task=64

cd "$(dirname "$0")"

# Activate your environment if needed
# conda activate <your_environment>

python3 -u run_multilayer_inference.py \
    -d DP_50_Compressed_allaData_3ports_to_use_in_github.hdf5 \
    -n trained_model_20260605_0057.pt
