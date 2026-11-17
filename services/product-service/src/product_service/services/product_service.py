from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from product_service.models.product import Product
from product_service.repositories.product_repository import ProductRepository
from product_service.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, db: AsyncSession):
        self.repository = ProductRepository(db)
        self.db = db

    async def create_product(self, product_data: ProductCreate) -> Product:
        existing_product = await self.repository.get_by_sku(product_data.sku)

        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A product with this SKU already exists",
            )

        product = await self.repository.create(
            product_data.model_dump()
        )

        await self.db.commit()

        return product

    async def get_product(self, product_id: int) -> Product:
        product = await self.repository.get_by_id(product_id)

        if not product or not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        return product

    async def get_products(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Product]:
        return await self.repository.get_all(
            skip=skip,
            limit=limit,
        )

    async def update_product(
        self,
        product_id: int,
        update_data: ProductUpdate,
    ) -> Product:
        product = await self.get_product(product_id)

        changes = update_data.model_dump(exclude_unset=True)

        if not changes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No update data provided",
            )

        # Only description is allowed to be explicitly null.
        for field, value in changes.items():
            if value is None and field != "description":
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"{field} cannot be null",
                )

        # Check SKU uniqueness if the SKU is being changed.
        if "sku" in changes and changes["sku"] != product.sku:
            existing_product = await self.repository.get_by_sku(
                changes["sku"]
            )

            if existing_product:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="A product with this SKU already exists",
                )

        updated_product = await self.repository.update(
            product,
            changes,
        )

        await self.db.commit()

        return updated_product

    async def delete_product(self, product_id: int) -> Product:
        product = await self.get_product(product_id)

        deleted_product = await self.repository.delete(product)

        await self.db.commit()

        return deleted_product