#!/bin/sh
set -eu

# Wenn Internet-Sharing aktiv ist, willst du evtl. "kein Captive" signalisieren.
# Hier pragmatisch: Wenn /run/cdc-inet.on existiert => "online"
ONLINE_FLAG="/run/cdc-inet.on"

# Sehr einfache Heuristik: wenn Flag existiert -> success; sonst -> portal
if [ -f "$ONLINE_FLAG" ]; then
  # Android erwartet oft 204 bei connectivitycheck
  # iOS erwartet oft "Success" oder eine 200 mit bestimmtem Body – aber 204 ist ok für "kein captive".
  echo "Status: 204 No Content"
  echo "Content-Type: text/plain"
  echo "Cache-Control: no-store"
  echo ""
  exit 0
fi

# Captive aktiv -> liefere Portal (HTML) mit Hinweis + Link auf UI
echo "Content-Type: text/html; charset=utf-8"
echo "Cache-Control: no-store"
echo ""
cat <<'HTML'
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PocketCHIP Setup</title>
  <style>
    body{font-family:sans-serif;margin:0;padding:18px;background:#f6f6f6}
    .card{background:#fff;border-radius:10px;padding:16px;box-shadow:0 2px 10px rgba(0,0,0,.06);max-width:720px;margin:0 auto}
    a{display:inline-block;margin-top:12px;padding:10px 12px;border-radius:8px;border:1px solid #ccc;text-decoration:none;color:#111}
    small{display:block;margin-top:10px;color:#555}
  </style>
</head>
<body>
  <div class="card">
    <h1>PocketCHIP Setup</h1>
    <p>USB verbunden. Konfiguriere WLAN und Internet-Sharing.</p>
    <a href="/">Zum Control Panel</a>
    <small>Hinweis: Sobald Internet-Sharing aktiviert ist, wird dieses Captive-Portal ggf. nicht mehr automatisch geöffnet.</small>
  </div>
</body>
</html>
HTML