@echo off
setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set "PYTHON_EXE="
if exist "python_path.txt" (
  for /f "usebackq delims=" %%I in ("python_path.txt") do (
    set "PYTHON_EXE=%%~I"
    goto :path_loaded
  )
)

:path_loaded
set "PYTHON_EXE=%PYTHON_EXE:\"=%"
set "PYTHON_EXE=%PYTHON_EXE:"=%"

if not defined PYTHON_EXE (
  for /f "delims=" %%I in ('py -3.12 -c "import sys; print(sys.executable)" 2^>nul') do set "PYTHON_EXE=%%I"
)
if not defined PYTHON_EXE (
  for /f "delims=" %%I in ('py -3 -c "import sys; print(sys.executable)" 2^>nul') do set "PYTHON_EXE=%%I"
)
if not defined PYTHON_EXE (
  for /f "delims=" %%I in ('python -c "import sys; print(sys.executable)" 2^>nul') do set "PYTHON_EXE=%%I"
)

if not defined PYTHON_EXE (
  echo [FAIL] Could not find Python. Run setup_windows.bat first.
  goto end
)

if not exist ".deps" (
  echo [WARN] .deps folder not found. Run setup_windows.bat first.
)
set "PYTHONPATH=%SCRIPT_DIR%.deps"

set "INTERACTIVE="
if "%~1"=="" goto menu

set "CMD=%~1"
shift

if /I "%CMD%"=="scan" (
  "%PYTHON_EXE%" image_dedupe_manager.py scan --source %* --app-bin .\app_recycle_bin
  goto end
)

if /I "%CMD%"=="scan-visual" (
  "%PYTHON_EXE%" image_dedupe_manager.py scan --source %* --app-bin .\app_recycle_bin --visual
  goto end
)

if /I "%CMD%"=="restore" (
  "%PYTHON_EXE%" image_dedupe_manager.py restore --app-bin .\app_recycle_bin
  goto end
)

if /I "%CMD%"=="purge-recycle" (
  "%PYTHON_EXE%" image_dedupe_manager.py purge --app-bin .\app_recycle_bin --mode recycle
  goto end
)

if /I "%CMD%"=="purge-permanent" (
  "%PYTHON_EXE%" image_dedupe_manager.py purge --app-bin .\app_recycle_bin --mode permanent
  goto end
)

goto help

:menu
set "INTERACTIVE=1"
echo.
echo Dedupe Manager
echo   1^) Scan exact duplicates
echo   2^) Scan exact + visual duplicates
echo   3^) Restore from app recycle bin
echo   4^) Purge app bin to Windows recycle bin
echo   5^) Purge app bin permanently
echo   6^) Exit
set /p CHOICE=Choose 1-6: 

if "%CHOICE%"=="1" (
  set /p SRC=Enter folders/drives in quotes ^(example: "C:\Users\You\Pictures" "D:\Photos"^): 
  if not defined SRC goto end
  "%PYTHON_EXE%" image_dedupe_manager.py scan --source !SRC! --app-bin .\app_recycle_bin
  goto end
)
if "%CHOICE%"=="2" (
  set /p SRC=Enter folders/drives in quotes ^(example: "C:\Users\You\Pictures" "D:\Photos"^): 
  if not defined SRC goto end
  "%PYTHON_EXE%" image_dedupe_manager.py scan --source !SRC! --app-bin .\app_recycle_bin --visual
  goto end
)
if "%CHOICE%"=="3" (
  "%PYTHON_EXE%" image_dedupe_manager.py restore --app-bin .\app_recycle_bin
  goto end
)
if "%CHOICE%"=="4" (
  "%PYTHON_EXE%" image_dedupe_manager.py purge --app-bin .\app_recycle_bin --mode recycle
  goto end
)
if "%CHOICE%"=="5" (
  "%PYTHON_EXE%" image_dedupe_manager.py purge --app-bin .\app_recycle_bin --mode permanent
  goto end
)
if "%CHOICE%"=="6" goto end
echo Invalid choice.
goto menu

:help
echo.
echo Unknown or missing command.
echo.
echo Commands:
echo   scan [folders...]          - exact duplicates only
echo   scan-visual [folders...]   - exact + visual duplicates
echo   restore                    - restore from app recycle bin
echo   purge-recycle              - send app recycle bin files to Windows recycle bin
echo   purge-permanent            - permanently delete app recycle bin files

goto end

:end
if defined INTERACTIVE pause
endlocal
