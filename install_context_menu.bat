@echo off
chcp 65001 >nul
setlocal

rem === Installs a "Compress images to WEB" entry into the folder right-click menu ===
rem Writes to HKCU so no admin rights are required.

set "TARGET=%~dp0compress_images.bat"
set "TARGET=%TARGET:~0,-1%"

if not exist "%TARGET%" (
    echo.
    echo  compress_images.bat not found next to this installer.
    echo  Expected: %TARGET%
    echo.
    pause
    exit /b 1
)

set "LABEL=Compress images to WEB"
set "KEY1=HKCU\Software\Classes\Directory\shell\CompressImagesWeb"
set "KEY2=HKCU\Software\Classes\Directory\Background\shell\CompressImagesWeb"

rem -- right-click on a folder --
reg add "%KEY1%" /ve /d "%LABEL%" /f >nul
reg add "%KEY1%" /v Icon /d "imageres.dll,-122" /f >nul
reg add "%KEY1%\command" /ve /d "\"%TARGET%\" \"%%1\"" /f >nul

rem -- right-click on empty space inside an open folder --
reg add "%KEY2%" /ve /d "%LABEL%" /f >nul
reg add "%KEY2%" /v Icon /d "imageres.dll,-122" /f >nul
reg add "%KEY2%\command" /ve /d "\"%TARGET%\" \"%%V\"" /f >nul

echo.
echo  Installed. Right-click any folder ^-^> "%LABEL%"
echo  Script location: %TARGET%
echo.
pause
endlocal
