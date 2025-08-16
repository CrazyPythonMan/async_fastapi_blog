from fastapi import APIRouter
from  .login.login_view import app as diy_login
from .category.category_views import router as category_router
from .article.article_view import router as article_router
from .comment.comment_view import router as comment_router
from .like.like_view import router as like_router
router = APIRouter()
router.include_router(diy_login)
router.include_router(category_router)
router.include_router(article_router)
router.include_router(comment_router)
router.include_router(like_router)

