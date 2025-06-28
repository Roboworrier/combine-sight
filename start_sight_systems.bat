@echo off
echo ========================================
echo    SIGHT-SYSTEMs Unified Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "BOTSIGHT" (
    echo ERROR: BOTSIGHT directory not found
    echo Please run this script from the SIGHT-SYSTEMs root directory
    pause
    exit /b 1
)

if not exist "CHIPSIGHT" (
    echo ERROR: CHIPSIGHT directory not found
    echo Please run this script from the SIGHT-SYSTEMs root directory
    pause
    exit /b 1
)

if not exist "plant_union" (
    echo ERROR: plant_union directory not found
    echo Please run this script from the SIGHT-SYSTEMs root directory
    pause
    exit /b 1
)

echo Starting SIGHT-SYSTEMs...
echo.
echo This will start:
echo   - PLANT_UNION (Landing Page): http://localhost:5002
echo   - BOTSIGHT (Bot Assembly): https://localhost:5000
echo   - CHIPSIGHT (Digital Twin): http://localhost:5001
echo.
echo Press Ctrl+C to stop all applications
echo.

REM Start the unified launcher (simple version)
python run_simple.py

pause 