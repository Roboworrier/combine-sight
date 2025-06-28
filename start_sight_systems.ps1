# SIGHT-SYSTEMs Unified Launcher PowerShell Script

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SIGHT-SYSTEMs Unified Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if we're in the right directory
$requiredDirs = @("BOTSIGHT", "CHIPSIGHT", "plant_union")
foreach ($dir in $requiredDirs) {
    if (-not (Test-Path $dir)) {
        Write-Host "ERROR: $dir directory not found" -ForegroundColor Red
        Write-Host "Please run this script from the SIGHT-SYSTEMs root directory" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "Starting SIGHT-SYSTEMs..." -ForegroundColor Green
Write-Host ""
Write-Host "This will start:" -ForegroundColor Yellow
Write-Host "  - PLANT_UNION (Landing Page): http://localhost:5002" -ForegroundColor White
Write-Host "  - BOTSIGHT (Bot Assembly): https://localhost:5000" -ForegroundColor White
Write-Host "  - CHIPSIGHT (Digital Twin): http://localhost:5001" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop all applications" -ForegroundColor Yellow
Write-Host ""

# Start the unified launcher (simple version)
try {
    python run_simple.py
} catch {
    Write-Host "Error starting SIGHT-SYSTEMs: $_" -ForegroundColor Red
}

Read-Host "Press Enter to exit" 