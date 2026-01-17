#!/bin/sh
echo "Content-Type: application/json"
echo ""

qs="${QUERY_STRING:-}"

get_qs() { printf "%s" "$qs" | sed -n "s/.*$1=\([^&]*\).*/\1/p"; }

ACTION="$(get_qs action)"
[ -n "$ACTION" ] || ACTION="status"

IFACE="$(get_qs iface)"
[ -n "$IFACE" ] || IFACE="wlan0"

# Allowlist action
case "$ACTION" in
  start|stop|status) ;;
  *) ACTION="status" ;;
esac

# Sanitize iface (kill ; und alles ungewollte)
IFACE="$(printf "%s" "$IFACE" | tr -cd 'A-Za-z0-9_.:-')"
[ -n "$IFACE" ] || IFACE="wlan0"

CTRL="/home/chip/chip-webui/scripts/tcpdump-control.sh"

RESULT="$(sudo -n /bin/sh "$CTRL" "$ACTION" "$IFACE" 2>&1 | tail -n 1 | sed 's/"/\\"/g')"

echo "{ \"action\": \"$ACTION\", \"iface\": \"$IFACE\", \"result\": \"$RESULT\" }"
