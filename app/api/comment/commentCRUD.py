from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from app.models.tables import Comment
from app.api.comment.schema import CommentCreate, CommentUpdate
import uuid


class CommentCRUD:

    @staticmethod
    async def create(session: AsyncSession, comment_in: CommentCreate, author_id: uuid.UUID) -> Comment:
        comment = Comment(
            content=comment_in.content,
            author_id=author_id,
            article_id=comment_in.article_id
        )
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment

    @staticmethod
    async def get_by_id(session: AsyncSession, comment_id: int) -> Comment:
        result = await session.execute(select(Comment).where(Comment.id == comment_id))
        comment = result.scalars().first()
        if not comment:
            raise NoResultFound(f"Comment {comment_id} not found")
        return comment

    @staticmethod
    async def update(session: AsyncSession, comment_id: int, comment_in: CommentUpdate) -> Comment:
        comment = await CommentCRUD.get_by_id(session, comment_id)
        comment.content = comment_in.content
        await session.commit()
        await session.refresh(comment)
        return comment

    @staticmethod
    async def delete(session: AsyncSession, comment_id: int) -> None:
        comment = await CommentCRUD.get_by_id(session, comment_id)
        await session.delete(comment)
        await session.commit()

    @staticmethod
    async def list_by_article(session: AsyncSession, article_id: int):
        result = await session.execute(
            select(Comment).where(Comment.article_id == article_id).order_by(Comment.created_at.desc())
        )
        return result.scalars().all()
