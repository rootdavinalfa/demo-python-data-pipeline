#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating venv..."
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e packages/shared

if [ ! -f ".env" ]; then
    echo "Copying .env.example to .env..."
    cp .env.example .env
fi

echo ""
echo "Setup complete!"
echo "Run: source venv/bin/activate && ./run.sh"