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
  echo [FAIL] Could not find Python.
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

if /I "%CMD%"=="index" (
  "%PYTHON_EXE%" image_prompt_search.py index --source %* --index-dir .\.image_search_index
  goto end
)

if /I "%CMD%"=="search" (
  "%PYTHON_EXE%" image_prompt_search.py search --index-dir .\.image_search_index --query "%*"
  goto end
)

if /I "%CMD%"=="ui" (
  "%PYTHON_EXE%" -m streamlit run streamlit_image_search_app.py --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false --server.enableCORS true --server.enableXsrfProtection true
  goto end
)

goto help

:menu
set "INTERACTIVE=1"
echo.
echo Prompt Image Search
echo   1^) Build/Rebuild index
echo   2^) Search by prompt (CLI)
echo   3^) Launch UI
echo   4^) Exit
set /p CHOICE=Choose 1-4: 

if "%CHOICE%"=="1" (
  set /p SRC=Enter folders/drives in quotes ^(example: "C:\Users\You\Pictures" "D:\Photos"^): 
  if not defined SRC goto end
  "%PYTHON_EXE%" image_prompt_search.py index --source !SRC! --index-dir .\.image_search_index
  goto end
)
if "%CHOICE%"=="2" (
  set /p QUERY=Enter search prompt ^(example: blue and white shoes^): 
  if not defined QUERY goto end
  "%PYTHON_EXE%" image_prompt_search.py search --index-dir .\.image_search_index --query "!QUERY!"
  goto end
)
if "%CHOICE%"=="3" (
  "%PYTHON_EXE%" -m streamlit run streamlit_image_search_app.py --server.address 127.0.0.1 --server.port 8501 --browser.gatherUsageStats false --server.enableCORS true --server.enableXsrfProtection true
  goto end
)
if "%CHOICE%"=="4" goto end
echo Invalid choice.
goto menu

:help
echo.
echo Usage:
echo   run_image_search_windows.bat index [folders...]
echo   run_image_search_windows.bat search [query words...]
echo   run_image_search_windows.bat ui

goto end

:end
if defined INTERACTIVE pause
endlocal
