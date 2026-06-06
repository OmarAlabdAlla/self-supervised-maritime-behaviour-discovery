#!/bin/bash
#SBATCH --partition=long
#SBATCH --gres=gpu:L4:1
#SBATCH --output=logs/ais_dataset_%j.out
#SBATCH --error=logs/ais_dataset_%j.err
#SBATCH --cpus-per-task=64

cd "$(dirname "$0")"

# Activate your environment if needed
# conda activate <your_environment>

python -u -m scripts.build_dataset
