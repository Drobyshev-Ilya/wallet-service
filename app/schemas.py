from pydantic import BaseModel, UUID4, condecimal, ConfigDict
from decimal import Decimal
from enum import Enum
from typing import Optional
from datetime import datetime

class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

class Operation(BaseModel):
    operation_type: str
    amount: float

class WalletOperation(BaseModel):
    operation_type: OperationType
    amount: condecimal(ge=Decimal('0.01'), decimal_places=2)

class WalletResponse(BaseModel):
    id: UUID4
    balance: Decimal
    updated_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
