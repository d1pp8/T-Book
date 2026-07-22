#!/bin/sh
set -e

echo "[tbook-frontend] publishing build to /frontend ..."
rm -rf /frontend/*
cp -r /dist/* /frontend/
echo "[tbook-frontend] done. $(find /frontend -maxdepth 1 | wc -l) entries published."

tail -f /dev/null
