
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_service.repositories.inventory_repository import (
    InventoryRepository,
)
from inventory_service.schemas.inventory import InventoryCreate
from inventory_service.core.exceptions import (
    InsufficientAvailableStockError,
    InsufficientReservedStockError,
    InventoryAlreadyExistsError,
    InventoryNotFoundError,
)


class InventoryService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = InventoryRepository(db)

    async def create_inventory(
        self,
        inventory_data: InventoryCreate,
    ):
        # Check whether inventory already exists for this product
        existing_inventory = await self.repository.get_by_product_id(
            inventory_data.product_id
        )

        if existing_inventory:
            raise InventoryAlreadyExistsError(
                "Inventory already exists for this product"
            )

        try:
            inventory = await self.repository.create(
                inventory_data.model_dump()
            )

            await self.db.commit()

            return inventory

        except IntegrityError:
            await self.db.rollback()
            raise ValueError(
                "Inventory already exists for this product."
            )

        except Exception:
            await self.db.rollback()
            raise

    async def get_inventory_by_id(self, inventory_id: int):
        return await self.repository.get_by_id(inventory_id)

    async def get_inventory_by_product_id(self, product_id: int):
        return await self.repository.get_by_product_id(product_id)

    async def get_all_inventory(
        self,
        skip: int = 0,
        limit: int = 100,
    ):
        return await self.repository.get_all(
            skip=skip,
            limit=limit,
        )

    
    async def reserve_stock(
        self,
        product_id: int,
        quantity: int,
    ):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        try:
            inventory = await self.repository.get_by_product_id_for_update(
                product_id
            )

            if inventory is None:
                raise InventoryNotFoundError("Inventory not found")

            if inventory.available_quantity < quantity:
                raise InsufficientAvailableStockError("Insufficient available stock")

            inventory.available_quantity -= quantity
            inventory.reserved_quantity += quantity

            await self.db.commit()
            await self.db.refresh(inventory)

            return inventory

        except Exception:
            await self.db.rollback()
            raise

    async def release_stock(
        self,
        product_id: int,
        quantity: int,
    ):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        try:
            inventory = await self.repository.get_by_product_id_for_update(
                product_id
            )

            if inventory is None:
                raise InventoryNotFoundError("Inventory not found")

            if inventory.reserved_quantity < quantity:
                raise InsufficientReservedStockError("Insufficient reserved stock")

            inventory.reserved_quantity -= quantity
            inventory.available_quantity += quantity

            await self.db.commit()
            await self.db.refresh(inventory)

            return inventory

        except Exception:
            await self.db.rollback()
            raise

    
    async def fulfill_stock(
        self,
        product_id: int,
        quantity: int,
    ):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        try:
            inventory = await self.repository.get_by_product_id_for_update(
                product_id
            )

            if inventory is None:
                raise InventoryNotFoundError(
                    "Inventory not found for this product."
                )

            if inventory.reserved_quantity < quantity:
                raise InsufficientReservedStockError(
                    "Insufficient reserved stock."
                )

            inventory.reserved_quantity -= quantity

            await self.db.commit()
            await self.db.refresh(inventory)

            return inventory

        except Exception:
            await self.db.rollback()
            raise


