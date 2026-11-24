
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_service.db.session import get_db
from inventory_service.schemas.inventory import (
    InventoryCreate,
    InventoryResponse,
    StockOperationRequest,
)
from inventory_service.services.inventory_service import InventoryService


router = APIRouter()


@router.post(
    "",
    response_model=InventoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_inventory(
    inventory_data: InventoryCreate,
    db: AsyncSession = Depends(get_db),
):
    service = InventoryService(db)

    try:
        return await service.create_inventory(inventory_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[InventoryResponse],
)
async def get_all_inventory(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = InventoryService(db)

    return await service.get_all_inventory(
        skip=skip,
        limit=limit,
    )


@router.get(
    "/product/{product_id}",
    response_model=InventoryResponse,
)
async def get_inventory_by_product_id(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = InventoryService(db)

    inventory = await service.get_inventory_by_product_id(product_id)

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found for this product.",
        )

    return inventory


@router.get(
    "/{inventory_id}",
    response_model=InventoryResponse,
)
async def get_inventory_by_id(
    inventory_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = InventoryService(db)

    inventory = await service.get_inventory_by_id(inventory_id)

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory not found.",
        )

    return inventory


@router.post("/reserve", response_model=InventoryResponse)
async def reserve_stock(
    request: StockOperationRequest,
    db: AsyncSession = Depends(get_db),
):
    service = InventoryService(db)

    try:
        return await service.reserve_stock(
            product_id=request.product_id,
            quantity=request.quantity,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post("/release", response_model=InventoryResponse)
async def release_stock(
    request: StockOperationRequest,
    db: AsyncSession = Depends(get_db),
):
    service = InventoryService(db)

    try:
        return await service.release_stock(
            product_id=request.product_id,
            quantity=request.quantity,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post("/fulfill", response_model=InventoryResponse)
async def fulfill_stock(
    request: StockOperationRequest,
    db: AsyncSession = Depends(get_db),
):
    service = InventoryService(db)

    try:
        return await service.fulfill_stock(
            product_id=request.product_id,
            quantity=request.quantity,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
