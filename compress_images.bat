@echo off
chcp 65001 >nul
setlocal

rem === Drag a folder onto this .bat to compress every image inside ===

if "%~1"=="" (
    echo.
    echo  Usage: drag a folder onto this file.
    echo.
    pause
    exit /b 1
)

if not exist "%~1\" (
    echo.
    echo  Not a folder: %~1
    echo  Please drag a FOLDER, not a file.
    echo.
    pause
    exit /b 1
)

set "SCRIPT=%~dp0compress_images.py"

if not exist "%SCRIPT%" (
    echo.
    echo  compress_images.py not found next to this .bat
    echo  Expected at: %SCRIPT%
    echo.
    pause
    exit /b 1
)

python "%SCRIPT%" "%~1"
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
    echo  Done. Check the WEB subfolder inside: %~1
) else (
    echo  Finished with errors ^(exit code %RC%^).
)
echo.
pause
endlocal
