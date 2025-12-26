# PocketCHIP WebUI

Minimalistisches, vollständig offline-fähiges WebUI für den PocketCHIP.
Ausgelegt für Betrieb **ausschließlich über usb0 (CDC Ethernet)**.

---

## Zugriff (Port 80)

Das WebUI läuft bewusst **ohne HTTPS und ohne externe Abhängigkeiten**.

**Browser-Aufruf:**

http://192.168.7.1:80/

Der Port **80 ist fest konfiguriert** (busybox httpd).
Ein expliziter Port ist optional.

---

## Architektur

- USB CDC Ethernet (`usb0`)
- BusyBox `httpd`
- CGI (POSIX shell)
- systemd Services
- tcpdump

Webroot:
```
/home/chip/chip-webui/web
```

---

## CGI-Endpunkte

Pfad:
```
/cgi-bin/
```

| Skript | Funktion |
|------|---------|
| cdc.cgi | USB → Internet NAT |
| wifi.cgi | WLAN Status / Scan / Connect |
| shutdown.cgi | Shutdown |
| sniffer.cgi | PCAP Sniffer Steuerung |
| sniffer-live.cgi | Live Sniffer (SSE) |

---

## Packet Sniffer (PCAP)

Service:
```
chip-sniffer.service
```

- Interface: usb0
- Tool: tcpdump
- Rotation: 6 × 5 MB
- Speicher:
```
/var/lib/chip-sniffer/captures
```

Download:
```
http://192.168.7.1:80/captures/
```

Symlink:
```
web/captures → /var/lib/chip-sniffer/captures
```

---

## Live Sniffer (Browser)

Live-Ausgabe des Netzwerkverkehrs ohne PCAP.

URL:
```
http://192.168.7.1:80/cgi-bin/sniffer-live.cgi
```

Technik:
- Server-Sent Events (SSE)
- tcpdump line-buffered
- 60s Stream, reconnect-fähig
- Kein WebSocket

Ideal für:
- Schnelle Analyse
- Debugging
- Lehr-/Demo-Zwecke

---

## Sicherheit

- Nur über USB erreichbar
- Kein Passwortschutz (physischer Zugriff)
- sudo strikt whitelisted
- Keine WLAN-Exponierung

---

## Ziel

- Minimal
- Robust
- Offline
- Embedded-tauglich

---

## Lizenz

Experimental / Forschungszwecke.
Keine Garantie.
