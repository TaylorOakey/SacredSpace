#!/usr/bin/env bash
# Schedule the Business Hub rebuild in WSL2 cron (every 3 hours + at WSL start).
# Idempotent: re-running replaces the old entry. Remove with:  bash install_hub_cron.sh --remove
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
TAG="# sacredspace-business-hub"
LOG="$HOME/.sacred_hub.log"
CMD="cd \"$REPO\" && /usr/bin/python3 09_SACRED_MARKET/tools/hub_build.py >> \"$LOG\" 2>&1"

current="$(crontab -l 2>/dev/null | grep -v "$TAG" || true)"
if [ "${1:-}" = "--remove" ]; then
  printf '%s\n' "$current" | crontab -
  echo "∆ hub schedule removed"; exit 0
fi
printf '%s\n%s\n%s\n' "$current" "0 */3 * * * $CMD $TAG" "@reboot sleep 60 && $CMD $TAG" | sed '/^$/d' | crontab -
echo "∆ hub scheduled (every 3h + WSL start). Log: $LOG"

# cron only runs while WSL is up and the cron service is running.
if ! pgrep -x cron >/dev/null 2>&1; then
  echo "  · cron is not running. Start it: sudo service cron start"
  echo "    (or enable systemd in /etc/wsl.conf: [boot] systemd=true, then wsl --shutdown)"
fi
/usr/bin/python3 "$REPO/09_SACRED_MARKET/tools/hub_build.py" | tail -1
