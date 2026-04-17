from app.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy import Integer, DateTime, UUID
from datetime import datetime
from sqlalchemy import func


class Wallet(Base):
    __tablename__ = "wallets"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    balance: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, server_default=func.now()
    )
