# LưuGọn - Anonymous Text and Image Compression Sharing

LưuGọn is an anonymous web application that allows users to compress text or images into shortened links or QR codes for easy sharing, similar to Google Drive but without requiring login.

## Features

✨ **Anonymous Access** - No login or account creation required
⚡ **Fast Compression** - Compress and share in seconds  
📱 **QR Code Support** - Generate QR codes for easy mobile sharing
🔒 **Privacy First** - End-to-end encryption support (optional)
🎨 **Dark Mode** - Modern UI with dark mode by default
📊 **Compression Stats** - View original vs compressed size
🌍 **Responsive** - Works perfectly on desktop, tablet, and mobile

## Tech Stack

### Frontend
- Next.js 14 with React 18
- TypeScript
- Tailwind CSS
- Shadcn/UI components
- Zustand for state management
- Zod for validation

### Backend
- Python with FastAPI
- Pydantic for data validation
- Pillow for image compression
- qrcode for QR generation
- PostgreSQL (via Supabase)
- Supabase Storage

## Project Structure

```
luugon/
├── frontend/               # Next.js React application
│   ├── app/               # App router pages
│   ├── components/        # React components
│   ├── lib/              # Utilities and API client
│   ├── public/           # Static assets
│   └── package.json
│
├── backend/               # FastAPI Python backend
│   ├── main.py           # Main FastAPI application
│   ├── config.py         # Configuration
│   ├── models.py         # Pydantic models
│   ├── utils.py          # Utility functions
│   ├── qr_generator.py   # QR code generation
│   ├── supabase_service.py  # Database client
│   ├── rate_limiter.py   # Rate limiting
│   └── requirements.txt
│
└── README.md             # This file
```

## Database Schema

### items table
```sql
CREATE TABLE items (
  id UUID PRIMARY KEY,
  short_code VARCHAR(10) UNIQUE,
  type ENUM('text', 'image'),
  original_content TEXT,
  file_path TEXT,
  original_size_kb INTEGER,
  compressed_size_kb INTEGER,
  created_at TIMESTAMP WITH TIME ZONE,
  expires_at TIMESTAMP WITH TIME ZONE
);
```

## API Endpoints

### POST /api/compress
Compress text or image and create shortened link.

### GET /api/item/{short_code}
Retrieve item content by short code.

### GET /api/qr/{short_code}
Get QR code image for a short code.

## Getting Started

### Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
# Update .env.local with your backend URL
npm run dev
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Update .env with your Supabase credentials
uvicorn main:app --reload
```

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-public-anon-key
BASE_URL=https://luugon.com
```

## Security Features

- ✅ Input validation with Pydantic and Zod
- ✅ XSS protection and HTML sanitization
- ✅ Rate limiting (100 requests per minute)
- ✅ File type validation
- ✅ File size limits (10MB max)
- ✅ CORS configuration
- ✅ Content type checking
- ✅ SQL injection prevention (via Pydantic)

## Edge Cases Handled

- Empty input validation
- Invalid file format rejection
- File size limit enforcement
- Network error handling
- 404 for non-existent links
- Expired link handling
- Compression ratio calculation
- Proper error messages

## Deployment

### Quick Start (Recommended)
- **Frontend:** Deploy to Vercel (free, automatic CI/CD)
- **Backend:** Deploy to Railway ($5/month with free credits)
- **Database:** Supabase (free tier sufficient)
- **Domain:** Namecheap (~$10-15/year)

For detailed deployment instructions, see [DEPLOYMENT_PUBLIC.md](./DEPLOYMENT_PUBLIC.md)

### Local Development
```bash
# Frontend
cd frontend && npm run dev

# Backend (in another terminal)
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn main:app --reload
```

## 🚀 Live Demo
- 🔗 Coming soon!

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
