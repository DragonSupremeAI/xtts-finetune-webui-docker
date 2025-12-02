# syntax=docker/dockerfile:1
FROM python:3.11-slim-bookworm AS base

ARG APP_NAME=xtts-finetune-webui
ARG CUDA_VER=cu121
ARG GID=966
ARG UID=966
ARG WHISPER_MODEL="large-v3"

# Environment
ENV APP_NAME=$APP_NAME \
    APP_HOME=/app/$APP_NAME \
    CUDA_VER=$CUDA_VER \
    WHISPER_MODEL=$WHISPER_MODEL \
    HF_HOME=/app/cache/huggingface \
    HUGGINGFACE_HUB_CACHE=/app/cache/huggingface/hub \
    TRANSFORMERS_CACHE=/app/cache/huggingface \
    TORCH_HOME=/app/cache/torch

# Install system dependencies required on RunPod images
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libegl1 \
        libopengl0 \
        libxcb-cursor0 \
        openssh-server && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/run/sshd

# User configuration
RUN groupadd -r app -g $GID && \
    useradd --no-log-init -m -r -g app -d $APP_HOME -s /bin/bash app -u $UID

# Prepare file-system
RUN mkdir -p /app/server $APP_HOME $HF_HOME $HUGGINGFACE_HUB_CACHE $TORCH_HOME $APP_HOME/.cache/huggingface/hub && \
    chown -R $UID:$GID /app
COPY --chown=$UID:$GID *.py *.sh *.txt *.md /app/server/
ADD --chown=$UID:$GID utils /app/server/utils

# Enter environment and install dependencies
WORKDIR /app/server

# Install Python dependencies globally so they are available to the runtime user
RUN pip3 install --no-cache-dir nvidia-pyindex && \
    pip3 install --no-cache-dir nvidia-cudnn && \
    pip3 install --no-cache-dir torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 \
        --index-url https://download.pytorch.org/whl/cu121 && \
    pip3 install --no-cache-dir -r requirements.txt

ENV NVIDIA_VISIBLE_DEVICES=all

# Pre-download the Whisper model weights as the non-root user so they live in $HOME
USER $UID:$GID
RUN python3 -c "import os; from faster_whisper import WhisperModel; WhisperModel(os.environ['WHISPER_MODEL'], device='cpu', compute_type='int8')"
USER root

# Ports and servername
EXPOSE 22 5003
ENV GRADIO_ANALYTICS_ENABLED="False" \
    GRADIO_SERVER_NAME="0.0.0.0" \
    GRADIO_SERVER_PORT="5003"

CMD [ "bash", "runpod-entrypoint.sh"]
