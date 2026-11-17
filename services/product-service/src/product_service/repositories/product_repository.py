from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from product_service.models.product import Product


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, product_data: dict) -> Product:
        product = Product(**product_data)

        self.db.add(product)
        await self.db.flush()
        await self.db.refresh(product)

        return product

    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )

        return result.scalar_one_or_none()

    async def get_by_sku(self, sku: str) -> Product | None:
        result = await self.db.execute(
            select(Product).where(Product.sku == sku)
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Product]:
        result = await self.db.execute(
            select(Product)
            .where(Product.is_active.is_(True))
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def update(
        self,
        product: Product,
        update_data: dict,
    ) -> Product:
        for field, value in update_data.items():
            setattr(product, field, value)

        await self.db.flush()
        await self.db.refresh(product)

        return product

    async def delete(self, product: Product) -> Product:
        product.is_active = False

        await self.db.flush()
        await self.db.refresh(product)

        return product