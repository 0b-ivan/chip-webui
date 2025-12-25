#!/bin/sh
set -eu

    # SSE Header
    echo "Content-Type: text/event-stream; charset=utf-8"
echo "Cache-Control: no-cache"
echo "Connection: keep-alive"
echo ""

IFACE="usb0"

# Optional: Filter (Beispiel: kein SSH)
FILTER="not port 22"

# 60s streamen, dann Ende (Browser kann neu verbinden)
# -l  line buffered
# -n  kein DNS
# -ttt relative timestamps (oder -tttt für volle Zeit)
# -s 96 nur Header/Anfang (keine vollen Payloads)
timeout 60 /usr/sbin/tcpdump -l -i "$IFACE" -n -tttt -s 96 $FILTER 2>/dev/null | \
    while IFS= read -r line; do
    # SSE "data:" pro Zeile
    printf 'data: %s\n\n' "$(printf '%s' "$line" | tr '\r' ' ')"
done

    # Ende markieren
    echo "event: end"
echo "data: done"
echo ""