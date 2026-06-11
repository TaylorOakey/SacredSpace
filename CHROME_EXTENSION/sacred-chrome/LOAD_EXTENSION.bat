@echo off
title SacredSpace OS — Load Chrome Extension
color 0E

echo.
echo  ###############################################
echo  ###  SACREDSPACE OS — Chrome Extension      ###
echo  ###  In Lakesh Alakin  /  S∆CR3DS!G∆L       ###
echo  ###############################################
echo.
echo  This extension must be loaded in Developer Mode.
echo.
echo  STEPS:
echo.
echo  1.  Open Google Chrome
echo  2.  Navigate to:  chrome://extensions
echo  3.  Toggle ON "Developer mode" (top-right corner)
echo  4.  Click "Load unpacked"
echo  5.  Browse to this folder:
echo.
echo        %~dp0sacred-chrome
echo.
echo  6.  Click "Select Folder"
echo  7.  The SacredSpace OS extension will appear.
echo      Pin it to the toolbar via the puzzle icon.
echo.
echo  NOTE: Chrome may warn about developer mode extensions
echo  on each launch — this is normal for unpacked extensions.
echo  Click "Keep it" or simply dismiss the banner.
echo.
echo  ─────────────────────────────────────────────
echo  Opening chrome://extensions for you now...
echo  ─────────────────────────────────────────────
echo.

start chrome "chrome://extensions"

echo  Press any key to close this window.
pause > /dev/null
