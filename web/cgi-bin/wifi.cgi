#!/bin/sh
set -eu

echo "Content-Type: text/plain; charset=utf-8"
echo ""

QS="${QUERY_STRING:-}"

# action=... aus QueryString ziehen (minimal)
ACTION="$(printf '%s' "$QS" | sed -n 's/.*action=\([^&]*\).*/\1/p')"
SSID="$(printf '%s' "$QS" | sed -n 's/.*ssid=\([^&]*\).*/\1/p')"
PSK="$(printf '%s' "$QS"  | sed -n 's/.*psk=\([^&]*\).*/\1/p')"

# rudimentäres URL-decoding für %20 usw. (reicht pragmatisch)
urldecode() {
  # busybox ash: printf %b trick
  printf '%b' "$(printf '%s' "$1" | sed 's/+/ /g; s/%/\\x/g')"
}

ACTION="$(urldecode "${ACTION:-}")"
SSID="$(urldecode "${SSID:-}")"
PSK="$(urldecode "${PSK:-}")"

case "$ACTION" in
  status|scan|on|off|connect) ;;
  *) echo "ERROR: action must be status|scan|on|off|connect"; exit 0 ;;
esac

# connect benötigt ssid, psk optional (offenes wlan)
if [ "$ACTION" = "connect" ]; then
  sudo -n /usr/local/sbin/wifi-webui connect "$SSID" "$PSK" 2>&1 || { echo "ERROR: sudo/wifi-webui failed"; }
  exit 0
fi

sudo -n /usr/local/sbin/wifi-webui "$ACTION" 2>&1 || { echo "ERROR: sudo/wifi-webui failed"; }
