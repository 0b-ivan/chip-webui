#!/bin/sh
set -e

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

echo "[OK] Installation finished"
