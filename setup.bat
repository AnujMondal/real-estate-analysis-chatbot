@echo off
REM Real Estate Chatbot - Automated Setup Script for Windows
REM This script sets up both backend and frontend automatically

echo.
echo 🏠 Real Estate Analysis Chatbot - Automated Setup
echo ==================================================
echo.

REM Check prerequisites
echo 📋 Checking prerequisites...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo ✅ Python found

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16 or higher.
    pause
    exit /b 1
)
echo ✅ Node.js found

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is not installed. Please install npm.
    pause
    exit /b 1
)
echo ✅ npm found

echo.
echo 🔧 Setting up Backend...
echo ========================
echo.

REM Navigate to backend
cd backend

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Copy environment file
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo ⚠️  Please update .env with your configuration
)

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Generate sample data
echo Generating sample data...
python generate_sample_data.py

REM Move sample data to data directory
if exist real_estate_data.xlsx (
    if not exist data mkdir data
    move real_estate_data.xlsx data\
    echo ✅ Sample data created in data\real_estate_data.xlsx
)

echo.
echo ✅ Backend setup complete!
echo.

REM Navigate back to root
cd ..

echo 🎨 Setting up Frontend...
echo =========================
echo.

REM Navigate to frontend
cd frontend

REM Install dependencies
echo Installing Node.js dependencies...
call npm install

REM Copy environment file
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
)

echo.
echo ✅ Frontend setup complete!
echo.

REM Navigate back to root
cd ..

echo ==================================================
echo 🎉 Setup Complete!
echo ==================================================
echo.
echo 📝 Next Steps:
echo.
echo 1. Start Backend Server:
echo    cd backend
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
echo 2. Start Frontend Server (in a new terminal):
echo    cd frontend
echo    npm start
echo.
echo 3. Open your browser to: http://localhost:3000
echo.
echo 📊 Sample data has been generated in: backend\data\real_estate_data.xlsx
echo.
echo 💡 Try these sample queries:
echo    • 'Analyze Wakad'
echo    • 'Compare Aundh and Kharadi demand trends'
echo    • 'Show price growth for Hinjewadi'
echo.
echo 📖 For more information, see README.md
echo.
echo 🚀 Happy analyzing!
echo.
pause
