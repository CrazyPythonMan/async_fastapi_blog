from fastapi import APIRouter, Depends, HTTPException, status

from app.models.db import AsyncSessionDep
from app.api.login.userManager import CurrentActiveUser
from app.api.comment.commentCRUD import CommentCRUD
from app.api.comment.schema import CommentCreate, CommentUpdate, CommentRead


router = APIRouter(prefix="/comments", tags=["comment"])


@router.post("/", response_model=CommentRead)
async def create_comment(
    comment_in: CommentCreate,
    session: AsyncSessionDep,
    user: CurrentActiveUser
):
    return await CommentCRUD.create(session, comment_in, author_id=user.id)


@router.get("/{comment_id}", response_model=CommentRead)
async def get_comment(comment_id: int, session: AsyncSessionDep):
    comment = await CommentCRUD.get_by_id(session, comment_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="评论不存在")
    return comment


@router.put("/{comment_id}", response_model=CommentRead)
async def update_comment(
    comment_id: int,
    comment_in: CommentUpdate,
    session: AsyncSessionDep,
    user: CurrentActiveUser
):
    comment = await CommentCRUD.get_by_id(session, comment_id)
    if comment.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权修改别人的评论")
    return await CommentCRUD.update(session, comment_id, comment_in)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    session: AsyncSessionDep,
    user: CurrentActiveUser
):
    comment = await CommentCRUD.get_by_id(session, comment_id)
    if comment.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="无权删除别人的评论")
    await CommentCRUD.delete(session, comment_id)
    return {"detail": "评论删除成功"}


@router.get("/article/{article_id}", response_model=list[CommentRead])
async def list_comments(article_id: int, session: AsyncSessionDep):
    return await CommentCRUD.list_by_article(session, article_id)
