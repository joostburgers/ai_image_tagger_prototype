# AI Image Bias Tagger

An educational tool for identifying and tracking bias in AI-generated images from Sora.

## Overview

This prototype system scrapes AI-generated images from [Sora](https://sora.chatgpt.com/explore), filters for images containing people, and presents them to users for bias tagging. The goal is to raise awareness about AI bias and create a dataset for training bias detection models.

## Features

- **Image Scraping**: Automated collection of top images from Sora's explore page
- **People Detection**: Filters images to focus on those depicting people
- **Bias Tagging**: Users can tag images with four bias types:
  - **Ageism**: Age-related stereotypes or underrepresentation
  - **Genderism**: Gender stereotypes or lack of diversity
  - **Ableism**: Disability-related biases or absence
  - **Colorism**: Skin tone or ethnic representation biases
- **Smart Lifecycle**: Images shown to 5 unique users; deleted if no bias is detected, kept for additional review if tagged
- **Analytics Dashboard**: Real-time statistics showing bias patterns and trends
- **Educational Focus**: Designed to highlight how bias appears in seemingly neutral prompts

## Installation

### Prerequisites

- Python 3.8+
- pip
- Chrome browser (for web scraping)

### Setup

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up environment** (optional):
   ```powershell
   Copy-Item .env.example .env
   # Edit .env with your preferred settings
   ```

## Usage

### Running the Application Locally

Start the development server:

```powershell
python app.py
```

The application will be available at:
- **Home**: http://localhost:5000/
- **Tagging Interface**: http://localhost:5000/tag
- **Dashboard**: http://localhost:5000/dashboard
- **About**: http://localhost:5000/about

### Deploying to the Cloud

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for:
- Render.com (recommended - free tier)
- Railway.app
- Heroku
- Hugging Face Spaces
- PythonAnywhere
- VPS/Cloud servers

**Quick Deploy to Render:**
1. Push code to GitHub
2. Sign up at [Render.com](https://render.com)
3. Create new Web Service from your GitHub repo
4. Render auto-detects and deploys!

### Scraping Images from Sora

To scrape real images from Sora:

```powershell
python scraper_enhanced.py
```

**Note**: 
- Requires Chrome browser
- You'll need to authenticate with ChatGPT/Sora manually
- Images are downloaded to the `images/` folder
- The scraper extracts metadata (prompt, creator, likes, title)

### Using Mock Data

For development and testing without scraping:

```powershell
python scraper.py
```

## Project Structure

```
ai_image_tagger_prototype/
├── app.py                 # Flask web application
├── database.py            # Database models and operations
├── scraper.py            # Image scraper (with mock data)
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
├── data/                 # Database storage (created automatically)
├── static/
│   ├── css/
│   │   └── style.css     # Application styles
│   └── js/
│       ├── main.js       # Common JavaScript
│       ├── tagger.js     # Tagging interface logic
│       └── dashboard.js  # Dashboard logic
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Home page
    ├── tag.html          # Tagging interface
    ├── dashboard.html    # Statistics dashboard
    └── about.html        # About page
```

## How It Works

### Pipeline

1. **Scraping**: Images are collected from Sora's explore page
2. **Filtering**: System identifies images likely containing people based on tags/prompts
3. **Distribution**: Images are randomly distributed to users who haven't seen them
4. **Tagging**: Users review images and tag observed biases
5. **Lifecycle Management**:
   - Each image tracked for unique viewers
   - After 5 views with no bias tags → deleted
   - Images with bias tags → kept for additional review
6. **Analysis**: Statistics aggregated and displayed on dashboard

### Database Schema

- **images**: Stores image data, view counts, and status
- **bias_tags**: Records user-submitted bias observations
- **user_sessions**: Tracks unique users
- **image_views**: Maps which users viewed which images

## Educational Purpose

This tool is designed to:
- Demonstrate how AI bias manifests in image generation
- Educate users about different types of bias
- Create awareness about the importance of diverse training data
- Generate datasets for future bias detection research

## API Endpoints

- `GET /api/next-image` - Get next unviewed image for current user
- `POST /api/submit-tags` - Submit bias tags for an image
- `POST /api/skip-image` - Skip image without tagging
- `GET /api/statistics` - Get aggregated statistics
- `POST /api/load-mock-data` - Load mock data for testing

## Contributing

This is a prototype/educational tool. Suggestions for improvement:
- Enhanced scraper with better people detection
- Machine learning model for automatic bias pre-detection
- More granular bias categories
- Multi-language support
- Export functionality for research data

## Important Notes

- This is a **prototype** for educational purposes
- Mock data is used by default for development
- Real scraping may require authentication and adherence to Sora's terms of service
- The tool highlights bias patterns but should not be considered a definitive measure
- User contributions are anonymous (session-based only)

## License

This is an educational prototype. Please respect OpenAI's terms of service when scraping content.

## Future Enhancements

- [ ] Machine learning integration for bias prediction
- [ ] More detailed bias subcategories
- [ ] Export tagged images for research
- [ ] User accounts and tracking
- [ ] Admin panel for content moderation
- [ ] API for external integrations
- [ ] Mobile-responsive improvements

## Support

For questions or issues, please refer to the About page in the application or the project documentation.

---

**Remember**: This tool is meant to educate and raise awareness. AI bias is a complex issue requiring ongoing research and improvement across the entire AI development lifecycle.
