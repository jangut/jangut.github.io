@echo off
chcp 65001 >nul
pushd "%~dp0.."

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python 3 first.
    pause >nul
    exit /b 1
)

:: Use port from env or default 8080
if "%PORT%"=="" set PORT=8080

echo ==================================
echo   Blog Manager v1.0
echo   Running on port %PORT%
echo   URL: http://localhost:%PORT%
echo ==================================
echo.

:: Start server in background
start /b python manager.py
if errorlevel 1 (
    echo Failed to start server!
    pause >nul
    exit /b 1
)

timeout /t 2 /nobreak >nul

:: Open browser
start http://localhost:%PORT%

echo Open http://localhost:%PORT% in your browser if not automatic.
echo.
echo [Ctrl+C] to stop server  | more
pause >nul

:: Cleanup on close
taskkill /f /im python.exe >nul 2>&1
popd
