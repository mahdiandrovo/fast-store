from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from product_service.db.session import get_db
from product_service.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from product_service.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

DatabaseSession = Annotated[AsyncSession, Depends(get_db)]

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_data: ProductCreate,
    db: DatabaseSession,
):
    service = ProductService(db)
    return await service.create_product(product_data)

@router.get(
    "/",
    response_model=list[ProductResponse],
)
async def get_products(
    db: DatabaseSession,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
):
    service = ProductService(db)
    return await service.get_products(skip=skip, limit=limit)

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
async def get_product(
    product_id: int,
    db: DatabaseSession,
):
    service = ProductService(db)
    return await service.get_product(product_id)

@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: DatabaseSession,
):
    service = ProductService(db)
    return await service.update_product(product_id, product_data)

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    product_id: int,
    db: DatabaseSession,
):
    service = ProductService(db)
    await service.delete_product(product_id)