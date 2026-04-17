import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select
from app.database.models.wallet import Wallet


async def get_wallet_by_id_crud(wallet_uuid: uuid.UUID, session: AsyncSession):
    return await session.get(Wallet, wallet_uuid)


async def get_all_wallet_id_crud(session: AsyncSession):
    stmt = select(Wallet).order_by(Wallet.created_at)
    result: Result = await session.execute(stmt)
    wallets: list = result.scalars().all()
    return wallets
