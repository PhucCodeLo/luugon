#!/bin/bash

# LưuGọn Quick Start Script
# This script helps set up the LưuGọn application locally

set -e

echo "🚀 LưuGọn Quick Start Setup"
echo "============================\n"

# Check prerequisites
echo "✓ Checking prerequisites..."

if ! command -v node &> /dev/null; then
    echo "✗ Node.js is not installed. Please install it first."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed. Please install it first."
    exit 1
fi

echo "✓ Prerequisites OK\n"

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    npm install
fi

if [ ! -f ".env.local" ]; then
    cp .env.local.example .env.local
    echo "⚠ Created .env.local - please update with your API URL"
fi

echo "✓ Frontend setup complete\n"
cd ..

# Backend setup
echo "🐍 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠ Created .env - please update with your Supabase credentials"
fi

deactivate

echo "✓ Backend setup complete\n"
cd ..

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update frontend/.env.local with your backend URL"
echo "2. Update backend/.env with your Supabase credentials"
echo "3. Run database initialization script"
echo ""
echo "To start development:"
echo "  Terminal 1: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "  Terminal 2: cd frontend && npm run dev"
echo ""
echo "Then visit: http://localhost:3000"
