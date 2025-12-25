#!/bin/sh
set -eu

    echo "Content-Type: text/plain; charset=utf-8"
echo ""

echo "Powering off…"
sudo -n /usr/local/sbin/shutdown-chip