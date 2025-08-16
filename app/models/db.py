
import logging
from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator

from fastapi import Depends, FastAPI

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.models.base import Base
from app.settings import settings

logger = logging.getLogger(__name__)

async_engine = create_async_engine(
    settings.DB_URI,
    pool_pre_ping=True,
    echo=settings.ECHO_SQL,
)
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    autoflush=False,
    future=True,
    expire_on_commit=False
)

async def get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            logger.exception(e)
            # get_session 里捕获了 SQLAlchemyError 并 logger.exception，但没重新抛出。
            # 如果出错，依赖注入可能会继续使用无效session
            # 这里可以选择重新抛出异常，或者处理后返回一个空的session
            raise
async def create_db_and_tables() -> None:
    """启动时自动创建所有表，适合无迁移方案或首次启动"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI 生命周期管理器，自动初始化数据库结构"""
    try:
        await create_db_and_tables()
        yield
    finally:
        # 这里可加关闭连接等清理逻辑，暂时不需要
        pass


# 此依赖只是用在非User模型的场景,User模型有自己的依赖,此坑踩太深了
AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]
