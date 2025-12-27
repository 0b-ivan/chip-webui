#!/bin/sh
set -eu

# 1) NextDNS CLI installieren (offizieller Installer)
# Hinweis: nutzt curl; stelle sicher, dass curl vorhanden ist.
if ! command -v nextdns >/dev/null 2>&1; then
  echo "[*] Installing NextDNS CLI"
  curl -fsSL https://nextdns.io/install | sh
fi

echo "[*] nextdns version: $(nextdns version 2>/dev/null || true)"

# 2) Konfig anlegen (Profile-ID eintragen!)
# WICHTIG: PROFILE_ID anpassen
PROFILE_ID="${1:-}"

if [ -z "$PROFILE_ID" ]; then
  echo "ERROR: missing PROFILE_ID"
  echo "Usage: $0 <PROFILE_ID>"
  exit 1
fi

cat > /etc/nextdns.conf <<EOF
profile $PROFILE_ID
report-client-info true
cache-size 10MB
listen 127.0.0.1:5353
EOF

chmod 0644 /etc/nextdns.conf
echo "[OK] /etc/nextdns.conf written"
