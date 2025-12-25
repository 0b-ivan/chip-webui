#!/bin/sh
set -eu

    # SSE Header
    echo "Content-Type: text/event-stream; charset=utf-8"
echo "Cache-Control: no-cache"
echo "Connection: keep-alive"
echo ""

IFACE="usb0"
FILTER="not port 22"

# Optional: sofort eine Zeile schicken (damit man sieht, dass es läuft)
printf 'event: status\ndata: starting sniffer on %s\n\n' "$IFACE"

# sudo wrapper benutzen (tcpdump braucht root/caps)
# Wichtig: -l (line-buffered) ist im Wrapper bereits gesetzt; falls nicht, im Wrapper ergänzen.
sudo -n /usr/local/sbin/sniffer-live "$IFACE" 2>&1 | while IFS= read -r line; do
    # Filter grob im CGI anwenden (pragmatisch). Alternativ: Filter direkt im sniffer-live wrapper.
    # Falls du Filter sauber im Wrapper willst: sniffer-live "$IFACE" "$FILTER" und dort exec tcpdump ... $FILTER
    case "$line" in
    *" IP "*)
      # sehr einfacher Filter: "not port 22"
      echo "$line" | grep -q "\.22 " && continue
      echo "$line" | grep -q "\.22:" && continue
      ;;
  esac

  printf 'data: %s\n\n' "$(printf '%s' "$line" | tr '\r' ' ')"
done

# Wenn sudo/tcpdump endet (oder Permission-Error), melden wir Ende
echo "event: end"
echo "data: done"
echo ""