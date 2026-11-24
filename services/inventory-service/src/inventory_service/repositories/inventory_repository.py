
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inventory_service.models.inventory import Inventory


class InventoryRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, inventory_data: dict) -> Inventory:
        inventory = Inventory(**inventory_data)

        self.db.add(inventory)

        await self.db.flush()
        await self.db.refresh(inventory)

        return inventory

    async def get_by_id(self, inventory_id: int) -> Inventory | None:
        statement = select(Inventory).where(
            Inventory.id == inventory_id
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()

    async def get_by_product_id(self, product_id: int) -> Inventory | None:
        statement = select(Inventory).where(
            Inventory.product_id == product_id
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Inventory]:

        statement = (
            select(Inventory)
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(statement)

        return list(result.scalars().all())

    
    async def get_by_product_id_for_update(
        self,
        product_id: int,
    ) -> Inventory | None:
        statement = (
            select(Inventory)
            .where(Inventory.product_id == product_id)
            .with_for_update()
        )

        result = await self.db.execute(statement)

        return result.scalar_one_or_none()