#!/bin/sh
set -eu

echo "Content-Type: application/json"
echo ""

CAPDIR="/home/chip/chip-webui/web/captures"

ACTION="$(printf "%s" "${QUERY_STRING:-}" | sed -n 's/.*action=\([^&]*\).*/\1/p')"
[ -n "${ACTION:-}" ] || ACTION="list"

LIMIT="$(printf "%s" "${QUERY_STRING:-}" | sed -n 's/.*limit=\([^&]*\).*/\1/p')"
DAYS="$(printf "%s" "${QUERY_STRING:-}" | sed -n 's/.*days=\([^&]*\).*/\1/p')"

[ -n "${LIMIT:-}" ] || LIMIT="30"
[ -n "${DAYS:-}" ] || DAYS="7"

case "$LIMIT" in ''|*[!0-9]*) LIMIT="30";; esac
case "$DAYS"  in ''|*[!0-9]*) DAYS="7";;  esac

json_escape() { printf "%s" "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'; }

case "$ACTION" in
  list)
    [ -d "$CAPDIR" ] || { echo '{ "ok": false, "error": "captures dir missing" }'; exit 0; }

    printf '{ "ok": true, "captures": ['
    first=1
    for f in $(ls -1t "$CAPDIR" 2>/dev/null | grep -E '\.pcap([0-9]+)?$|\.pcap$' | head -n "$LIMIT"); do
      path="$CAPDIR/$f"
      [ -f "$path" ] || continue
      size="$(stat -c %s "$path" 2>/dev/null || echo 0)"
      mtime="$(stat -c %Y "$path" 2>/dev/null || echo 0)"
      [ $first -eq 1 ] || printf ', '
      first=0
      printf '{ "name": "%s", "size": %s, "mtime": %s }' "$(json_escape "$f")" "$size" "$mtime"
    done
    printf '] }\n'
    ;;
  cleanup)
    [ -d "$CAPDIR" ] || { echo '{ "ok": false, "error": "captures dir missing" }'; exit 0; }

    before="$(find "$CAPDIR" -maxdepth 1 -type f \( -name '*.pcap' -o -name '*.pcap[0-9]*' \) 2>/dev/null | wc -l | tr -d ' ')"
    find "$CAPDIR" -maxdepth 1 -type f \( -name '*.pcap' -o -name '*.pcap[0-9]*' \) -mtime +"$DAYS" -delete 2>/dev/null || true
    after="$(find "$CAPDIR" -maxdepth 1 -type f \( -name '*.pcap' -o -name '*.pcap[0-9]*' \) 2>/dev/null | wc -l | tr -d ' ')"
    deleted=$((before-after)); [ "$deleted" -ge 0 ] || deleted=0
    echo "{ \"ok\": true, \"deleted\": $deleted, \"days\": $DAYS }"
    ;;
  *)
    echo '{ "ok": false, "error": "invalid action" }'
    ;;
esac
