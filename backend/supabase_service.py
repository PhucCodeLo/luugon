from supabase import create_client
from config import settings
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from typing import Optional, Dict
from models import ContentType, ItemResponse

class SupabaseClient:
    def __init__(self):
        self.client = create_client(settings.supabase_url, settings.supabase_key)
        self.storage = self.client.storage
        self.db = self.client.table('items')
    
    async def create_item(
        self,
        short_code: str,
        content_type: ContentType,
        original_content: Optional[str] = None,
        file_path: Optional[str] = None,
        original_size_kb: int = 0,
        compressed_size_kb: int = 0,
        expires_at: Optional[datetime] = None,
    ) -> ItemResponse:
        """Create a new item in the database."""
        item_id = uuid4()
        
        data = {
            'id': str(item_id),
            'short_code': short_code,
            'content_type': content_type.value,
            'original_content': original_content,
            'file_path': file_path,
            'original_size_kb': original_size_kb,
            'compressed_size_kb': compressed_size_kb,
            'created_at': datetime.utcnow().isoformat(),
            'expires_at': expires_at.isoformat() if expires_at else None,
        }
        
        try:
            response = self.db.insert(data).execute()
            
            if not response.data:
                raise Exception("Failed to create item in database")
            
            return ItemResponse(**response.data[0])
        except Exception as e:
            print(f"DEBUG: Insert error: {e}")
            print(f"DEBUG: Data: {data}")
            raise
    
    async def get_item_by_short_code(self, short_code: str) -> Optional[ItemResponse]:
        """Get an item by its short code."""
        response = self.db.select('*').eq('short_code', short_code).execute()
        
        if not response.data:
            return None
        
        return ItemResponse(**response.data[0])
    
    async def upload_file(self, file_path: str, file_data: bytes, content_type: str) -> str:
        """Upload a file to Supabase Storage."""
        response = self.storage.from_('luugon-files').upload(
            file_path,
            file_data,
            {
                'contentType': content_type,
            }
        )
        
        # Return public URL
        return f"{settings.supabase_url}/storage/v1/object/public/luugon-files/{file_path}"
    
    async def delete_item(self, item_id: str) -> bool:
        """Delete an item (soft delete or hard delete)."""
        response = self.db.delete().eq('id', item_id).execute()
        return True

# Global instance
supabase_client = SupabaseClient()
