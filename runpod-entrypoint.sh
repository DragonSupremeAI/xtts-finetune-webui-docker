#!/bin/bash
set -euo pipefail

APP_USER=${APP_USER:-app}
SERVER_DIR=/app/server
APP_LAUNCH_SCRIPT=${APP_LAUNCH_SCRIPT:-start-container.sh}
ROOT_SSH_DIR=/root/.ssh
AUTHORIZED_KEYS_FILE=$ROOT_SSH_DIR/authorized_keys

configure_authorized_keys() {
    local key_source="${SSH_PUBLIC_KEY:-${PUBLIC_KEY:-}}"

    if [ -z "${key_source}" ]; then
        echo "No SSH public key detected in SSH_PUBLIC_KEY or PUBLIC_KEY; skipping authorized_keys update."
        return
    fi

    mkdir -p "${ROOT_SSH_DIR}"
    chmod 700 "${ROOT_SSH_DIR}"
    touch "${AUTHORIZED_KEYS_FILE}"

    if ! grep -Fxq "${key_source}" "${AUTHORIZED_KEYS_FILE}"; then
        echo "${key_source}" >> "${AUTHORIZED_KEYS_FILE}"
        echo "Added provided SSH key to /root/.ssh/authorized_keys."
    else
        echo "Provided SSH key already present in /root/.ssh/authorized_keys."
    fi

    chmod 600 "${AUTHORIZED_KEYS_FILE}"
}

start_ssh_service() {
    echo "Starting SSH service for RunPod connections..."
    service ssh start
}

run_application() {
    local target_cmd

    if [ "$#" -gt 0 ]; then
        target_cmd="$*"
    else
        target_cmd="cd ${SERVER_DIR} && bash ${APP_LAUNCH_SCRIPT}"
    fi

    exec su - "${APP_USER}" -c "${target_cmd}"
}

configure_authorized_keys
start_ssh_service
run_application "$@"
