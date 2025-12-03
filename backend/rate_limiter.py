from fastapi import HTTPException
from typing import Dict
from datetime import datetime, timedelta
import time

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if a client is allowed to make a request."""
        now = time.time()
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Remove old requests outside the window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        
        # Check if limit exceeded
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True
    
    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests for a client."""
        now = time.time()
        
        if client_id not in self.requests:
            return self.max_requests
        
        # Remove old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        
        return max(0, self.max_requests - len(self.requests[client_id]))
