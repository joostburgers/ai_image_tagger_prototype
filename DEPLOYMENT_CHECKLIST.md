# Deployment Checklist

## Before Deploying

- [ ] Test app locally: `python app.py`
- [ ] Verify all dependencies in `requirements.txt`
- [ ] Check `.gitignore` excludes sensitive files
- [ ] Add some sample images to `images/` folder for demo
- [ ] Test with mock data first
- [ ] Set `FLASK_ENV=production` for deployment

## Files Ready for Deployment

- [x] `app.py` - Flask application with environment variable support
- [x] `requirements.txt` - All Python dependencies
- [x] `Procfile` - Process file for Heroku/Render
- [x] `runtime.txt` - Python version specification
- [x] `.gitignore` - Excludes unnecessary files
- [x] `DEPLOYMENT.md` - Detailed deployment guide

## Quick Deploy to Render.com (Easiest)

1. **Commit all changes**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Sign up at [Render.com](https://render.com)**

3. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select `ai_image_tagger_prototype` repository
   - Render auto-detects settings!

4. **Configure (optional)**:
   - Name: `ai-image-bias-tagger`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt` (auto-detected)
   - Start Command: `python app.py` (auto-detected)
   - Instance Type: Free

5. **Add Environment Variables**:
   - `FLASK_ENV` = `production`
   - `FLASK_SECRET_KEY` = [generate random: `python -c "import secrets; print(secrets.token_hex(32))"`]

6. **Deploy**:
   - Click "Create Web Service"
   - Wait 2-3 minutes for build
   - Your app will be live at `https://ai-image-bias-tagger.onrender.com`

## After Deployment

- [ ] Test all pages work
- [ ] Verify images load correctly
- [ ] Test tagging functionality
- [ ] Check dashboard displays correctly
- [ ] Share URL with users!

## Notes

- **Free tier limitations**: 
  - Render free tier spins down after inactivity (cold starts)
  - First request may be slow (15-30 seconds)
  - Persistent disk not included (database resets on redeploy)
  
- **For production use**, consider:
  - Upgrading to paid tier
  - Using PostgreSQL instead of SQLite
  - Setting up cloud storage for images (AWS S3, Cloudinary)
  - Adding authentication

- **Scraping**: 
  - Run scraper locally, commit images to git
  - Or set up scheduled scraping on a separate service
  - Cloud platforms usually don't support Chrome/Selenium

## Testing Production Mode Locally

```powershell
$env:FLASK_ENV="production"
$env:PORT="8080"
python app.py
```

Visit `http://localhost:8080`
