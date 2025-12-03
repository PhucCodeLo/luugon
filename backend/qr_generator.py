import qrcode
import io
from typing import Tuple

def generate_qr_code(data: str) -> Tuple[bytes, str]:
    """
    Generate QR code for the given data.
    
    Args:
        data: Data to encode in QR code (URL, text, etc.)
    
    Returns:
        Tuple of (image_bytes, content_type)
    """
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes.getvalue(), 'image/png'
    except Exception as e:
        raise ValueError(f"Failed to generate QR code: {str(e)}")
