#!/usr/bin/env bash
# Stages the Workshop upload folder in ~/Zomboid/Workshop/Soapmaker.
# Upload it from the game: main menu -> Workshop -> Soapmaker.
set -euo pipefail
cd "$(dirname "$0")"
DEST="$HOME/Zomboid/Workshop/Soapmaker"
rm -rf "$DEST"
mkdir -p "$DEST/Contents/mods/Soapmaker"
cp workshop/workshop.txt workshop/preview.png "$DEST/"
cp -r 42 common "$DEST/Contents/mods/Soapmaker/"
find "$DEST" -type f | sort
