
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InventoryCreate(BaseModel):
    product_id: int = Field(gt=0)
    available_quantity: int = Field(default=0, ge=0)
    reserved_quantity: int = Field(default=0, ge=0)


class InventoryResponse(BaseModel):
    id: int
    product_id: int
    available_quantity: int
    reserved_quantity: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StockOperationRequest(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)