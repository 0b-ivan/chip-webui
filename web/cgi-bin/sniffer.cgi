#!/bin/sh
set -eu

    echo "Content-Type: text/plain; charset=utf-8"
echo ""

QS="${QUERY_STRING:-}"
ACTION="$(printf '%s' "$QS" | sed -n 's/.*action=\([^&]*\).*/\1/p')"

case "$ACTION" in
    status)
sudo -n systemctl is-active chip-sniffer.service >/dev/null 2>&1 && echo "running=1" || echo "running=0"
sudo -n systemctl --no-pager -l status chip-sniffer.service 2>/dev/null | sed -n '1,8p' || true
    echo ""
echo "files:"
ls -1 /home/chip/chip-webui/web/captures 2>/dev/null | tail -n 30 || echo "(none)"
;;

start)
sudo -n systemctl start chip-sniffer.service
    echo "OK: sniffer started"
;;

stop)
sudo -n systemctl stop chip-sniffer.service
    echo "OK: sniffer stopped"
;;

*)
echo "ERROR: action must be status|start|stop"
;;
esac