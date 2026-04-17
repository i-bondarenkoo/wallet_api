from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid


class CreateWalletSchema(BaseModel):
    balance: int


class ResponseBalanceForWalletSchema(CreateWalletSchema):
    model_config = ConfigDict(from_attributes=True)


class ResponseWalletSchema(CreateWalletSchema):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResponseWalletIds(BaseModel):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
