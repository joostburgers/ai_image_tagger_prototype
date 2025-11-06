#!/usr/bin/env bash

# Quick deployment script for AI Image Bias Tagger

echo "🚀 AI Image Bias Tagger - Deployment Helper"
echo "==========================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📝 Initializing git repository..."
    git init
    git branch -M main
    echo "✅ Git initialized"
else
    echo "✅ Git repository already initialized"
fi

# Check for remote
if ! git remote | grep -q origin; then
    echo ""
    echo "⚠️  No git remote configured"
    echo "Please set up your GitHub repository first:"
    echo "  1. Create repo at https://github.com/new"
    echo "  2. Run: git remote add origin https://github.com/YOUR_USERNAME/ai_image_tagger_prototype.git"
    echo ""
    exit 1
fi

echo ""
echo "📦 Preparing deployment..."
echo ""

# Add all files
echo "Adding files..."
git add .

# Commit
echo "Creating commit..."
git commit -m "Deploy AI Image Bias Tagger - $(date '+%Y-%m-%d %H:%M:%S')"

# Push
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "🌐 Next steps:"
echo "  1. Go to https://render.com"
echo "  2. Click 'New +' → 'Web Service'"
echo "  3. Connect GitHub and select this repository"
echo "  4. Click 'Create Web Service'"
echo ""
echo "Your app will be live in ~2 minutes! 🎉"
