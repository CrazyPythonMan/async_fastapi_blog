from datetime import datetime
from typing import List, Optional
import uuid

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import (
    String, Text, ForeignKey, Table, Column, DateTime
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    - 继承自FastAPI Users的基础用户表
    - FastAPI Users已经实现了大部分用户相关的功能，不做额外修改,后期如果业务需要可以：diy相关逻辑
    - 独立出来使用依赖注入获取用户数据
    """
    pass

# --------------------
# 多对多中间表（文章 - 标签）
# --------------------
article_tag_table = Table(
    "article_tag",
    Base.metadata,
    Column("article_id", ForeignKey("article.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True)
)

# --------------------
# 多对多中间表（文章 - 点赞用户）
# --------------------
article_like_table = Table(
    "article_like",
    Base.metadata,
    Column("article_id", ForeignKey("article.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
)


# 分类表
class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    articles: Mapped[List["Article"]] = relationship(back_populates="category")


# 文章表
class Article(Base):
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id", ondelete="SET NULL"))

    category: Mapped["Category"] = relationship(back_populates="articles")
    tags: Mapped[List["Tag"]] = relationship(secondary=article_tag_table, back_populates="articles")
    comments: Mapped[List["Comment"]] = relationship(back_populates="article", cascade="all, delete-orphan")


# 标签表
class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    articles: Mapped[List["Article"]] = relationship(secondary=article_tag_table, back_populates="tags")


# 评论表
class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    article_id: Mapped[int] = mapped_column(ForeignKey("article.id", ondelete="CASCADE"))

    article: Mapped["Article"] = relationship(back_populates="comments")
