from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class ArticleBase(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = []  # 用于前端传 tag id 列表

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None

class ArticleOut(ArticleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: UUID

    class Config:
        from_attributes = True
