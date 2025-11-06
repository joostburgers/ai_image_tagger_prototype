# Quick Start Setup Script for AI Image Bias Tagger

Write-Host "================================" -ForegroundColor Cyan
Write-Host "AI Image Bias Tagger - Setup" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Python not found. Please install Python 3.8 or later." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "[OK] Virtual environment already exists" -ForegroundColor Green
}
else {
    python -m venv venv
    Write-Host "[OK] Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "[OK] Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "[OK] Dependencies installed" -ForegroundColor Green

# Create .env file if it doesn't exist
Write-Host "`nSetting up environment..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "[OK] .env file already exists" -ForegroundColor Green
}
else {
    Copy-Item .env.example .env
    Write-Host "[OK] .env file created from template" -ForegroundColor Green
}

# Create data directory
Write-Host "`nCreating data directory..." -ForegroundColor Yellow
if (!(Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
}
Write-Host "[OK] Data directory ready" -ForegroundColor Green

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "================================`n" -ForegroundColor Cyan

Write-Host "To start the application, run:" -ForegroundColor Yellow
Write-Host "  python app.py`n" -ForegroundColor White

Write-Host "Then visit:" -ForegroundColor Yellow
Write-Host "  http://localhost:5000`n" -ForegroundColor White

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
