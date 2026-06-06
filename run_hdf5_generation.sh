#!/bin/bash
#SBATCH --partition=long
#SBATCH --cpus-per-task=64

#SBATCH --output=logs/hdf5_generation_%j.out
#SBATCH --error=logs/hdf5_generation_%j.err

cd "$(dirname "$0")"

# Activate your environment if needed
# conda activate <your_environment>

python -u -m scripts.build_hdf5
