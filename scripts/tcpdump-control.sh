#!/bin/sh
set -eu

PATH=/usr/sbin:/usr/bin:/sbin:/bin
export PATH
TCPDUMP=/usr/sbin/tcpdump

ACTION="${1:-status}"
IFACE_RAW="${2:-${IFACE:-wlan0}}"

# Sanitize IFACE: nur erlaubte Zeichen (keine ;, spaces, etc.)
IFACE="$(printf "%s" "$IFACE_RAW" | tr -cd 'A-Za-z0-9_.:-')"
[ -n "$IFACE" ] || IFACE="wlan0"

OUTDIR="/home/chip/chip-webui/web/captures"
PIDFILE="/tmp/chip-webui-tcpdump-${IFACE}.pid"

mkdir -p "$OUTDIR"

is_running() {
  [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null
}

case "$ACTION" in
  start)
    if is_running; then
      echo "already running"
      exit 0
    fi

    TS="$(date +%Y%m%d-%H%M%S)"
    OUT="$OUTDIR/tcpdump-${IFACE}-${TS}.pcap"
    LOG="/tmp/chip-webui-tcpdump-${IFACE}-${TS}.log"
    LATEST="/tmp/chip-webui-tcpdump-${IFACE}.log"

    # Ringbuffer ~30MB: 6x5MB
    "$TCPDUMP" -i "$IFACE" -n -U -C 5 -W 6 -w "$OUT" >>"$LOG" 2>&1 &
    PID="$!"
    echo "$PID" > "$PIDFILE"

    # "latest log" aktualisieren (best-effort)
    ln -sf "$LOG" "$LATEST" 2>/dev/null || true

    sleep 0.2
    if ! kill -0 "$PID" 2>/dev/null; then
      echo "failed: $(tail -n 1 "$LOG" 2>/dev/null)"
      rm -f "$PIDFILE" 2>/dev/null || true
      exit 1
    fi

    echo "started: $OUT"
    ;;

  stop)
    if is_running; then
      kill "$(cat "$PIDFILE")" 2>/dev/null || true
      rm -f "$PIDFILE" 2>/dev/null || true
      echo "stopped"
    else
      rm -f "$PIDFILE" 2>/dev/null || true
      echo "not running"
    fi
    ;;

  status)
    if is_running; then
      echo "running"
    else
      echo "stopped"
    fi
    ;;

  *)
    echo "usage: $0 {start|stop|status} [iface]"
    exit 2
    ;;
esac
