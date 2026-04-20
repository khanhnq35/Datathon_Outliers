"""
Configuration parameters for the Datathon Outliers Project
"""
from pathlib import Path

# Base Paths (allowing execution from anywhere)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"

# Reproducibility
RANDOM_SEED = 42
