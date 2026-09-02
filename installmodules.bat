@echo off
cd /d "%~dp0"
where uv >nul 2>nul
if errorlevel 1 (
    echo uv is required. Install it with: winget install --id astral-sh.uv --exact
    pause
    exit /b 1
)

uv sync --locked
if errorlevel 1 (
    pause
    exit /b 1
)

echo Dependencies installed. Run ActVib with: uv run actvib
pause
