@echo off
REM Run Ping-Pong. Uses "py -3" on Windows if "python" is not in PATH.
cd /d "%~dp0"

set PY=python
py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PY=py -3
    echo Using: py -3
) else (
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Python not found.
        echo Install Python from https://www.python.org/downloads/
        echo Or run in a terminal: py -3 -u ping_pong_cursor.py
        pause
        exit /b 1
    )
    echo Using: python
)

echo.
echo Starting Ping-Pong (check taskbar if window is behind others)...
echo.
%PY% -u ping_pong_cursor.py

echo.
echo Game exited.
pause
