@echo off
REM LưuGọn Quick Start Script for Windows

setlocal enabledelayedexpansion

echo 🚀 LưuGọn Quick Start Setup
echo ============================
echo.

REM Check prerequisites
echo ✓ Checking prerequisites...

where node >nul 2>nul
if !errorlevel! neq 0 (
    echo ✗ Node.js is not installed. Please install it first.
    exit /b 1
)

where python >nul 2>nul
if !errorlevel! neq 0 (
    echo ✗ Python is not installed. Please install it first.
    exit /b 1
)

echo ✓ Prerequisites OK
echo.

REM Frontend setup
echo 📦 Setting up frontend...
cd frontend

if not exist "node_modules" (
    call npm install
)

if not exist ".env.local" (
    copy .env.local.example .env.local
    echo ⚠ Created .env.local - please update with your API URL
)

echo ✓ Frontend setup complete
echo.
cd ..

REM Backend setup
echo 🐍 Setting up backend...
cd backend

if not exist "venv" (
    python -m venv venv
)

call venv\Scripts\activate.bat

pip install -q -r requirements.txt

if not exist ".env" (
    copy .env.example .env
    echo ⚠ Created .env - please update with your Supabase credentials
)

call venv\Scripts\deactivate.bat

echo ✓ Backend setup complete
echo.
cd ..

echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Update frontend\.env.local with your backend URL
echo 2. Update backend\.env with your Supabase credentials
echo 3. Run database initialization script
echo.
echo To start development:
echo   Terminal 1: cd backend ^& venv\Scripts\activate.bat ^& python -m uvicorn main:app --reload
echo   Terminal 2: cd frontend ^& npm run dev
echo.
echo Then visit: http://localhost:3000
