# LOCAL_RUN_SCRIPTS_REPORT.md — Start/Stop Shell Scripts for Local Testing

No application code was modified for this task. Two new shell scripts were added at the project root purely for developer convenience when running the FastAPI app locally.

## Files created

- `start.sh` — resolves the project root from its own location, detects `.venv`/`venv`/system Python (in that order), refuses to start a duplicate instance if `app.pid` shows a live process (and cleans up a stale one), launches `python -m uvicorn app.main:app --host 0.0.0.0 --port "$PORT"` (default port `8000`, no `--reload`) in the background, writes stdout/stderr to `app.log` and the PID to `app.pid`, waits briefly, then confirms the process is still alive. On failure it prints the last 30 lines of `app.log`, removes the stale `app.pid`, and exits non-zero.
- `stop.sh` — resolves the project root the same way, reads `app.pid`, exits cleanly if the file is missing or the recorded PID is already dead (removing the stale file), otherwise sends a normal `kill`, waits up to ~10 seconds, and escalates to `kill -9` only if the process hasn't exited. Never touches any process other than the one recorded in `app.pid` — no `pkill`/`killall`/`taskkill` used anywhere.

Both were made executable via `chmod +x start.sh stop.sh`. In Git Bash on Windows the executable bit isn't meaningful at the OS level, so they can always be run as `bash start.sh` / `bash stop.sh` regardless.

## Gitignore

- `app.log` was **already covered** by the existing `*.log` rule — no change needed.
- `app.pid` was **not previously covered** — added as a new single-line entry. No other rule in `.gitignore` was modified.

## Test result

| Test | Result |
|---|---|
| Initial start (`bash start.sh`, default port 8000) | **PASS** — `app.pid` created, process alive, `curl http://127.0.0.1:8000/` returned HTTP 200 |
| Duplicate-start prevention (`bash start.sh` while running) | **PASS** — printed "App is already running (PID ...)" and exited without spawning a second process |
| Homepage response | **PASS** — HTTP 200 on `/` for both the default-port and custom-port runs |
| Normal stop (`bash stop.sh`) | **PASS** — process terminated gracefully, "App stopped successfully." printed, `app.pid` removed |
| Repeated stop (`bash stop.sh` with no running app) | **PASS** — printed "The application does not appear to be running (no app.pid)." and exited 0 |
| Custom port test (`PORT=8090 bash start.sh`) | **PASS** — server started on port 8090, confirmed via `curl` (HTTP 200), then stopped cleanly via `bash stop.sh` |

One incidental finding during testing, unrelated to the scripts themselves: `PORT=8080` failed to bind on this specific Windows machine (`[Errno 13] ... forbidden by its access permissions`), which is a known Windows behavior where certain ports fall inside a reserved dynamic-port exclusion range (commonly caused by Hyper-V/WSL's `netsh` port reservations) — not a script defect. `start.sh` handled this exactly as specified: it detected the process had died, printed the last 30 lines of `app.log` showing the real bind error, deleted the stale `app.pid`, and exited non-zero. Port 8090 was used instead to confirm the `PORT` override mechanism itself works correctly end-to-end.

## Usage

Start (default port 8000):
```
./start.sh
```
or
```
bash start.sh
```

View logs:
```
tail -f app.log
```

Stop:
```
./stop.sh
```
or
```
bash stop.sh
```

Custom port:
```
PORT=8080 ./start.sh
```
(if a given port is unavailable on your machine, e.g. due to a Windows reserved-port range, pick another port)

## Final result

`LOCAL START/STOP SCRIPTS READY`
