from pydantic import BaseModel


class LikeIn(BaseModel):
    article_id: int


class LikeOut(BaseModel):
    article_id: int
    likes_count: int
    is_liked: bool
