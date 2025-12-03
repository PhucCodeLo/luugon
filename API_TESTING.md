# LưuGọn - API Testing Guide

## 📝 Testing the API Endpoints

### Prerequisites
- Backend running on `http://localhost:8000`
- Frontend running on `http://localhost:3000` (optional for testing)

### Tools
- Postman
- cURL (command line)
- Thunder Client (VS Code)
- Insomnia

---

## 🧪 Test Cases

### 1. Health Check

**Request:**
```bash
curl -X GET http://localhost:8000/health
```

**Expected Response (200):**
```json
{
  "status": "ok",
  "service": "LưuGọn API"
}
```

---

### 2. Compress Text

**Request:**
```bash
curl -X POST http://localhost:8000/api/compress \
  -F "type=text" \
  -F "content=Hello, this is a test message for LưuGọn!"
```

**Expected Response (200):**
```json
{
  "item_id": "550e8400-e29b-41d4-a716-446655440000",
  "short_code": "abc123",
  "short_url": "https://luugon.com/abc123",
  "qr_code_url": "https://your-supabase.supabase.co/storage/v1/object/public/luugon-files/qr/abc123.png",
  "original_size_kb": 1,
  "compressed_size_kb": 1,
  "compression_ratio": 1.0
}
```

---

### 3. Compress Image

**Request:**
```bash
curl -X POST http://localhost:8000/api/compress \
  -F "type=image" \
  -F "file=@path/to/image.jpg"
```

**Expected Response (200):**
```json
{
  "item_id": "550e8400-e29b-41d4-a716-446655440001",
  "short_code": "xyz789",
  "short_url": "https://luugon.com/xyz789",
  "qr_code_url": "https://your-supabase.supabase.co/storage/v1/object/public/luugon-files/qr/xyz789.png",
  "original_size_kb": 2048,
  "compressed_size_kb": 512,
  "compression_ratio": 0.25
}
```

---

### 4. Retrieve Text Item

**Request:**
```bash
curl -X GET http://localhost:8000/api/item/abc123
```

**Expected Response (200):**
```json
{
  "type": "text",
  "content": "Hello, this is a test message for LưuGọn!"
}
```

---

### 5. Retrieve Image Item

**Request:**
```bash
curl -X GET http://localhost:8000/api/item/xyz789
```

**Expected Response (200):**
```json
{
  "type": "image",
  "file_path": "https://your-supabase.supabase.co/storage/v1/object/public/luugon-files/images/xyz789.jpg"
}
```

---

### 6. Get QR Code

**Request:**
```bash
curl -X GET http://localhost:8000/api/qr/abc123 -o qr.png
```

**Expected Response (200):**
- PNG image file

---

## ❌ Error Cases

### Empty Text Input

**Request:**
```bash
curl -X POST http://localhost:8000/api/compress \
  -F "type=text" \
  -F "content="
```

**Expected Response (400):**
```json
{
  "detail": "Text content is required."
}
```

---

### Invalid File Type

**Request:**
```bash
curl -X POST http://localhost:8000/api/compress \
  -F "type=image" \
  -F "file=@document.pdf"
```

**Expected Response (400):**
```json
{
  "detail": "Invalid image type. Allowed types: image/jpeg, image/png, image/webp, image/gif"
}
```

---

### File Too Large

**Request:**
```bash
curl -X POST http://localhost:8000/api/compress \
  -F "type=image" \
  -F "file=@huge-image.jpg"  # > 10MB
```

**Expected Response (400):**
```json
{
  "detail": "File size exceeds maximum of 10MB."
}
```

---

### Item Not Found

**Request:**
```bash
curl -X GET http://localhost:8000/api/item/nonexistent
```

**Expected Response (404):**
```json
{
  "detail": "Item not found."
}
```

---

### Rate Limit Exceeded

**Request (100+ requests in 60 seconds):**
```bash
for i in {1..101}; do
  curl -X GET http://localhost:8000/health
done
```

**Expected Response (429) after limit:**
```json
{
  "detail": "Too many requests. Please try again later."
}
```

---

## 🧬 Postman Collection

Import this into Postman:

