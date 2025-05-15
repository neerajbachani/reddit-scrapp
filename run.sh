#!/bin/bash

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "Python could not be found. Please install Python 3.8 or later."
    exit 1
fi

# Check for required environment variables
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Copy .env.template to .env and add your API keys."
    if [ -f ".env.template" ]; then
        cp .env.template .env
        echo "Created .env from template. Please edit it with your API keys."
        exit 1
    fi
fi

# Run the scraper
echo "Starting Cronlytic Reddit Scraper..."
python main.py

# Check exit status
if [ $? -eq 0 ]; then
    echo "✅ Scraper completed successfully."
else
    echo "❌ Scraper failed. Check logs for details."
    exit 1
fi