# 🚀 Quick Start Guide - AI Image Bias Tagger

## What You've Built

A complete web application that:
- ✅ Scrapes AI-generated images from Sora
- ✅ Downloads images locally to `images/` folder  
- ✅ Extracts metadata (prompt, creator, likes, title)
- ✅ Presents images to users for bias tagging
- ✅ Tracks views and manages image lifecycle
- ✅ Shows analytics dashboard
- ✅ Ready for cloud deployment!

---

## 📦 Deploy to GitHub + Render (5 minutes)

### Step 1: Push to GitHub

```bash
git add .
git commit -m "AI Image Bias Tagger - Ready for deployment"
git push origin main
```

### Step 2: Deploy to Render.com

1. Go to [Render.com](https://render.com) and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select `ai_image_tagger_prototype` repository
5. Render auto-fills everything - just click **"Create Web Service"**
6. Wait 2 minutes... Done! 🎉

Your app will be live at: `https://ai-image-bias-tagger.onrender.com`

### Step 3: Add Sample Images (Optional)

Before deploying, add a few scraped images so your demo works immediately:

```powershell
# Run scraper to get real images
python scraper_enhanced.py

# Commit images to git
git add images/
git commit -m "Add sample images"
git push
```

---

## 🏃 Running Locally

### Development Mode:
```powershell
python app.py
```

Visit: http://localhost:5000

### With Scraped Images:
```powershell
# 1. Run scraper
python scraper_enhanced.py

# 2. Clear database
python clear_database.py

# 3. Load scraped images
python add_images.py

# 4. Start app
python app.py
```

---

## 📁 Project Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask web server |
| `database.py` | SQLite database management |
| `scraper_enhanced.py` | Sora image scraper (downloads to `images/`) |
| `scraper.py` | Mock data generator |
| `clear_database.py` | Reset database |
| `add_images.py` | Import scraped images to database |
| `templates/` | HTML pages |
| `static/` | CSS & JavaScript |
| `images/` | Downloaded images |
| `requirements.txt` | Python dependencies |
| `Procfile` | Deployment configuration |
| `DEPLOYMENT.md` | Full deployment guide |

---

## 🎯 How Scraping Works

The scraper now:
1. Opens Chrome browser
2. Goes to https://sora.chatgpt.com/explore/top
3. Collects links to individual generation pages
4. Visits each page
5. **Downloads the actual image** from `<img alt="Generated image">`
6. Saves to `images/` folder as `gen_01k94n8g.webp`
7. Extracts: prompt, creator, title, likes
8. Saves metadata to JSON
9. Filters for images with people

---

## 🌐 Deployment Options Compared

| Platform | Free Tier | Ease | Best For |
|----------|-----------|------|----------|
| **Render** | ✅ Yes | ⭐⭐⭐⭐⭐ Easy | **Recommended - Best overall** |
| Railway | ✅ Yes ($5 credit) | ⭐⭐⭐⭐ Easy | Good alternative |
| Heroku | ❌ No | ⭐⭐⭐ Medium | If you already use it |
| Hugging Face | ✅ Yes | ⭐⭐⭐ Medium | ML/AI focused projects |
| PythonAnywhere | ✅ Yes | ⭐⭐⭐⭐ Easy | Python-specific hosting |

---

## 🔧 Environment Variables

For production deployment, set these:

```
FLASK_ENV=production
FLASK_SECRET_KEY=<random-32-char-hex>
PORT=8080
```

Generate secret key:
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 💡 Tips

### For Best Demo:
1. Run scraper locally to get 10-20 real Sora images
2. Commit those images to git
3. Deploy to Render
4. App works immediately with real data!

### Limitations of Free Hosting:
- Render free tier "sleeps" after 15 min inactivity
- First request after sleep = 30 second cold start
- SQLite database resets on each deploy
- No persistent storage (upload files to git instead)

### For Production:
- Upgrade to paid tier ($7/month)
- Use PostgreSQL database
- Store images in AWS S3 or Cloudinary
- Add user authentication

---

## 🐛 Troubleshooting

**Images not showing after deploy:**
- Make sure you committed images to git: `git add images/`
- Check Flask is serving from correct path: `/images/<filename>`

**Database empty:**
- Run `python add_images.py` to load scraped data
- Or the app auto-loads mock data on first run

**Scraper finds 0 links:**
- Sora's HTML structure may have changed
- Check debug output for what links were found
- You may need to update selectors in `_collect_image_links()`

---

## 📊 Usage Stats

Once deployed, users can:
- View AI-generated images
- Tag bias (ageism, genderism, ableism, colorism)
- See dashboard with statistics
- Each image shown to 5 users
- Images deleted if no bias found after 5 views

---

## 🎉 You're Ready!

Your app is complete and ready to deploy. Choose your platform and go live! 

**Recommended path:**
1. `git push` to GitHub
2. Deploy to Render (2 clicks)
3. Share your app with the world! 🌍

Need help? See `DEPLOYMENT.md` for detailed guides.
