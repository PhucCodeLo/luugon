#!/bin/bash
# LưuGọn - Deployment Setup Script

echo "🚀 LưuGọn Deployment Setup"
echo "============================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}❌ Error: backend/.env not found${NC}"
    echo "📝 Creating .env.production template..."
    cp backend/.env.production backend/.env
    echo -e "${YELLOW}⚠️  Please update backend/.env with your Supabase credentials${NC}"
    exit 1
fi

echo -e "${GREEN}✅ .env found${NC}"

# Validate Python
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python found$(python --version)${NC}"

# Validate Node
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Node.js found: $(node --version)${NC}"

# Install dependencies
echo -e "\n${YELLOW}📦 Installing dependencies...${NC}"

cd frontend
npm install
cd ..

cd backend
python -m venv venv
source venv/bin/activate 2>/dev/null || venv\Scripts\activate
pip install -r requirements.txt
cd ..

echo -e "${GREEN}✅ Dependencies installed${NC}"

echo -e "\n${GREEN}🎉 Setup complete!${NC}"
echo -e "\nNext steps:"
echo "1. Update backend/.env with Supabase credentials"
echo "2. Update frontend/.env.local with API URL"
echo "3. For Vercel: push to GitHub and connect to Vercel"
echo "4. For Railway: push to GitHub and connect to Railway"
echo -e "\n📖 See DEPLOYMENT_PUBLIC.md for detailed instructions"
