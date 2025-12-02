#!/bin/bash

# XTTS Finetune WebUI Startup Script
# This script sets up the environment and launches the application

echo "Starting XTTS Finetune WebUI..."

# Set CUDA and cuDNN library paths to fix dynamic loading issues
export LD_LIBRARY_PATH="/usr/local/lib/python3.10/dist-packages/nvidia/cudnn/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cublas/lib:/usr/local/lib/python3.10/dist-packages/ctranslate2.libs:$LD_LIBRARY_PATH"

# Additional CUDA environment variables if needed
export CUDA_HOME="/usr/local/cuda"
export PATH="$CUDA_HOME/bin:$PATH"

echo "Environment variables set:"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"

# Create a Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if required packages are installed
echo "Checking dependencies..."
python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')" 2>/dev/null || {
    echo "Installing dependencies..."
    pip install -r requirements.txt 2>/dev/null || echo "No requirements.txt found, proceeding anyway..."
}

echo "Launching XTTS Demo..."
python xtts_demo.py