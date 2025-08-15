# import logging
# from contextlib import asynccontextmanager
# from typing import AsyncIterator, Annotated
# from app.models.base import Base
# from fastapi import Depends, FastAPI
# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
# from sqlalchemy.exc import SQLAlchemyError
#
# from app.settings import settings
#
# logger = logging.getLogger(__name__)
#
# class Database:
#     """数据库连接管理类，封装了SQLAlchemy2.0异步引擎和会话管理。"""
#     def __init__(self, db_uri: str, echo: bool = False):
#         self._engine = create_async_engine(
#             db_uri,
#             pool_pre_ping=True,
#             echo=echo,
#             future=True,
#             # 这里可以添加更多连接池相关参数，根据实际需求调整
#         )
#         self._sessionmaker = async_sessionmaker(
#             self._engine,
#             expire_on_commit=False,  # 避免潜在的Session刷新问题
#             autoflush=False,
#             future=True,
#         )
#
#     async def get_session(self) -> AsyncIterator[AsyncSession]:
#         async with self._sessionmaker() as session:
#             try:
#                 yield session
#             except SQLAlchemyError as exc:
#                 logger.error("数据库操作异常", exc_info=exc)
#                 raise  # 保证异常向上传递，FastAPI 能正确处理
#
#     def __call__(self) -> AsyncIterator[AsyncSession]:
#         # 使实例可作为依赖注入调用，简化FastAPI使用
#         return self.get_session()
#
#     async def dispose(self) -> None:
#         # 方便在应用生命周期结束时主动关闭连接池，释放资源
#         await self._engine.dispose()
#
#     async def create_tables(self):
#         async with self._engine.begin() as conn:
#             await conn.run_sync(Base.metadata.create_all)
#         logger.info("Database tables created")
#
#     @asynccontextmanager
#     async def lifespan(self, app: FastAPI):
#         await self.create_tables()
#         yield
#
# # 单例数据库管理对象，便于整个项目共享
# db = Database(settings.DB_URI, settings.ECHO_SQL)
#
# # FastAPI依赖声明，简洁明了
# AsyncSessionDep = Annotated[AsyncSession, Depends(db)]


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
