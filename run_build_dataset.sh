#! /bin/bash
#SBATCH --partition=long
#SBATCH --gres=gpu:L4:1
#SBATCH --output=logs/ais_dataset_%j.out
#SBATCH --error=logs/ais_dataset_%j.err
#SBATCH --cpus-per-task=64


source /data/users/omarala/miniforge3/etc/profile.d/conda.sh
conda activate exjobb_env

cd ~/exjobb/ml-analysis/jupyter_files/repo

python -u -m scripts.build_dataset
