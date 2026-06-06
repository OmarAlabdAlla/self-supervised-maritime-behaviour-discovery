#!/bin/bash
#SBATCH --partition=long
#SBATCH --time=20:00:00
#SBATCH --gres=gpu:L4:1
#SBATCH --cpus-per-task=64
#SBATCH --mem=32G

cd "$(dirname "$0")"

# Activate your environment if needed
# conda activate <your_environment>

python3 -u train_multilayer_model.py \
    -c configs/double_layer_config.toml
