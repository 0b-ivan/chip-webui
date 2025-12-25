#!/bin/sh
set -eu

echo "Content-Type: text/plain; charset=utf-8"
echo ""

# --- helpers -----------------------------------------------------

urldecode() {
  # minimal URL decode for x-www-form-urlencoded
  # "+" -> space, %XX -> byte
  printf '%s' "$1" | sed 's/+/ /g; s/%/\\x/g' | xargs -0 printf '%b' 2>/dev/null || true
}

get_qs_param() {
  # $1 = key
  echo "${QUERY_STRING:-}" | tr '&' '\n' | sed -n "s/^$1=//p" | head -n1
}

read_post_body() {
  # reads x-www-form-urlencoded body to stdout
  len="${CONTENT_LENGTH:-0}"
  [ "$len" -gt 0 ] || { echo ""; return 0; }
  dd bs=1 count="$len" 2>/dev/null
}

get_post_param() {
  # $1 = key
  body="$(read_post_body)"
  echo "$body" | tr '&' '\n' | sed -n "s/^$1=//p" | head -n1
}

wifi_status() {
  # nmcli status summary
  sudo -n /usr/bin/nmcli -t -f DEVICE,TYPE,STATE,CONNECTION device 2>/dev/null || true
  echo "---"
  sudo -n /usr/bin/nmcli -t -f GENERAL.STATE,GENERAL.CONNECTION dev show wlan0 2>/dev/null || true
}

wifi_scan() {
  # list networks (compact)
  sudo -n /usr/bin/nmcli -t -f IN-USE,SSID,SECURITY,SIGNAL device wifi list 2>/dev/null || true
}

wifi_on()  { sudo -n /usr/bin/nmcli radio wifi on  2>&1 || true; echo "OK: wifi on"; }
wifi_off() { sudo -n /usr/bin/nmcli radio wifi off 2>&1 || true; echo "OK: wifi off"; }

wifi_connect() {
  ssid_enc="$(get_post_param ssid)"
  pass_enc="$(get_post_param pass)"

  ssid="$(urldecode "${ssid_enc:-}")"
  pass="$(urldecode "${pass_enc:-}")"

  if [ -z "$ssid" ]; then
    echo "ERROR: missing ssid"
    exit 0
  fi

  # Important: do NOT echo password
  if [ -n "$pass" ]; then
    sudo -n /usr/bin/nmcli dev wifi connect "$ssid" password "$pass" 2>&1 || {
      echo "ERROR: connect failed"
      exit 0
    }
  else
    # open network attempt
    sudo -n /usr/bin/nmcli dev wifi connect "$ssid" 2>&1 || {
      echo "ERROR: connect failed (maybe needs password)"
      exit 0
    }
  fi

  echo "OK: connected to $ssid"
}

# --- router ------------------------------------------------------

action="$(get_qs_param action)"
action="$(urldecode "${action:-status}")"

case "$action" in
  status)  wifi_status ;;
  scan)    wifi_scan ;;
  on)      wifi_on ;;
  off)     wifi_off ;;
  connect) wifi_connect ;;
  *) echo "ERROR: action must be status|scan|on|off|connect" ;;
esac
