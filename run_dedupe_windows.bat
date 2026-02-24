@echo off
setlocal

REM Usage examples:
REM   run_dedupe_windows.bat scan "D:\Photos" "E:\Archive"
REM   run_dedupe_windows.bat scan-visual "D:\Photos"
REM   run_dedupe_windows.bat restore
REM   run_dedupe_windows.bat purge-recycle
REM   run_dedupe_windows.bat purge-permanent

if exist ".venv\Scripts\python.exe" (
  set PYTHON_EXE=.venv\Scripts\python.exe
) else (
  set PYTHON_EXE=python
)

if "%~1"=="" goto help

set CMD=%~1
shift

if "%CMD%"=="scan" (
  %PYTHON_EXE% image_dedupe_manager.py scan --source %* --app-bin .\app_recycle_bin
  goto end
)

if "%CMD%"=="scan-visual" (
  %PYTHON_EXE% image_dedupe_manager.py scan --source %* --app-bin .\app_recycle_bin --visual
  goto end
)

if "%CMD%"=="restore" (
  %PYTHON_EXE% image_dedupe_manager.py restore --app-bin .\app_recycle_bin
  goto end
)

if "%CMD%"=="purge-recycle" (
  %PYTHON_EXE% image_dedupe_manager.py purge --app-bin .\app_recycle_bin --mode recycle
  goto end
)

if "%CMD%"=="purge-permanent" (
  %PYTHON_EXE% image_dedupe_manager.py purge --app-bin .\app_recycle_bin --mode permanent
  goto end
)

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
endlocal
