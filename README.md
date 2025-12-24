# PocketCHIP CDC Web UI

Minimalistisches, ressourcenschonendes Webinterface zur Steuerung von
USB-CDC Internet Sharing auf dem **PocketCHIP** (Debian Buster).

Die Oberfläche läuft ausschließlich über **usb0 (192.168.7.1)** und ist
dafür gedacht, den PocketCHIP unkompliziert als
USB-Ethernet-Gateway zu nutzen (z. B. Laptop ↔ PocketCHIP ↔ WLAN).

---

## Features

- Aktivieren / Deaktivieren von CDC Internet Sharing
- Statusanzeige (usb0, uplink, ip_forward, iptables, dnsmasq)
- Läuft mit:
  - `busybox httpd`
  - POSIX-Shell (`/bin/sh`)
- Keine Datenbank
- Kein PHP
- Kein Framework
- Kein JavaScript-Buildsystem

**Ziel:** maximale Robustheit bei minimalem Ressourcenverbrauch.

---

## Architektur (Kurzfassung)

```
Browser (Client)
  │
  │ HTTP (usb0, 192.168.7.1:8080)
  ▼
busybox httpd
  │
  │ CGI
  ▼
cdc.cgi
  │
  │ sudo (NOPASSWD, eingeschränkt)
  ▼
cdc-share (Shell)
  │
  ├─ ip / iptables
  ├─ dnsmasq
  └─ sysctl (ip_forward)
```

---

## Voraussetzungen

- PocketCHIP
- Debian 10 (buster)
- Pakete:
  - busybox
  - dnsmasq
  - iptables (legacy)
  - sudo
- Netzwerk:
  - `usb0` (CDC Gadget)
  - `wlan0` oder anderes Default-Uplink-Interface

---

## Installation (Kurzform)

```sh
git clone https://github.com/<user>/chip-webui.git
cd chip-webui
```

Systemweite Komponenten:
- `/usr/local/sbin/cdc-share`
- `/etc/sudoers.d/chip-webui`
- `/etc/systemd/system/chip-webui.service`

Webroot:
- `~/chip-webui/web`

Service aktivieren:
```sh
sudo systemctl daemon-reload
sudo systemctl enable --now chip-webui.service
```

Aufruf vom Client:
```
http://192.168.7.1:8080/
```

---

## Sicherheit

**Bewusste Entscheidungen:**

- Webinterface lauscht **nur auf usb0**
- Keine Authentifizierung (physischer Zugriff erforderlich)
- `sudo` ist strikt auf `cdc-share {status,up,down}` begrenzt
- `cdc-share` verweigert Änderungen, wenn eine SSH-Session über `192.168.7.x` läuft
  (Schutz vor Selbst-Aussperrung)

**Nicht geeignet für:**
- Internet-exponierte Systeme
- Mehrbenutzer-Umgebungen
- Untrusted Clients

---

## Status

**Reifegrad:** experimentell / funktional  
**Getestet auf:** PocketCHIP, Debian Buster  
**Nicht getestet auf:** neuere Debian-Versionen

---

## Motivation

Der PocketCHIP ist langsam, alt und limitiert – und genau deshalb
ist dieses Projekt **absichtlich simpel**.

Wenn etwas mit:
- weniger RAM
- weniger CPU
- weniger Abhängigkeiten

lösbar ist, dann wird es hier so umgesetzt.

---

## Lizenz

MIT

