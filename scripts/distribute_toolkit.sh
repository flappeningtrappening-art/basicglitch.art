#!/bin/bash

# Configuration
SHARED_DRIVE="/media/sf_minty_windows"
TOOLKIT_SOURCE="$HOME/monetization/basic-glitch-art/scripts/krita/BasicGlitch_toolkit"
DEST_FOLDER="$SHARED_DRIVE/BasicGlitch_Distribution"

echo "🚀 BASIC GLITCH TOOLKIT: SYSTEM-WIDE DISTRIBUTION v3 (FIXED PATHS)"
echo "================================================================"

# 1. Check Shared Drive
if [ ! -d "$SHARED_DRIVE" ]; then
    echo "❌ Shared drive not found at $SHARED_DRIVE"
    exit 1
fi

# 2. Create Distribution Folder
mkdir -p "$DEST_FOLDER"

# 3. Copy Toolkit
cp -rf "$TOOLKIT_SOURCE" "$DEST_FOLDER/"
cp -f "$HOME/monetization/basic-glitch-art/scripts/krita/kritapykrita_BasicGlitch_toolkit.desktop" "$DEST_FOLDER/"

# 4. Generate Windows Installer (System Path) with Path-Fix
cat > "$DEST_FOLDER/Install_System.bat" <<'EOF'
@echo off
echo BASIC GLITCH SYSTEM INSTALLER v3
echo ================================
echo.

:: Fix: Get the directory where this BAT file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Target your verified path
set "TARGET_DIR=C:\Program Files\Krita (x64)\share\krita\pykrita"
echo Source: %SCRIPT_DIR%
echo Target: %TARGET_DIR%

:: Check for Admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo [!] ERROR: This script MUST be 'Run as Administrator'.
    echo     Right-click this file and select 'Run as Administrator'.
    echo.
    pause
    exit /b 1
)

if not exist "%TARGET_DIR%" (
    echo.
    echo [!] ERROR: Path not found. Check your Krita installation path.
    pause
    exit /b 1
)

echo.
echo [1/2] Copying Registration File...
copy /Y "kritapykrita_BasicGlitch_toolkit.desktop" "%TARGET_DIR%\"

echo.
echo [2/2] Copying Toolkit Folder...
if exist "%TARGET_DIR%\BasicGlitch_toolkit" (
    echo [!] Removing old toolkit...
    rmdir /s /q "%TARGET_DIR%\BasicGlitch_toolkit"
)
xcopy /E /I /Y "BasicGlitch_toolkit" "%TARGET_DIR%\BasicGlitch_toolkit"

echo.
echo ✅ SYSTEM INSTALLATION COMPLETE!
echo    Restart Krita and check Tools -> Scripts.
echo.
pause
EOF

echo "✅ Distribution package updated at: $DEST_FOLDER"
echo "👉 Go to Windows, open that folder, and RUN Install_System.bat AS ADMIN"
