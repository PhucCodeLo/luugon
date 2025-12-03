# LưuGọn - Setup & Deployment Guide

## Local Development Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Supabase account with project
- Git

### Step 1: Clone and Install

```bash
# Clone repository
git clone <repository-url>
cd luugon

# Frontend setup
cd frontend
npm install
cp .env.local.example .env.local
cd ..

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
cd ..
```

### Step 2: Configure Supabase

1. Create a new project on Supabase
2. Go to SQL Editor and run the SQL from `backend/init_db.sql`
3. Create two storage buckets:
   - `luugon-files` - For images and QR codes
   - Set public read access for both

### Step 3: Environment Setup

**frontend/.env.local:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**backend/.env:**
```
SUPABASE_URL=https://mgppqllknjhcltnnkekk.supabase.co
SUPABASE_KEY=sb_publishable_sdBZc-MleZO0vgNJK_WDDg_VnQLX-V2
BASE_URL=http://localhost:3000
```

### Step 4: Run Development Servers

Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000`

## Docker Deployment

### Build and Run with Docker Compose

```bash
cp .env.example .env
docker-compose up --build
```

## Production Deployment

### Frontend (Vercel)

```bash
# Login to Vercel
vercel login

# Deploy
vercel
```

Environment variables in Vercel dashboard:
```
NEXT_PUBLIC_API_URL=https://api.luugon.com
```

### Backend (Heroku/Railway/Render)

1. Create account on chosen platform
2. Create new application
3. Set environment variables:
   - SUPABASE_URL
   - SUPABASE_KEY
   - BASE_URL=https://api.luugon.com
   - CORS_ORIGINS=https://luugon.com,https://www.luugon.com

4. Deploy:
   ```bash
   # Heroku
   heroku login
   heroku create luugon-api
   git push heroku main
   ```

## Database Migrations

To run migrations on production:

```bash
# Connect to Supabase database
psql postgresql://username:password@host:port/database

# Run init_db.sql
\i backend/init_db.sql
```

## Monitoring & Maintenance

### Cleanup Expired Items

```python
# Run periodically (e.g., daily cron job)
from supabase_service import supabase_client
from datetime import datetime

async def cleanup_expired():
    supabase_client.db.delete().lt('expires_at', datetime.utcnow().isoformat()).execute()
```

### Performance Monitoring

- Monitor Supabase database usage
- Check API response times
- Monitor storage usage
- Set up alerts for rate limit abuse

## Troubleshooting

### CORS Errors
- Check `CORS_ORIGINS` in backend .env
- Verify frontend URL is in the list

### Database Connection Issues
- Verify Supabase credentials
- Check network connectivity
- Ensure database tables are created

### File Upload Issues
- Check storage bucket permissions
- Verify file size limits
- Check allowed MIME types

## Support

For issues and questions, open an issue on GitHub.
