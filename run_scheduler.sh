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

# Run the scheduler
echo "Starting Cronlytic Reddit Scheduler..."
echo "Press Ctrl+C to stop the scheduler."
python scheduler/daily_scheduler.py

# This code will only run if the scheduler exits normally
echo "Scheduler stopped."