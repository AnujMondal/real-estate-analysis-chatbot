#!/bin/bash

# Real Estate Chatbot - Automated Setup Script
# This script sets up both backend and frontend automatically

set -e  # Exit on error

echo "🏠 Real Estate Analysis Chatbot - Automated Setup"
echo "=================================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi
echo "✅ npm found: $(npm --version)"

echo ""
echo "🔧 Setting up Backend..."
echo "========================"

# Navigate to backend
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Generate sample data
echo "Generating sample data..."
python generate_sample_data.py

# Move sample data to data directory
if [ -f real_estate_data.xlsx ]; then
    mkdir -p data
    mv real_estate_data.xlsx data/
    echo "✅ Sample data created in data/real_estate_data.xlsx"
fi

echo ""
echo "✅ Backend setup complete!"
echo ""

# Navigate back to root
cd ..

echo "🎨 Setting up Frontend..."
echo "========================="

# Navigate to frontend
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo ""
echo "✅ Frontend setup complete!"
echo ""

# Navigate back to root
cd ..

echo "=================================================="
echo "🎉 Setup Complete!"
echo "=================================================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Start Backend Server:"
echo "   cd backend"
echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "   python manage.py runserver"
echo ""
echo "2. Start Frontend Server (in a new terminal):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Open your browser to: http://localhost:3000"
echo ""
echo "📊 Sample data has been generated in: backend/data/real_estate_data.xlsx"
echo ""
echo "💡 Try these sample queries:"
echo "   • 'Analyze Wakad'"
echo "   • 'Compare Aundh and Kharadi demand trends'"
echo "   • 'Show price growth for Hinjewadi'"
echo ""
echo "📖 For more information, see README.md"
echo ""
echo "🚀 Happy analyzing!"
