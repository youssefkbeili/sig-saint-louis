#!/usr/bin/env bash
set -uo pipefail

# Resolve the project root from this script's location, regardless of cwd.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$SCRIPT_DIR"

PID_FILE="app.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "The application does not appear to be running (no $PID_FILE)."
    exit 0
fi

PID="$(cat "$PID_FILE" 2>/dev/null || true)"

if [ -z "$PID" ] || ! kill -0 "$PID" 2>/dev/null; then
    echo "Recorded PID is no longer running. Removing stale $PID_FILE."
    rm -f "$PID_FILE"
    exit 0
fi

echo "Stopping app (PID $PID) ..."
kill "$PID" 2>/dev/null || true

# Wait up to ~10 seconds for a graceful exit.
for _ in $(seq 1 20); do
    if ! kill -0 "$PID" 2>/dev/null; then
        rm -f "$PID_FILE"
        echo "App stopped successfully."
        exit 0
    fi
    sleep 0.5
done

echo "App did not exit in time. Forcing shutdown (kill -9)."
kill -9 "$PID" 2>/dev/null || true
rm -f "$PID_FILE"
echo "App stopped (forced)."
