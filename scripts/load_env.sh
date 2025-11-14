#!/usr/bin/env bash
set -a
ENV_FILE="${1:-.env}"
if [ -f "$ENV_FILE" ]; then
  . "$ENV_FILE"
fi
set +a