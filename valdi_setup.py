#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo "Starting XTTS Finetune WebUI..."
# This script sets up the environment and delegates to a Python wrapper for venv handling

# Set CUDA and cuDNN library paths to fix dynamic loading issues
export LD_LIBRARY_PATH="/usr/local/lib/python3.10/dist-packages/nvidia/cudnn/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cublas/lib:/usr/local/lib/python3.10/dist-packages/ctranslate2.libs:${LD_LIBRARY_PATH:-}"

# Additional CUDA environment variables if needed
export CUDA_HOME="/usr/local/cuda"
export PATH="$CUDA_HOME/bin:$PATH"

echo "Environment variables set:"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"

# Dry-run and minimal-deps control
DRY_RUN=${DRY_RUN:-0}
MINIMAL_DEPS=${MINIMAL_DEPS:-0}

# Ensure wrapper exists
WRAPPER="launcher/venv_launcher.py"
if [ ! -f "$WRAPPER" ]; then
  echo "ERROR: venv launcher not found: $WRAPPER" >&2
  exit 1
fi

# Build args for wrapper
WRAPPER_ARGS=()
if [ "${DRY_RUN:-0}" = "1" ]; then
  WRAPPER_ARGS+=(--dry-run)
fi
if [ "${MINIMAL_DEPS:-0}" = "1" ]; then
  WRAPPER_ARGS+=(--minimal)
fi

# Run the wrapper
python3 "$WRAPPER" "${WRAPPER_ARGS[@]}"r
