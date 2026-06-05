#!/bin/bash
#SBATCH --partition=long
#SBATCH --time=20:00:00
#SBATCH --gres=gpu:L4:1
#SBATCH --cpus-per-task=64
#SBATCH --mem=32G

cd ~/exjobb/ml-analysis/jupyter_files/repo




source /data/users/omarala/miniforge3/etc/profile.d/conda.sh
conda activate exjobb_env

python3 -u train_multilayer_model.py -c configs/double_layer_config.toml