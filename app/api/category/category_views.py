from fastapi import Depends, APIRouter, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.db import AsyncSessionDep,get_session
from app.api.login.userManager import CurrentActiveUser
from .CategoryCRUD import CategoryCRUD
from .schema import CategoryOut, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Category"])

@router.post("/", response_model=CategoryOut)
async def create_category(category_in: CategoryCreate, session: AsyncSessionDep,user: CurrentActiveUser=None):
    return await CategoryCRUD.create(session, category_in)

@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(category_id: int, session: AsyncSessionDep, user: CurrentActiveUser=None):
    category = await CategoryCRUD.get(session, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/", response_model=list[CategoryOut])
async def list_categories(skip: int = 0, limit: int = 100,session: AsyncSession=Depends(get_session), user: CurrentActiveUser=None):
    return await CategoryCRUD.list(session, skip, limit)

@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(category_id: int, category_in: CategoryUpdate, session: AsyncSessionDep, user: CurrentActiveUser=None):
    category = await CategoryCRUD.update(session, category_id, category_in)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}", response_model=dict)
async def delete_category(category_id: int, session: AsyncSessionDep,user: CurrentActiveUser=None):

    success = await CategoryCRUD.delete(session, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"ok": True}