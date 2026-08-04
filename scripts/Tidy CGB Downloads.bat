@echo off
REM ============================================================
REM  Tidy CGB Downloads
REM  Double-click this. Keep it in the same folder as
REM  tidy_downloads.py — anywhere on the machine is fine.
REM ============================================================
title Tidy CGB Downloads
cd /d "%~dp0"

if not exist "tidy_downloads.py" (
  echo.
  echo  Cannot find tidy_downloads.py.
  echo  Keep this .bat in the SAME FOLDER as tidy_downloads.py.
  echo.
  pause
  exit /b 1
)

REM py launcher first, then plain python
where py >nul 2>&1
if %errorlevel%==0 (
  py "tidy_downloads.py" %*
  goto done
)

where python >nul 2>&1
if %errorlevel%==0 (
  python "tidy_downloads.py" %*
  goto done
)

echo.
echo  Python is not installed on this machine, or it is not on your PATH.
echo.
echo  Install it once from  https://www.python.org/downloads/
echo  and tick "Add Python to PATH" on the first screen of the installer.
echo.
echo  Then double-click this file again.
echo.
pause
exit /b 1

:done
