#!/bin/sh
set -eu
echo "Content-Type: text/plain; charset=utf-8"
echo ""
echo "whoami: $(id -un)"
echo "uid/gid: $(id)"
echo "SSH_CONNECTION: ${SSH_CONNECTION:-<empty>}"
echo ""

QS="${QUERY_STRING:-}"
ACTION="$(printf '%s' "$QS" | sed -n 's/.*action=\([^&]*\).*/\1/p')"
echo "action=$ACTION"
echo ""

sudo -n /usr/local/sbin/cdc-share "${ACTION:-status}" 2>&1 || true
