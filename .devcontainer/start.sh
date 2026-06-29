#!/bin/bash
set -e

VNC_PASSWORD="${VNC_PASSWORD:-V1312}"
IDLE_TIMEOUT="${IDLE_TIMEOUT:-300}"

echo "[Desktop] Restoring state..."
python3 /opt/desktop/restore-state.py || true

echo "[Desktop] Starting Xvfb..."
Xvfb :1 -screen 0 1280x720x24 -ac +extension GLX +render -noreset &
XVFB_PID=$!
sleep 2

echo "[Desktop] Starting Openbox..."
DISPLAY=:1 openbox --config-file /dev/null &
sleep 1

echo "[Desktop] Setting VNC password..."
mkdir -p /root/.vnc
x11vnc -storepasswd "$VNC_PASSWORD" /root/.vnc/passwd

echo "[Desktop] Starting x11vnc..."
x11vnc \
    -display :1 \
    -rfbauth /root/.vnc/passwd \
    -rfbport 5900 \
    -forever \
    -noxdamage \
    -shared \
    -quiet &
sleep 1

echo "[Desktop] Starting noVNC..."
websockify --web /usr/share/novnc/ --daemon 6080 localhost:5900
sleep 1

echo "[Desktop] Starting API..."
touch /tmp/last_activity
python3 /opt/desktop/api.py &
sleep 1

echo "[Desktop] Starting idle watchdog (${IDLE_TIMEOUT}s timeout)..."
(
    while true; do
        sleep 60
        LAST=$(stat -c %Y /tmp/last_activity 2>/dev/null || echo 0)
        NOW=$(date +%s)
        IDLE=$((NOW - LAST))
        if [ "$IDLE" -gt "$IDLE_TIMEOUT" ]; then
            echo "[Watchdog] Idle ${IDLE}s — stopping codespace"
            gh codespace stop --codespace "$CODESPACE_NAME" 2>/dev/null || kill "$XVFB_PID"
        fi
    done
) &

echo "[Desktop ${DESKTOP_ID:-?}] Ready!"
echo "  noVNC → port 6080"
echo "  API   → port 8080"
echo "  Log:  tail -f /tmp/desktop.log"

wait $XVFB_PID
