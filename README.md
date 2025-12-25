# PocketCHIP CDC WebUI

Pragmatisches, ressourcenschonendes Webinterface (HTML + BusyBox `httpd` + CGI), das **nur auf `usb0`** lauscht und die USB‑CDC‑Konfiguration steuert.

## Konzept

Es gibt zwei getrennte Ebenen:

### 1) CDC Base (immer aktiv)
**Ziel:** Sobald der PocketCHIP per USB angeschlossen ist, soll die CDC‑Schnittstelle funktionieren.

- `usb0` bekommt **statisch** `192.168.7.1/24`
- DHCP für den Client über `dnsmasq` (z. B. `192.168.7.2–192.168.7.50`)
- Die WebUI lauscht auf `192.168.7.1:8080`

### 2) CDC Internet Sharing (umschaltbar)
**Ziel:** Optionales Routing/NAT vom USB‑Client ins Uplink‑Netz (meist `wlan0`).

- IPv4 Forwarding (`net.ipv4.ip_forward=1`)
- `iptables` NAT (MASQUERADE) und Forward‑Regeln für `usb0 → uplink`
- Uplink‑Interface wird über Default‑Route erkannt (Fallback z. B. `wlan0`)


## Installation

```bash
git clone https://github.com/USER/chip-webui.git
cd chip-webui
sudo ./install.sh

## Komponenten

### Services / Timer

- `cdc-base.service`  
  setzt `usb0=192.168.7.1/24` und aktiviert DHCP (dnsmasq‑Snippet)

- `cdc-inet` (Script)  
  schaltet nur Internet‑Sharing (NAT/Forwarding) ein/aus

- `chip-webui.service`  
  startet BusyBox `httpd` auf `192.168.7.1:8080` und bedient CGI‑Endpoints

### Scripts

- `/usr/local/sbin/cdc-base`  
  Base‑Setup: USB‑IP + DHCP (dnsmasq)

- `/usr/local/sbin/cdc-inet`  
  Internet‑Sharing Setup: ip_forward + iptables

### WebUI

- statisch: `web/index.html`, optional `web/style.css`, `web/app.js`
- CGI: `web/cgi-bin/*.cgi`

## CGI Endpoints (aktuell)

### CDC Internet Sharing

- `GET /cgi-bin/cdc.cgi?action=status`  
  zeigt `uplink_if=…`, `ip_forward=…` sowie passende iptables‑Regeln

- `GET /cgi-bin/cdc.cgi?action=on`  
  aktiviert NAT/Forwarding (usb0 → uplink)

- `GET /cgi-bin/cdc.cgi?action=off`  
  deaktiviert NAT/Forwarding

Beispiel:

```sh
curl -s "http://192.168.7.1:8080/cgi-bin/cdc.cgi?action=status"
curl -s "http://192.168.7.1:8080/cgi-bin/cdc.cgi?action=on"
curl -s "http://192.168.7.1:8080/cgi-bin/cdc.cgi?action=off"
```
## 📡 WLAN – Scan & Verbinden

Der PocketCHIP nutzt **NetworkManager (`nmcli`)**, um WLAN-Verbindungen
zu scannen und herzustellen.  
Diese Funktion ist sowohl **per CLI** als auch über die **CDC WebUI**
verfügbar.

Das Design ist bewusst **minimalistisch und ressourcenschonend**:

- kein eigenes `wpa_supplicant`-Handling
- kein Framework
- kein dauerhafter Daemon
- Steuerung ausschließlich über `nmcli`

---

### Voraussetzungen

- Debian (PocketCHIP)
- `NetworkManager` aktiv
- WLAN-Interface: `wlan0`
- Benutzer `chip` ist Mitglied der Gruppe `netdev`

Prüfen:

```sh
systemctl is-active NetworkManager
nmcli device status

## sudoers (wichtig)

Die WebUI ruft die Scripts via `sudo -n` auf. Dafür braucht es eine Whitelist:

Datei: `/etc/sudoers.d/chip-webui`

```sudoers
chip ALL=(root) NOPASSWD:   /usr/local/sbin/cdc-inet status,   /usr/local/sbin/cdc-inet on,   /usr/local/sbin/cdc-inet off
```

## Start/Stop

```sh
sudo systemctl daemon-reload

# Base
sudo systemctl enable --now cdc-base.service

# WebUI
sudo systemctl enable --now chip-webui.service
systemctl status chip-webui.service --no-pager -l
```

## Troubleshooting

### WebUI startet nicht: “Address already in use”
Prüfen, ob bereits ein `busybox httpd` auf `192.168.7.1:8080` läuft:

```sh
sudo ss -ltnp | grep ':8080' || true
```

### dnsmasq bindet nicht: “Address already in use”
In der Regel läuft schon ein dnsmasq (systemweit). Lösung ist ein **Snippet** unter `/etc/dnsmasq.d/` und dann `systemctl restart dnsmasq`.

### “sudo: a password is required” in CGI
Whitelist in `/etc/sudoers.d/chip-webui` prüfen und:

```sh
sudo visudo -c
sudo -n -l
```

## Nächste Schritte (geplant)
- WLAN: Toggle, Scan SSIDs, Connect via `nmcli`
- UI: klarere Trennung „CDC Base“ vs „Internet Sharing“

