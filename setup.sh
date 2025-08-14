#!/bin/bash

echo "🎤 Setting up AI Interview Note Taker..."
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python version $python_version is too old. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your OpenAI API key"
else
    echo "✅ .env file already exists"
fi

# Create templates directory if it doesn't exist
if [ ! -d "templates" ]; then
    echo "🔧 Creating templates directory..."
    mkdir -p templates
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the application: python app.py"
echo "4. Open http://localhost:5000 in your browser"
echo ""
echo "For more information, see README.md"