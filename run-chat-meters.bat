@echo off
REM Just the always-on-top per-chat usage meters, no main window.
setlocal
cd /d "%~dp0"

set "PY=py"
where py >nul 2>nul
if errorlevel 1 set "PY=python"

"%PY%" -c "import psutil" >nul 2>nul
if errorlevel 1 (
  echo Installing psutil ...
  "%PY%" -m pip install --user psutil
)

start "" "%PY%" resource_guard.py --meters
