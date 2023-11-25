from pydantic import BaseModel
from typing import List, Optional


class AllInitialPost(BaseModel):
    url: str
    url_ext: str
    exclude_columns: Optional[List[str]] = None
    key_columns: Optional[List[str]] = None
    database: str = "Redis"
    flag_columns: bool = True
    headers: dict = None


class AllRequestPost(BaseModel):
    url: str
    database: str = "Redis"
    headers: dict
    data: dict
