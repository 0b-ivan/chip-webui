#!/bin/sh
set -e

[ "$(id -u)" -eq 0 ] || { echo "Run as root: sudo ./install.sh"; exit 1; }

install -d /usr/local/sbin /etc/systemd/system /etc/sudoers.d

echo "[*] Installing shutdown script"
install -m 0755 bin/shutdown-chip /usr/local/sbin/shutdown-chip

echo "[*] Installing CDC scripts"
install -m 0755 bin/cdc-base /usr/local/sbin/cdc-base
install -m 0755 bin/cdc-inet /usr/local/sbin/cdc-inet

echo "[*] Installing systemd units"
install -m 0644 systemd/cdc-base.service /etc/systemd/system/
install -m 0644 systemd/chip-webui.service /etc/systemd/system/

echo "[*] Reloading systemd"
systemctl daemon-reload

echo "[*] Enable CDC base"
systemctl enable --now cdc-base.service

echo "[*] Installing sudoers for WebUI"
install -m 0440 sudoers/chip-webui /etc/sudoers.d/chip-webui
visudo -c

echo "[OK] Installation finished"
systemctl enable --now chip-webui.service
echo "[*] Enable WebUI"