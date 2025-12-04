#!/bin/bash

echo "================================"
echo "Anshul Portfolio Backend Setup"
echo "Minimal Version for Vercel"
echo "================================"
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org/"
    exit 1
fi

echo "[1/6] Python detected"
python3 --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[2/6] Creating virtual environment..."
    python3 -m venv venv
else
    echo "[2/6] Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "[3/6] Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "[4/6] Installing dependencies..."
pip install -r requirements.txt
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "[5/6] Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "[IMPORTANT] Please edit .env file and add your GOOGLE_API_KEY"
    echo "Get your API key from: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Press Enter after you've added your API key..."
else
    echo "[5/6] .env file already exists"
fi
echo ""

# Start the server
echo "[6/6] Starting FastAPI server..."
echo ""
echo "================================"
echo "Server will start at:"
echo "http://localhost:8000"
echo ""
echo "Interactive docs:"
echo "http://localhost:8000/docs"
echo "================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
