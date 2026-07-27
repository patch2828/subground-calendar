@echo off
REM RESOURCE GUARD - double-click to watch what's stealing your machine.
REM Right-click -> "Run as administrator" if you want it able to throttle
REM everything (some processes refuse a priority change otherwise).
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

"%PY%" resource_guard.py %*
if errorlevel 1 pause
