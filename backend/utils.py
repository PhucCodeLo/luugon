import string
import random
import hashlib
import io
from PIL import Image
from typing import Tuple

def generate_short_code(length: int = 6) -> str:
    """Generate a random short code for URL shortening."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def compress_image(image_data: bytes, quality: int = 85, max_width: int = 1920, max_height: int = 1920) -> Tuple[bytes, int]:
    """
    Compress an image using Pillow.
    
    Args:
        image_data: Raw image bytes
        quality: JPEG quality (1-100)
        max_width: Maximum width
        max_height: Maximum height
    
    Returns:
        Tuple of (compressed_bytes, new_size_kb)
    """
    try:
        # Open image from bytes
        img = Image.open(io.BytesIO(image_data))
        
        # Convert RGBA to RGB for JPEG
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Resize if necessary
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Save compressed
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        compressed_data = output.getvalue()
        
        return compressed_data, len(compressed_data) // 1024
    except Exception as e:
        raise ValueError(f"Failed to compress image: {str(e)}")

def calculate_compression_ratio(original_size: int, compressed_size: int) -> float:
    """Calculate compression ratio (compressed / original)."""
    if original_size == 0:
        return 0.0
    return compressed_size / original_size

def sanitize_text(text: str) -> str:
    """Sanitize text to prevent XSS attacks."""
    # Remove potential script tags and dangerous content
    dangerous_chars = ['<', '>', '"', "'"]
    sanitized = text
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    return sanitized.strip()

def hash_text(text: str) -> str:
    """Create a hash of text for deduplication."""
    return hashlib.sha256(text.encode()).hexdigest()
