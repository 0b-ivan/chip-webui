#!/bin/sh
set -eu

echo "Content-Type: text/plain; charset=utf-8"
echo ""

QS="${QUERY_STRING:-}"
ACTION="$(printf '%s' "$QS" | sed -n 's/.*action=\([^&]*\).*/\1/p')"

case "$ACTION" in
  status|on|off) ;;
  *) echo "ERROR: action must be status|on|off"; exit 0 ;;
esac

sudo -n /usr/local/sbin/cdc-inet "$ACTION" 2>&1 || {
  echo "ERROR: sudo/cdc-inet failed"
  exit 0
}
