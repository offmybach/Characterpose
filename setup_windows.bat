@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo ==========================================
echo Prompt Image Search + Dedupe - Windows Setup (Pivot: no venv)
echo Script folder: %SCRIPT_DIR%
echo ==========================================
echo.

set PYTHON_EXE=

if exist "python_path.txt" (
  for /f "usebackq delims=" %%I in ("python_path.txt") do (
    set "PYTHON_EXE=%%~I"
    goto :path_loaded
  )
)

:path_loaded
set "PYTHON_EXE=%PYTHON_EXE:\"=%"
set "PYTHON_EXE=%PYTHON_EXE:"=%"

if defined PYTHON_EXE echo python_path.txt found. Requested interpreter: %PYTHON_EXE%

if not defined PYTHON_EXE (
  for /f "delims=" %%I in ('py -3.12 -c "import sys; print(sys.executable)" 2^>nul') do set PYTHON_EXE=%%I
)
if not defined PYTHON_EXE (
  for /f "delims=" %%I in ('py -3 -c "import sys; print(sys.executable)" 2^>nul') do set PYTHON_EXE=%%I
)
if not defined PYTHON_EXE (
  for /f "delims=" %%I in ('python -c "import sys; print(sys.executable)" 2^>nul') do set PYTHON_EXE=%%I
)

if not defined PYTHON_EXE (
  echo [FAIL] Could not find a usable Python interpreter.
  echo Install Python 3.11+ from https://www.python.org/downloads/windows/
  pause
  exit /b 1
)

if not exist "%PYTHON_EXE%" (
  echo [FAIL] Selected python path does not exist: %PYTHON_EXE%
  echo Update python_path.txt with a valid full path to python.exe
  pause
  exit /b 1
)

echo Using Python: %PYTHON_EXE%

echo %PYTHON_EXE% | find /I "python_embeded" >nul
if not errorlevel 1 (
  echo [FAIL] Detected ComfyUI embedded Python path.
  echo This setup must use a full Python install, not python_embeded.
  echo Create python_path.txt in this same folder with one line, e.g.:
  echo C:\PortableTools\python-3.12.10-amd64\python.exe
  pause
  exit /b 1
)

echo Preparing local dependency folder (.deps)...
if not exist ".deps" mkdir ".deps"

"%PYTHON_EXE%" -m pip --version >nul 2>nul
if errorlevel 1 (
  echo [FAIL] pip is not available on selected Python.
  echo Try: "%PYTHON_EXE%" -m ensurepip --upgrade
  pause
  exit /b 1
)

echo Installing/updating dependencies into .deps (no virtualenv)...
"%PYTHON_EXE%" -m pip install --upgrade pip
"%PYTHON_EXE%" -m pip install --upgrade --target .deps -r requirements-image-search.txt
if errorlevel 1 (
  echo [FAIL] Failed installing requirements-image-search.txt
  pause
  exit /b 1
)
"%PYTHON_EXE%" -m pip install --upgrade --target .deps -r requirements-image-dedupe.txt
if errorlevel 1 (
  echo [FAIL] Failed installing requirements-image-dedupe.txt
  pause
  exit /b 1
)

echo.
echo Verifying imports using local .deps...
set "PYTHONPATH=%SCRIPT_DIR%.deps"
"%PYTHON_EXE%" -c "import PIL, numpy, sentence_transformers, streamlit, imagehash; print('[OK] core modules import successfully')"
if errorlevel 1 (
  echo [FAIL] Import verification failed.
  pause
  exit /b 1
)

echo.
echo Setup complete. No .venv required.
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
