#!/bin/bash

# Local setup and testing script for Crypto Scraper API

set -e

echo "🔧 Crypto Scraper - Local Setup Script"
echo "========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher"
    exit 1
fi

python_version=$(python3 --version)
echo "✅ Found: $python_version"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Activated"

echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt > /dev/null
echo "✅ Dependencies installed"

echo ""
echo "📋 Checking configuration..."
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from .env.local..."
    cp .env.local .env
    echo "✅ .env created (you can customize it if needed)"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🗄️  Initializing database..."
python3 << 'EOF'
from api import init_db
init_db()
print("✅ Database initialized")
EOF

echo ""
echo "🚀 Starting API server..."
echo "========================================="
echo ""
echo "Server will be available at: http://localhost:3000"
echo ""
echo "API Endpoints:"
echo "  • GET  http://localhost:3000/api/health"
echo "  • GET  http://localhost:3000/api/results"
echo "  • GET  http://localhost:3000/api/results/<account>"
echo "  • POST http://localhost:3000/api/scrape"
echo "  • GET  http://localhost:3000/api/stats"
echo "  • GET  http://localhost:3000/api/logs"
echo ""
echo "Test commands:"
echo "  curl http://localhost:3000/api/health"
echo "  curl http://localhost:3000/api/stats"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================="
echo ""

python3 api.py
