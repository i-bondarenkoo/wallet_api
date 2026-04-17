from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid


class CreateWalletSchema(BaseModel):
    balance: int


class ResponseWalletSchema(CreateWalletSchema):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
