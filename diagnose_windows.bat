@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo ==========================================
echo Prompt Image Search - Quick Diagnose (pivot: no venv)
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

if defined PYTHON_EXE echo [OK] python_path.txt requests: %PYTHON_EXE%

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
  echo [FAIL] Could not detect Python.
  goto end
)

echo [OK] Python detected: %PYTHON_EXE%

echo %PYTHON_EXE% | find /I "python_embeded" >nul
if not errorlevel 1 (
  echo [FAIL] You are still using ComfyUI embedded Python.
  echo Create or fix python_path.txt in this folder with a C: Python path.
  goto end
)

echo.
"%PYTHON_EXE%" -c "import sys; print('Executable:', sys.executable)"
"%PYTHON_EXE%" -m pip --version
if errorlevel 1 (
  echo [FAIL] pip not available for %PYTHON_EXE%
  goto end
)

echo.
if not exist ".deps" (
  echo [WARN] .deps not found yet. Run setup_windows.bat first.
  goto compile_check
)

echo [OK] .deps folder found
set "PYTHONPATH=%SCRIPT_DIR%.deps"
echo Checking required modules from .deps...
"%PYTHON_EXE%" -c "import PIL, numpy, sentence_transformers, streamlit, imagehash; print('[OK] core modules import successfully')"
if errorlevel 1 (
  echo [FAIL] Some modules missing in .deps. Run setup_windows.bat
  goto end
)

:compile_check
echo.
echo Checking app scripts compile...
"%PYTHON_EXE%" -m py_compile image_prompt_search.py streamlit_image_search_app.py image_dedupe_manager.py
if errorlevel 1 (
  echo [FAIL] Compile check failed.
  goto end
)

echo [OK] Local setup looks good.
echo Next:
echo   run_image_search_windows.bat index "D:\Photos"
echo   run_image_search_windows.bat ui

:end
pause
endlocal
