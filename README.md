# Family Trip Spending Tracker

A web application to track daily expenses during family trips with interactive charts and sharing capabilities.

## Features

- 📊 Interactive charts (Plotly)
- 💰 Daily expense tracking
- 🏷️ Category-based organization
- 📤 CSV export functionality
- 📱 Mobile-responsive design
- 🔗 Easy sharing with family

## Deployment Options

### Option 1: Render (Free - Recommended)

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Create a new Web Service
4. Connect your GitHub repository
5. Deploy automatically

### Option 2: Quick Test with ngrok

```bash
# Install ngrok
brew install ngrok  # macOS
# or download from ngrok.com

# Run your Flask app
python app.py

# In another terminal
ngrok http 5001
```

### Option 3: Other Platforms

- **Heroku**: Classic platform (paid)
- **Railway**: Modern alternative
- **Vercel**: Good for static sites
- **PythonAnywhere**: Python-specific hosting

## Local Development

```bash
# Clone and setup
git clone <your-repo>
cd family-spending-tracker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

## Usage

1. Add daily expenses with description, amount, category, and location
2. View real-time charts and statistics
3. Export data as CSV
4. Share the URL with family members

## Categories

- 🍽️ Food & Dining
- 🚗 Transportation
- 🏨 Accommodation
- 🎢 Entertainment
- 🛍️ Shopping
- 📝 Other