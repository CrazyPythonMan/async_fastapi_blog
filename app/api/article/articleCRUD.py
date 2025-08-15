from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models.tables import Article, Tag, article_tag_table
from app.api.article.schema import ArticleCreate, ArticleUpdate

class ArticleCRUD:

    @staticmethod
    async def create(session: AsyncSession, article_in: ArticleCreate, author_id):
        article = Article(
            title=article_in.title,
            content=article_in.content,
            category_id=article_in.category_id,
            author_id=author_id
        )
        session.add(article)
        await session.flush()  # 获取 article.id

        # 处理 tags
        if article_in.tag_ids:
            result = await session.execute(select(Tag).where(Tag.id.in_(article_in.tag_ids)))
            tags = result.scalars().all()
            article.tags = tags

        await session.commit()
        await session.refresh(article)
        return article

    @staticmethod
    async def get(session: AsyncSession, article_id: int) -> Optional[Article]:
        result = await session.execute(select(Article).where(Article.id == article_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def list(session: AsyncSession, skip: int = 0, limit: int = 20) -> List[Article]:
        result = await session.execute(select(Article).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def update(session: AsyncSession, article: Article, article_in: ArticleUpdate):
        for field, value in article_in.dict(exclude_unset=True).items():
            if field == "tag_ids" and value is not None:
                result = await session.execute(select(Tag).where(Tag.id.in_(value)))
                article.tags = result.scalars().all()
            else:
                setattr(article, field, value)
        await session.commit()
        await session.refresh(article)
        return article

    @staticmethod
    async def delete(session: AsyncSession, article: Article):
        await session.delete(article)
        await session.commit()
