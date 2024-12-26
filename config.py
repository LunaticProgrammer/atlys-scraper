from pydantic import BaseModel
from typing import Optional

class ScrapingConfig(BaseModel):
    page_limit: Optional[int] = None
    proxy: Optional[str] = None
    base_url: str
    auth_token: Optional[str] = None
    retry_attempts: int = 3
    retry_delay: int = 5