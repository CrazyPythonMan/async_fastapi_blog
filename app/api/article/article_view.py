from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.login.userManager import CurrentActiveUser
from app.api.article.schema import ArticleCreate, ArticleUpdate, ArticleOut
from app.api.article.articleCRUD import ArticleCRUD
from app.models.db import AsyncSessionDep, get_session
from app.models.tables import Article
from fastapi_users import models as user_model

router = APIRouter(prefix="/articles", tags=["articles"])


@router.post("/", response_model=ArticleOut)
async def create_article(
        article_in: ArticleCreate,
        session: AsyncSessionDep, user: CurrentActiveUser = None
):
    return await ArticleCRUD.create(session, article_in, author_id=user.id)


@router.get("/{article_id}", response_model=ArticleOut)
async def get_article(
        article_id: int,
        session: AsyncSessionDep, user: CurrentActiveUser = None
):
    article = await ArticleCRUD.get(session, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.get("/", response_model=List[ArticleOut])
async def list_articles(
        skip: int = 0,
        limit: int = 20,
        session: AsyncSession = Depends(get_session), user: CurrentActiveUser = None
):
    return await ArticleCRUD.list(session, skip, limit)


@router.put("/{article_id}", response_model=ArticleOut)
async def update_article(
        article_id: int,
        article_in: ArticleUpdate,
        session: AsyncSessionDep, user: CurrentActiveUser = None
):
    article = await ArticleCRUD.get(session, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return await ArticleCRUD.update(session, article, article_in)


@router.delete("/{article_id}", response_model=dict)
async def delete_article(
        article_id: int,
        session: AsyncSessionDep, user: CurrentActiveUser = None
):
    article = await ArticleCRUD.get(session, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await ArticleCRUD.delete(session, article)
    return {"detail": "Article deleted"}
