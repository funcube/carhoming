@echo off
chcp 65001 >nul
setlocal

rem === Removes the "Compress images to WEB" right-click menu entry ===

reg delete "HKCU\Software\Classes\Directory\shell\CompressImagesWeb" /f >nul 2>&1
reg delete "HKCU\Software\Classes\Directory\Background\shell\CompressImagesWeb" /f >nul 2>&1

echo.
echo  Right-click menu entry removed.
echo.
pause
endlocal
