from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import uuid


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    article_id: int


class CommentUpdate(CommentBase):
    pass


class CommentRead(CommentBase):
    id: int
    content: str
    created_at: datetime
    author_id: uuid.UUID
    article_id: int

    class Config:

        from_attributes = True
