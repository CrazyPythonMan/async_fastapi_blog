from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, func
from app.models.tables import article_like_table
import uuid


class LikeCRUD:

    @staticmethod
    async def like_article(session: AsyncSession, article_id: int, user_id: uuid.UUID) -> dict:
        # 检查是否已点赞
        result = await session.execute(
            select(article_like_table).where(
                article_like_table.c.article_id == article_id,
                article_like_table.c.user_id == user_id
            )
        )
        if result.first():
            return {"article_id": article_id, "liked": True}  # 已经点过赞

        await session.execute(
            insert(article_like_table).values(article_id=article_id, user_id=user_id)
        )
        await session.commit()
        return {"article_id": article_id, "liked": True}

    @staticmethod
    async def unlike_article(session: AsyncSession, article_id: int, user_id: uuid.UUID) -> dict:
        await session.execute(
            delete(article_like_table).where(
                article_like_table.c.article_id == article_id,
                article_like_table.c.user_id == user_id
            )
        )
        await session.commit()
        return {"article_id": article_id, "liked": False}

    @staticmethod
    async def count_likes(session: AsyncSession, article_id: int) -> int:
        result = await session.execute(
            select(func.count()).select_from(article_like_table).where(
                article_like_table.c.article_id == article_id
            )
        )
        return result.scalar_one()
