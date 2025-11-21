#!/bin/bash

# My Work Bot Setup Script
# This script helps you set up the bot quickly

set -e

echo "=================================================="
echo "🤖 My Work Bot Setup"
echo "=================================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  No .env file found"
    echo "📝 Creating .env from env.example..."
    cp env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API tokens:"
    echo "   - SLACK_BOT_TOKEN"
    echo "   - SLACK_SIGNING_SECRET"
    echo "   - SLACK_APP_TOKEN"
    echo "   - GITHUB_TOKEN"
    echo "   - JIRA_API_TOKEN"
    echo ""
    echo "📖 See QUICKSTART.md for detailed setup instructions"
else
    echo "✅ .env file already exists"
fi
echo ""

echo "=================================================="
echo "✨ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API tokens (if not done)"
echo "  2. Run: source venv/bin/activate"
echo "  3. Run: python run.py"
echo ""
echo "📖 For detailed instructions, see:"
echo "   - QUICKSTART.md (5-minute guide)"
echo "   - README.md (complete documentation)"
echo ""
echo "Happy coding! 🚀"

