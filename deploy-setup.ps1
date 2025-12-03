# LưuGọn - Deployment Setup Script (Windows)

Write-Host "🚀 LưuGọn Deployment Setup" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green

# Check if .env exists
if (-Not (Test-Path "backend\.env")) {
    Write-Host "❌ Error: backend\.env not found" -ForegroundColor Red
    Write-Host "📝 Creating .env.production template..." -ForegroundColor Yellow
    Copy-Item "backend\.env.production" "backend\.env"
    Write-Host "⚠️  Please update backend\.env with your Supabase credentials" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ .env found" -ForegroundColor Green

# Validate Python
if (-Not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python is not installed" -ForegroundColor Red
    exit 1
}

$pythonVersion = python --version
Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green

# Validate Node
if (-Not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js is not installed" -ForegroundColor Red
    exit 1
}

$nodeVersion = node --version
Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green

# Install dependencies
Write-Host "`n📦 Installing dependencies..." -ForegroundColor Yellow

Push-Location frontend
npm install
Pop-Location

Push-Location backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Pop-Location

Write-Host "✅ Dependencies installed" -ForegroundColor Green

Write-Host "`n🎉 Setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:"
Write-Host "1. Update backend\.env with Supabase credentials"
Write-Host "2. Update frontend\.env.local with API URL"
Write-Host "3. For Vercel: push to GitHub and connect to Vercel"
Write-Host "4. For Railway: push to GitHub and connect to Railway"
Write-Host "`n📖 See DEPLOYMENT_PUBLIC.md for detailed instructions" -ForegroundColor Cyan
