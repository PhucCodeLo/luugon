from supabase import create_client
from config import settings
from uuid import uuid4
from datetime import datetime
from typing import Optional
from models import ContentType, ItemResponse

class SupabaseClient:
    def __init__(self):
        self.client = create_client(settings.supabase_url, settings.supabase_key)
        self.storage = self.client.storage
        self.db = self.client.table('items')

    def create_item(
        self,
        short_code: str,
        content_type: ContentType,
        original_content: Optional[str] = None,
        file_path: Optional[str] = None,
        original_size_kb: int = 0,
        compressed_size_kb: int = 0,
        expires_at: Optional[datetime] = None,
    ) -> ItemResponse:
        item_id = uuid4()

        data = {
            "id": str(item_id),
            "short_code": short_code,
            "content_type": content_type.value,
            "original_content": original_content,
            "file_path": file_path,
            "original_size_kb": original_size_kb,
            "compressed_size_kb": compressed_size_kb,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expires_at.isoformat() if expires_at else None,
        }

        try:
            response = self.db.insert(data).execute()

            if not response.data:
                raise Exception("Failed to create item")

            return ItemResponse(**response.data[0])

        except Exception as e:
            print(f"DEBUG Insert error: {e}")
            print(f"DEBUG Data: {data}")
            raise

    def get_item_by_short_code(self, short_code: str) -> Optional[ItemResponse]:
        response = self.db.select("*").eq("short_code", short_code).execute()

        if not response.data:
            return None

        return ItemResponse(**response.data[0])

    def upload_file(self, file_path: str, file_data: bytes, content_type: str) -> str:
        """Upload file to Supabase storage."""
        result = (
            self.storage
            .from_("luugon-files")
            .upload(
                file_path,
                file_data,
                {"contentType": content_type},
            )
        )

        # result is dict-like; check for errors
        if "error" in result and result["error"] is not None:
            raise Exception(f"Upload failed: {result['error']}")

        return f"{settings.supabase_url}/storage/v1/object/public/luugon-files/{file_path}"

    def delete_item(self, item_id: str) -> bool:
        self.db.delete().eq("id", item_id).execute()
        return True


# Global instance
supabase_client = SupabaseClient()
