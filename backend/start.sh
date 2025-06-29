#!/bin/bash

# Start the FastAPI backend server
# Usage: ./start.sh [host] [port]
# Defaults: host=127.0.0.1, port=8000

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

HOST=${1:-127.0.0.1}
PORT=${2:-8000}

export PYTHONPATH="$SCRIPT_DIR"

echo "Starting FastAPI backend at http://$HOST:$PORT ..."
uvicorn app.main:app --host $HOST --port $PORT --reload
