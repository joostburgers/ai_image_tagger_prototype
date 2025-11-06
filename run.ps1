# Run Script for AI Image Bias Tagger

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "AI Image Bias Tagger - Starting" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "Virtual environment not found. Running setup first...`n" -ForegroundColor Yellow
    & ".\setup.ps1"
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Run the application
Write-Host "Starting Flask application...`n" -ForegroundColor Yellow
python app.py
