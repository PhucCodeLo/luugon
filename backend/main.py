from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import io
from datetime import datetime, timedelta
import mimetypes

from config import settings
from models import ContentType, CompressRequest, CompressResponse, ErrorResponse
from utils import (
    generate_short_code,
    compress_image,
    calculate_compression_ratio,
    sanitize_text,
)
from qr_generator import generate_qr_code
from supabase_service import supabase_client
from rate_limiter import RateLimiter

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="LưuGọn - Anonymous text and image compression API"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Rate limiter
rate_limiter = RateLimiter(
    max_requests=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_period_seconds
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "LưuGọn API"}

@app.post("/api/compress", response_model=CompressResponse)
async def compress_content(
    request: Request,
    type: str = Form(...),
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    """
    Compress text or image and create a shortened link.
    
    - **type**: 'text' or 'image'
    - **content**: Text content (required if type='text')
    - **file**: Image file (required if type='image')
    """
    
    print(f"DEBUG: /api/compress called with type={type}, content_len={len(content) if content else 0}, file={file.filename if file else None}")
    
    # Rate limiting
    client_id = request.client.host if request.client else "unknown"
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )
    
    try:
        # Validate input
        if type not in ["text", "image"]:
            raise HTTPException(status_code=400, detail="Invalid type. Must be 'text' or 'image'.")
        
        short_code = generate_short_code()
        short_url = f"{settings.base_url}/{short_code}"
        
        if type == "text":
            # Handle text compression
            if not content or not content.strip():
                raise HTTPException(status_code=400, detail="Text content is required.")
            
            if len(content) > settings.max_text_length:
                raise HTTPException(
                    status_code=400,
                    detail=f"Text content exceeds maximum length of {settings.max_text_length} characters."
                )
            
            # Sanitize text
            sanitized_content = sanitize_text(content)
            print(f"DEBUG: Sanitized content OK")
            
            # Calculate sizes
            original_size_kb = len(content.encode()) // 1024
            compressed_size_kb = len(sanitized_content.encode()) // 1024
            print(f"DEBUG: Sizes calculated: {original_size_kb}KB -> {compressed_size_kb}KB")
            
            # Generate QR code
            qr_data, qr_content_type = generate_qr_code(short_url)
            print(f"DEBUG: QR code generated")
            qr_file_path = f"qr/{short_code}.png"
            try:
                qr_url = await supabase_client.upload_file(qr_file_path, qr_data, qr_content_type)
                print(f"DEBUG: QR uploaded to {qr_url}")
            except Exception as e:
                print(f"DEBUG: QR upload failed: {e}")
                qr_url = None  # Skip QR for now
            
            # Store in database
            print(f"DEBUG: About to create item in database...")
            item = await supabase_client.create_item(
                short_code=short_code,
                content_type=ContentType.TEXT,
                original_content=sanitized_content,
                original_size_kb=original_size_kb,
                compressed_size_kb=compressed_size_kb,
            )
            print(f"DEBUG: Item created successfully: {item.id}")
            
            compression_ratio = calculate_compression_ratio(original_size_kb, compressed_size_kb)
            
            return CompressResponse(
                item_id=item.id,
                short_code=short_code,
                short_url=short_url,
                qr_code_url=qr_url,
                original_size_kb=original_size_kb,
                compressed_size_kb=compressed_size_kb,
                compression_ratio=compression_ratio,
            )
        
        elif type == "image":
            # Handle image compression
            if not file:
                raise HTTPException(status_code=400, detail="Image file is required.")
            
            # Validate file type
            if file.content_type not in settings.allowed_image_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid image type. Allowed types: {', '.join(settings.allowed_image_types)}"
                )
            
            # Check file size
            file_size = 0
            file_data = await file.read()
            file_size = len(file_data)
            
            if file_size > settings.max_file_size_mb * 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail=f"File size exceeds maximum of {settings.max_file_size_mb}MB."
                )
            
            # Compress image
            compressed_data, compressed_size_kb = compress_image(file_data)
            original_size_kb = file_size // 1024
            
            # Upload compressed image
            image_file_path = f"images/{short_code}.jpg"
            image_url = await supabase_client.upload_file(
                image_file_path,
                compressed_data,
                "image/jpeg"
            )
            
            # Generate QR code
            qr_data, qr_content_type = generate_qr_code(short_url)
            qr_file_path = f"qr/{short_code}.png"
            qr_url = await supabase_client.upload_file(qr_file_path, qr_data, qr_content_type)
            
            # Store in database
            item = await supabase_client.create_item(
                short_code=short_code,
                content_type=ContentType.IMAGE,
                file_path=image_url,
                original_size_kb=original_size_kb,
                compressed_size_kb=compressed_size_kb,
            )
            
            compression_ratio = calculate_compression_ratio(original_size_kb, compressed_size_kb)
            
            return CompressResponse(
                item_id=item.id,
                short_code=short_code,
                short_url=short_url,
                qr_code_url=qr_url,
                original_size_kb=original_size_kb,
                compressed_size_kb=compressed_size_kb,
                compression_ratio=compression_ratio,
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/item/{short_code}")
async def get_item(short_code: str):
    """Retrieve item content by short code."""
    
    try:
        item = await supabase_client.get_item_by_short_code(short_code)
        
        if not item:
            raise HTTPException(status_code=404, detail="Item not found.")
        
        # Check if expired
        if item.expires_at and datetime.fromisoformat(item.expires_at) < datetime.utcnow():
            raise HTTPException(status_code=410, detail="Item has expired.")
        
        if item.content_type == ContentType.TEXT:
            return {
                "type": "text",
                "content": item.original_content,
            }
        elif item.content_type == ContentType.IMAGE:
            # Redirect to file or return file_path
            return {
                "type": "image",
                "file_path": item.file_path,
            }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/qr/{short_code}")
async def get_qr_code(short_code: str):
    """Get QR code image for a short code."""
    
    try:
        item = await supabase_client.get_item_by_short_code(short_code)
        
        if not item:
            raise HTTPException(status_code=404, detail="Item not found.")
        
        # Generate QR code for the full URL
        full_url = f"{settings.base_url}/{short_code}"
        qr_data, _ = generate_qr_code(full_url)
        
        return FileResponse(
            io.BytesIO(qr_data),
            media_type="image/png",
            filename=f"qr-{short_code}.png"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
