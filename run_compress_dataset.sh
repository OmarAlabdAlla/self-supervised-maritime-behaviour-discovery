#!/bin/bash
#SBATCH --partition=long
#SBATCH --cpus-per-task=64

#SBATCH --output=logs/compress_dataset_%j.out
#SBATCH --error=logs/compress_dataset_%j.err

cd "$(dirname "$0")"

# Activate your environment if needed
# conda activate <your_environment>

python -u -m scripts.compress_dataset
