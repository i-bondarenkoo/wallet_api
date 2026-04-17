import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, select
from app.database.models.wallet import Wallet
from app.schemas.wallet import WalletOperationSchema, OperationType


async def get_wallet_by_id_crud(wallet_uuid: uuid.UUID, session: AsyncSession):
    return await session.get(Wallet, wallet_uuid)


async def get_all_wallet_id_crud(session: AsyncSession):
    stmt = select(Wallet).order_by(Wallet.created_at)
    result: Result = await session.execute(stmt)
    wallets: list = result.scalars().all()
    return wallets


async def edit_wallet_balance_crud(
    wallet_uuid: uuid.UUID,
    data_in: WalletOperationSchema,
    session: AsyncSession,
):
    stmt = (
        select(Wallet.id, Wallet.balance)
        .where(Wallet.id == wallet_uuid)
        .with_for_update()
    )
    result: Result = await session.execute(stmt)
    current_wallet = result.scalars().one_or_none()
    if current_wallet is None:
        return None
    if data_in.operation_type == OperationType.DEPOSIT:
        current_wallet.balance += data_in.amount
    elif data_in.operation_type == OperationType.WITHDRAW:
        if current_wallet.balance - data_in.amount < 0:
            return False
        current_wallet.balance -= data_in.amount
    await session.commit()
    await session.refresh
    return current_wallet
