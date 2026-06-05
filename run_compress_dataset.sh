#!/bin/bash
#SBATCH --partition=long
#SBATCH --cpus-per-task=64

#SBATCH --output=logs/compress_dataset_%j.out
#SBATCH --error=logs/compress_dataset_%j.err

source /data/users/omarala/miniforge3/etc/profile.d/conda.sh
conda activate exjobb_env

cd ~/exjobb/ml-analysis/jupyter_files/repo

python -u -m scripts.compress_dataset