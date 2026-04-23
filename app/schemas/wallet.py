from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
import uuid
from enum import Enum


class CreateWalletSchema(BaseModel):
    balance: int = Field(gt=0)


class ResponseBalanceForWalletSchema(CreateWalletSchema):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class ResponseWalletSchema(CreateWalletSchema):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResponseWalletIds(BaseModel):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletOperationSchema(BaseModel):
    operation_type: OperationType
    amount: int = Field(gt=0)
