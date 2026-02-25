@echo off
setlocal

if exist ".venv\Scripts\python.exe" (
  set PYTHON_EXE=.venv\Scripts\python.exe
) else (
  set PYTHON_EXE=python
)

if "%~1"=="" goto help

set CMD=%~1
shift

if "%CMD%"=="index" (
  %PYTHON_EXE% image_prompt_search.py index --source %* --index-dir .\.image_search_index
  goto end
)

if "%CMD%"=="search" (
  %PYTHON_EXE% image_prompt_search.py search --index-dir .\.image_search_index --query %*
  goto end
)

if "%CMD%"=="ui" (
  %PYTHON_EXE% -m streamlit run streamlit_image_search_app.py
  goto end
)

:help
echo.
echo Usage:
echo   run_image_search_windows.bat index [folders...]
echo   run_image_search_windows.bat search [query words...]
echo   run_image_search_windows.bat ui

goto end

:end
endlocal
