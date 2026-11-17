#!/bin/sh
set -eu

APP_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SDK_PATH="$(xcrun --sdk macosx26.5 --show-sdk-path)"
APP_BUNDLE="$APP_DIR/FactIndic.app"
CONTENTS="$APP_BUNDLE/Contents"
EXECUTABLE="$CONTENTS/MacOS/FactIndic"

mkdir -p "$CONTENTS/MacOS" "$CONTENTS/Resources"
swiftc \
  -parse-as-library \
  -sdk "$SDK_PATH" \
  -target arm64-apple-macosx13.0 \
  -module-cache-path "${TMPDIR:-/tmp}/factindic-module-cache" \
  -framework SwiftUI \
  -framework AppKit \
  "$APP_DIR/Sources/FactIndicApp/FactIndicApp.swift" \
  -o "$EXECUTABLE"

cat > "$CONTENTS/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleExecutable</key><string>FactIndic</string>
  <key>CFBundleIdentifier</key><string>com.sirohi.factindic</string>
  <key>CFBundleInfoDictionaryVersion</key><string>6.0</string>
  <key>CFBundleName</key><string>FactIndic</string>
  <key>CFBundleDisplayName</key><string>FactIndic</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleSupportedPlatforms</key><array><string>MacOSX</string></array>
  <key>CFBundleShortVersionString</key><string>1.0</string>
  <key>CFBundleVersion</key><string>1</string>
  <key>LSMinimumSystemVersion</key><string>13.0</string>
  <key>NSPrincipalClass</key><string>NSApplication</string>
  <key>NSHighResolutionCapable</key><true/>
</dict>
</plist>
PLIST

printf 'APPL????' > "$CONTENTS/PkgInfo"
codesign --force --deep --sign - "$APP_BUNDLE"
printf 'Built %s\n' "$APP_BUNDLE"
