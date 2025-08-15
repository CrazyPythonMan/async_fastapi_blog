from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from app.api.category.schema import CategoryCreate, CategoryUpdate
from app.models.tables import Category, User


class CategoryCRUD:
    @staticmethod
    async def create(session: AsyncSession, category_in: CategoryCreate) -> Category:
        category = Category(**category_in.dict())
        session.add(category)
        try:
            await session.commit()
            await session.refresh(category)
        except IntegrityError:
            await session.rollback()
            raise
        return category

    @staticmethod
    async def get(session: AsyncSession, category_id: int) -> Category | None:
        result = await session.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def list(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Category]:
        result = await session.execute(select(Category).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def update(session: AsyncSession, category_id: int, category_in: CategoryUpdate) -> Category | None:
        category = await CategoryCRUD.get(session, category_id)
        if not category:
            return None
        for key, value in category_in.dict(exclude_unset=True).items():
            setattr(category, key, value)
        session.add(category)
        await session.commit()
        await session.refresh(category)
        return category

    @staticmethod
    async def delete(session: AsyncSession, category_id: int) -> bool:
        category = await CategoryCRUD.get(session, category_id)
        if not category:
            return False
        await session.delete(category)
        await session.commit()
        return True
