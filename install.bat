@echo off
setlocal enabledelayedexpansion

REM Get the directory where the script is located
set "SCRIPT_DIR=%~dp0"
set "THEMES_DIR=%APPDATA%\Vencord\themes"
set "THEME_FILES=hide.css fork.css"

REM Check if Vencord themes directory exists
if not exist "%THEMES_DIR%" (
    echo Error: Vencord themes directory not found at %THEMES_DIR%
    exit /b 1
)

REM Check if source theme files exist
for %%f in (%THEME_FILES%) do (
    if not exist "%SCRIPT_DIR%%%f" (
        echo Error: Source theme file '%%f' not found in %SCRIPT_DIR%
        exit /b 1
    )
)

REM Create symbolic links
for %%f in (%THEME_FILES%) do (
    mklink "%THEMES_DIR%\%%f" "%SCRIPT_DIR%%%f" >nul 2>&1
    if errorlevel 1 (
        echo Error: Failed to create symbolic link for %%f
        exit /b 1
    )
)

echo Discord Theme installed successfully!
