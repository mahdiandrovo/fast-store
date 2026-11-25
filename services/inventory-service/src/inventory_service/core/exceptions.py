
class InventoryNotFoundError(Exception):
    """Raised when an inventory record cannot be found."""


class InventoryAlreadyExistsError(Exception):
    """Raised when inventory already exists for a product."""


class InsufficientAvailableStockError(Exception):
    """Raised when available stock is insufficient."""


class InsufficientReservedStockError(Exception):
    """Raised when reserved stock is insufficient."""