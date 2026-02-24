@echo off
setlocal

echo ==========================================
echo Prompt Image Search + Dedupe - Windows Setup
echo ==========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo Python is not installed or not on PATH.
  echo Install Python from https://www.python.org/downloads/windows/
  echo IMPORTANT: during install, check "Add python.exe to PATH".
  pause
  exit /b 1
)

if not exist ".venv" (
  echo Creating local virtual environment...
  python -m venv .venv
  if errorlevel 1 (
    echo Failed to create .venv
    pause
    exit /b 1
  )
)

echo Installing dependencies for prompt search app and dedupe tool...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements-image-search.txt
if errorlevel 1 (
  echo Failed to install dependencies.
  echo If your network blocks pip, try a different network and rerun this file.
  pause
  exit /b 1
)

echo.
echo Setup complete.
echo.
echo Primary goal (prompt image search):
echo   run_image_search_windows.bat index "D:\Photos" "E:\Archive"
echo   run_image_search_windows.bat ui

echo.
echo Optional duplicate cleanup:
echo   run_dedupe_windows.bat scan "D:\Photos"
echo.
pause
endlocal
