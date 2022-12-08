#!/usr/bin/env bash

# This script is meant to be sourced, not executed.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "This script is meant to be sourced, not executed."
    exit 1
fi

if ! command -v conda &> /dev/null
then
    echo "conda is not installed."
    return
fi

conda_env_list=$(conda env list | grep gpt3)
if [[ -z "${conda_env_list}" ]]; then
    echo "No conda environment found."
    return
fi

conda activate gpt3
