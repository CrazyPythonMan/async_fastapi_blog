from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.models.db import AsyncSessionDep
from app.api.login.userManager import CurrentActiveUser
from app.api.like.likeCRUD import LikeCRUD
from app.api.like.schema import LikeOut
from app.models.tables import article_like_table

router = APIRouter(prefix="/likes", tags=["like"])


@router.post("/article/{article_id}", response_model=LikeOut)
async def like_article(article_id: int, session: AsyncSessionDep, user: CurrentActiveUser):
    await LikeCRUD.like_article(session, article_id, user.id)
    count = await LikeCRUD.count_likes(session, article_id)
    return {"article_id": article_id, "likes_count": count, "is_liked": True}


@router.delete("/article/{article_id}", response_model=LikeOut)
async def unlike_article(article_id: int, session: AsyncSessionDep, user: CurrentActiveUser):
    await LikeCRUD.unlike_article(session, article_id, user.id)
    count = await LikeCRUD.count_likes(session, article_id)
    return {"article_id": article_id, "likes_count": count, "is_liked": False}


@router.get("/article/{article_id}", response_model=LikeOut)
async def get_article_likes(article_id: int, session: AsyncSessionDep, user: CurrentActiveUser):
    count = await LikeCRUD.count_likes(session, article_id)

    # 判断用户是否点过赞
    result = await session.execute(
        select(article_like_table).where(
            article_like_table.c.article_id == article_id,
            article_like_table.c.user_id == user.id
        )
    )
    is_liked = result.first() is not None
    return {"article_id": article_id, "likes_count": count, "is_liked": is_liked}
