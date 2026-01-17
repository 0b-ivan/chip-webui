#!/bin/sh
set -eu

    echo "Content-Type: text/plain; charset=utf-8"
echo ""

QS="${QUERY_STRING:-}"
ACTION="$(printf '%s' "$QS" | sed -n 's/.*action=\([^&]*\).*/\1/p')"

urldecode() {
    printf '%b' "$(printf '%s' "$1" | sed 's/+/ /g; s/%/\\x/g')"
}
ACTION="$(urldecode "${ACTION:-}")"

read_post() {
    [ "${REQUEST_METHOD:-GET}" = "POST" ] || return 0
    [ -n "${CONTENT_LENGTH:-}" ] || return 0
    dd bs=1 count="$CONTENT_LENGTH" 2>/dev/null
}
POST="$(read_post || true)"

post_get() {
    key="$1"
    printf '%s' "$POST" | tr '&' '\n' | sed -n "s/^${key}=//p" | head -n1
}

SSID_QS="$(printf '%s' "$QS" | sed -n 's/.*ssid=\([^&]*\).*/\1/p')"
PASS_QS="$(printf '%s' "$QS" | sed -n 's/.*pass=\([^&]*\).*/\1/p')"

SSID_POST="$(post_get ssid || true)"
PASS_POST="$(post_get pass || true)"

SSID="$(urldecode "${SSID_POST:-$SSID_QS}")"
PASS="$(urldecode "${PASS_POST:-$PASS_QS}")"

case "$ACTION" in
  status|on|off|save) ;;
  *) echo "ERROR: action must be status|on|off|save"; exit 0 ;;
esac

if [ "$ACTION" = "save" ]; then
  if [ -z "${SSID:-}" ]; then
    echo "ERROR: ssid missing"
    exit 0
  fi
  sudo -n /usr/local/sbin/hotspot-webui save "$SSID" "${PASS:-}" 2>&1 || {
    echo "ERROR: sudo/hotspot-webui failed"
  }
  exit 0
fi

sudo -n /usr/local/sbin/hotspot-webui "$ACTION" 2>&1 || {
  echo "ERROR: sudo/hotspot-webui failed"
}