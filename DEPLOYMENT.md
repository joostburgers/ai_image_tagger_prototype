# Deployment Guide - AI Image Bias Tagger

This guide covers deploying your AI Image Bias Tagger to various platforms.

## Option 1: GitHub Pages + Backend Service (Recommended)

GitHub Pages only supports static sites, so you'll need to deploy the backend separately.

### Deploy Backend to Render/Railway/Heroku

#### Using Render (Free tier available):

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Create account at [Render.com](https://render.com)**

3. **Create New Web Service**:
   - Connect your GitHub repository
   - Name: `ai-image-bias-tagger`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

4. **Set Environment Variables**:
   - `FLASK_ENV=production`
   - `FLASK_SECRET_KEY=[generate a random key]`

5. **Deploy** - Render will give you a URL like `https://ai-image-bias-tagger.onrender.com`

#### Using Railway (Free tier):

1. **Create account at [Railway.app](https://railway.app)**

2. **Deploy from GitHub**:
   - New Project → Deploy from GitHub
   - Select your repository
   - Railway auto-detects Python and deploys

3. **Set Environment Variables** in Railway dashboard:
   - `FLASK_ENV=production`
   - `PORT=8080` (Railway provides this automatically)

4. **Generate Domain** - Railway gives you a public URL

#### Using Heroku:

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create Heroku app**:
   ```bash
   heroku create ai-image-bias-tagger
   ```

3. **Deploy**:
   ```bash
   git push heroku main
   ```

4. **Set config**:
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set FLASK_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
   ```

5. **Open app**:
   ```bash
   heroku open
   ```

---

## Option 2: Hugging Face Spaces (Recommended for AI/ML projects)

Hugging Face Spaces supports Flask apps and is free!

1. **Create account at [Hugging Face](https://huggingface.co)**

2. **Create new Space**:
   - Go to Spaces → Create new Space
   - Name: `ai-image-bias-tagger`
   - SDK: **Gradio** or **Streamlit** (you'll need to adapt) OR use **Docker**

3. **For Docker deployment, create `Dockerfile`**:
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 7860
   CMD ["python", "app.py"]
   ```

4. **Push code to Space**:
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/ai-image-bias-tagger
   git push hf main
   ```

---

## Option 3: PythonAnywhere (Simplest for Flask)

1. **Create account at [PythonAnywhere.com](https://www.pythonanywhere.com)** (free tier available)

2. **Upload code**:
   - Use their file browser or Git to clone your repo
   - Install dependencies in a virtualenv

3. **Configure Web App**:
   - Web tab → Add new web app
   - Python version: 3.10
   - Framework: Flask
   - Point to your `app.py`

4. **Set up paths** in WSGI configuration file

---

## Option 4: Local Network/VPS Deployment

### For VPS (Digital Ocean, Linode, AWS EC2):

1. **Set up server**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

2. **Clone repo and install**:
   ```bash
   git clone https://github.com/joostburgers/ai_image_tagger_prototype.git
   cd ai_image_tagger_prototype
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Use Gunicorn for production**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

4. **Configure Nginx as reverse proxy**

5. **Set up systemd service** for auto-restart

---

## Important Notes for Deployment

### Security:
- Set a secure `FLASK_SECRET_KEY` environment variable
- Don't commit sensitive data or API keys to git
- Use environment variables for configuration

### Database:
- SQLite works for prototypes but consider PostgreSQL for production
- The database file needs write permissions

### Scraping:
- Most cloud platforms don't support Selenium/Chrome
- You'll need to run the scraper locally and upload scraped images
- Or use a headless browser service like BrowserStack/Selenium Grid

### File Storage:
- Uploaded/scraped images should be stored in cloud storage (AWS S3, Cloudinary)
- Or commit sample images to the repository for demo purposes

---

## Quick Start for Demo Deployment

**Easiest path for demo:**

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

2. **Deploy to Render.com** (completely free):
   - Sign up at render.com
   - "New Web Service" → Connect GitHub
   - Select repository
   - Render auto-configures everything!

3. **Done!** Your app is live at `https://your-app.onrender.com`

---

## Testing Deployment Locally

Test production mode locally before deploying:

```bash
$env:FLASK_ENV="production"
$env:PORT="8080"
python app.py
```

Visit `http://localhost:8080` to verify everything works.
