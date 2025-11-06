# Quick deployment script for AI Image Bias Tagger (PowerShell)

Write-Host "🚀 AI Image Bias Tagger - Deployment Helper" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "📝 Initializing git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
    Write-Host "✅ Git initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already initialized" -ForegroundColor Green
}

# Check for remote
$hasRemote = git remote | Select-String -Pattern "origin"
if (-not $hasRemote) {
    Write-Host ""
    Write-Host "⚠️  No git remote configured" -ForegroundColor Yellow
    Write-Host "Please set up your GitHub repository first:"
    Write-Host "  1. Create repo at https://github.com/new"
    Write-Host "  2. Run: git remote add origin https://github.com/YOUR_USERNAME/ai_image_tagger_prototype.git"
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "📦 Preparing deployment..." -ForegroundColor Cyan
Write-Host ""

# Add all files
Write-Host "Adding files..." -ForegroundColor Yellow
git add .

# Commit
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "Creating commit..." -ForegroundColor Yellow
git commit -m "Deploy AI Image Bias Tagger - $timestamp"

# Push
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host ""
Write-Host "✅ Code pushed to GitHub!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Go to https://render.com"
Write-Host "  2. Click 'New +' → 'Web Service'"
Write-Host "  3. Connect GitHub and select this repository"
Write-Host "  4. Click 'Create Web Service'"
Write-Host ""
Write-Host "Your app will be live in ~2 minutes! 🎉" -ForegroundColor Green