```json
{
  "info": {
    "name": "LưuGọn API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "{{baseUrl}}/health"
      }
    },
    {
      "name": "Compress Text",
      "request": {
        "method": "POST",
        "url": "{{baseUrl}}/api/compress",
        "body": {
          "mode": "formdata",
          "formdata": [
            {
              "key": "type",
              "value": "text"
            },
            {
              "key": "content",
              "value": "Hello world"
            }
          ]
        }
      }
    },
    {
      "name": "Get Item",
      "request": {
        "method": "GET",
        "url": "{{baseUrl}}/api/item/{{shortCode}}"
      }
    },
    {
      "name": "Get QR Code",
      "request": {
        "method": "GET",
        "url": "{{baseUrl}}/api/qr/{{shortCode}}"
      }
    }
  ],
  "variable": [
    {
      "key": "baseUrl",
      "value": "http://localhost:8000"
    },
    {
      "key": "shortCode",
      "value": "abc123"
    }
  ]
}
```

---

## 🔍 Frontend Testing

### Test Text Compression Flow

1. Visit `http://localhost:3000`
2. Click "📝 Văn bản"
3. Enter text in the textarea
4. Click "Nén & Tạo Link"
5. Verify:
   - Short URL is displayed
   - QR code is shown
   - Copy button works
   - Download button works

### Test Image Compression Flow

1. Visit `http://localhost:3000`
2. Click "🖼️ Hình ảnh"
3. Select an image file
4. Click "Nén & Tạo Link"
5. Verify:
   - Compression ratio is calculated
   - QR code is generated
   - File sizes are displayed

### Test Item Retrieval

1. After compression, copy the short URL
2. Open in new tab
3. Verify content is displayed correctly

### Test Error Cases

1. Try submitting empty text
2. Try uploading non-image file
3. Try uploading file > 10MB
4. Try accessing non-existent short code

---

## 📊 Performance Testing

### Load Test Example (using Apache Bench)

```bash
# 100 requests with 10 concurrent connections
ab -n 100 -c 10 http://localhost:8000/health

# POST request (requires file)
ab -n 100 -c 10 -p data.txt -T application/x-www-form-urlencoded \
  http://localhost:8000/api/compress
```

### Using k6 for load testing

```javascript
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m30s', target: 10 },
    { duration: '20s', target: 0 },
  ],
};

export default function () {
  let response = http.get('http://localhost:8000/health');
  check(response, {
    'status is 200': (r) => r.status === 200,
  });
}
```

---

## 🔐 Security Testing

### SQL Injection Test

```bash
curl -X POST http://localhost:8000/api/compress \
  -F "type=text" \
  -F "content='; DROP TABLE items; --"
```

Expected: Content is safely stored as text

### XSS Test

```bash
curl -X POST http://localhost:8000/api/compress \
  -F "type=text" \
  -F "content=<script>alert('xss')</script>"
```

Expected: Script tags are sanitized

### Rate Limit Test

```bash
for i in {1..150}; do
  curl http://localhost:8000/health
done
```

Expected: 429 responses after 100 requests in 60 seconds

---

## 📈 Debugging

### Enable Debug Logging

In `backend/.env`:
```
DEBUG=True
```

### Check Supabase Connection

```python
# In backend directory, activate venv and run:
python -c "from supabase_service import supabase_client; print('Connected!')"
```

### Check Database Connection

```sql
-- In Supabase SQL Editor
SELECT * FROM items LIMIT 1;
```

### Check Storage Buckets

```bash
# List storage buckets via Supabase CLI
supabase storage list
```

---

## ✅ Checklist for Production Testing

- [ ] Health check endpoint responds
- [ ] Text compression works
- [ ] Image compression works
- [ ] QR codes are generated
- [ ] Items can be retrieved
- [ ] 404 for missing items
- [ ] Rate limiting works
- [ ] File size limits work
- [ ] Invalid file types rejected
- [ ] XSS sanitization works
- [ ] CORS headers correct
- [ ] Database stores data
- [ ] Storage files created
- [ ] Error messages helpful
- [ ] Response times acceptable

---

**Happy Testing! 🚀**
