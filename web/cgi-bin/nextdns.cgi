#!/bin/sh
set -eu

echo "Content-Type: text/plain; charset=utf-8"
echo ""

QS="${QUERY_STRING:-}"
ACTION="$(printf '%s' "$QS" | sed -n 's/.*action=\([^&]*\).*/\1/p')"

case "${ACTION:-status}" in
  status|on|off|logs) ;;
  *) echo "ERROR: action must be status|on|off|logs"; exit 0 ;;
esac

sudo -n /usr/local/sbin/nextdns-webui "$ACTION" 2>&1 || {
  echo "ERROR: sudo/nextdns-webui failed"
}
