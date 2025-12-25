#!/bin/sh
set -eu

echo "Content-Type: text/plain; charset=utf-8"
echo ""

QS="${QUERY_STRING:-}"
ACTION="$(printf '%s' "$QS" | sed -n 's/.*action=\([^&]*\).*/\1/p')"
ACTION="${ACTION:-status}"

CAPDIR="/var/lib/chip-sniffer/captures"
WEB_CAPDIR="/home/chip/chip-webui/web/captures"

case "$ACTION" in
  status|start|stop) ;;
  *) echo "ERROR: action must be status|start|stop"; exit 0 ;;
esac

status() {
  if sudo -n /bin/systemctl is-active chip-sniffer.service >/dev/null 2>&1; then
    echo "running=1"
  else
    echo "running=0"
  fi

  echo ""
  echo "service:"
  sudo -n /bin/systemctl --no-pager -l status chip-sniffer.service 2>/dev/null | sed -n '1,10p' || true

  echo ""
  echo "captures_dir=$CAPDIR"
  echo "web_dir=$WEB_CAPDIR"
  echo ""
  echo "files:"
  if [ -d "$CAPDIR" ]; then
    ls -1 "$CAPDIR" 2>/dev/null | tail -n 50 || true
  else
    echo "(missing: $CAPDIR)"
  fi

  echo ""
  echo "download_hint:"
  echo "http://192.168.7.1/captures/"
}

start() {
  sudo -n /bin/systemctl start chip-sniffer.service
  echo "OK: sniffer started"
}

stop() {
  sudo -n /bin/systemctl stop chip-sniffer.service
  echo "OK: sniffer stopped"
}

case "$ACTION" in
  status) status ;;
  start) start ;;
  stop)  stop ;;
esac
