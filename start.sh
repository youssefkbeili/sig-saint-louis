#!/usr/bin/env bash
set -euo pipefail

# Resolve the project root from this script's location, regardless of cwd.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$SCRIPT_DIR"

PORT="${PORT:-8000}"
PID_FILE="app.pid"
LOG_FILE="app.log"

# --- Refuse to start a duplicate instance ---
if [ -f "$PID_FILE" ]; then
    OLD_PID="$(cat "$PID_FILE" 2>/dev/null || true)"
    if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
        echo "App is already running (PID $OLD_PID). See $LOG_FILE, or run stop.sh first."
        exit 0
    else
        echo "Stale PID file found (process not running). Removing it."
        rm -f "$PID_FILE"
    fi
fi

# --- Detect a Python interpreter ---
PYTHON=""
for candidate in ".venv/bin/python" ".venv/Scripts/python.exe" "venv/bin/python" "venv/Scripts/python.exe"; do
    if [ -x "$candidate" ]; then
        PYTHON="$candidate"
        break
    fi
done
if [ -z "$PYTHON" ] && command -v python >/dev/null 2>&1; then
    PYTHON="python"
fi
if [ -z "$PYTHON" ]; then
    echo "No usable Python interpreter found (.venv, venv, or system python)." >&2
    exit 1
fi

echo "Using interpreter: $PYTHON"
echo "Starting app on 0.0.0.0:$PORT ..."

# --- Launch uvicorn in the background, detached from this shell ---
nohup "$PYTHON" -m uvicorn app.main:app --host 0.0.0.0 --port "$PORT" >"$LOG_FILE" 2>&1 &
NEW_PID=$!
echo "$NEW_PID" >"$PID_FILE"

# --- Give it a moment to fail fast (e.g. import error, port in use) ---
sleep 1.5

if kill -0 "$NEW_PID" 2>/dev/null; then
    echo "App started successfully."
    echo "  PID:        $NEW_PID"
    echo "  URL:        http://127.0.0.1:$PORT"
    echo "  Logs:       tail -f $LOG_FILE"
    echo "  Stop with:  bash stop.sh"
else
    echo "App failed to start. Last 30 lines of $LOG_FILE:" >&2
    tail -n 30 "$LOG_FILE" >&2 2>/dev/null || true
    rm -f "$PID_FILE"
    exit 1
fi
