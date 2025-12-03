# LưuGọn - Backend API

Python FastAPI backend for LưuGọn application.

## Setup

### Prerequisites
- Python 3.9 or higher
- Virtual environment tool (venv or conda)

### Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment variables:
```bash
cp .env.example .env
```

4. Update `.env` with your Supabase credentials and configuration.

5. Run development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /api/compress
Compress text or image and create a shortened link.

**Request (form-data):**
- `type`: 'text' or 'image'
- `content`: Text content (if type='text')
- `file`: Image file (if type='image')

**Response:**
```json
{
  "item_id": "uuid",
  "short_code": "abc123",
  "short_url": "https://luugon.com/abc123",
  "qr_code_url": "https://...",
  "original_size_kb": 100,
  "compressed_size_kb": 50,
  "compression_ratio": 0.5
}
```

### GET /api/item/{short_code}
Retrieve item content by short code.

### GET /api/qr/{short_code}
Get QR code image for a short code.

### GET /health
Health check endpoint.

## Project Structure

- `main.py` - FastAPI application and route handlers
- `config.py` - Configuration settings
- `models.py` - Pydantic models
- `utils.py` - Utility functions
- `qr_generator.py` - QR code generation
- `supabase_service.py` - Supabase database client
- `rate_limiter.py` - Rate limiting
- `requirements.txt` - Python dependencies

## Database Setup

The application expects a Supabase PostgreSQL database with the following table:

```sql
CREATE TABLE items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  short_code VARCHAR(10) UNIQUE NOT NULL,
  type ENUM('text', 'image') NOT NULL,
  original_content TEXT,
  file_path TEXT,
  original_size_kb INTEGER NOT NULL,
  compressed_size_kb INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  expires_at TIMESTAMP WITH TIME ZONE,
  CONSTRAINT check_content_or_file CHECK (
    (type = 'text' AND original_content IS NOT NULL AND file_path IS NULL) OR
    (type = 'image' AND original_content IS NULL AND file_path IS NOT NULL)
  )
);

CREATE INDEX idx_short_code ON items(short_code);
CREATE INDEX idx_created_at ON items(created_at);
```

## Storage Setup

Create two Supabase Storage buckets:
- `luugon-files` - For storing compressed images
- Configure RLS policies for public read access

## Technologies

- FastAPI - Web framework
- Uvicorn - ASGI server
- Pydantic - Data validation
- Pillow - Image processing
- qrcode - QR code generation
- Supabase - Database and file storage
- Python-dotenv - Environment variables
