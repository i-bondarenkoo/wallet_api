from fastapi import APIRouter, Path, Depends, HTTPException, status, Body
from app.core.config import settings
from app.crud.wallet import (
    get_wallet_by_id_crud,
    get_all_wallet_id_crud,
    edit_wallet_balance_crud,
)

from app.schemas.wallet import (
    ResponseWalletSchema,
    ResponseWalletIds,
    WalletOperationSchema,
    ResponseBalanceForWalletSchema,
)
from typing import Annotated
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_constructor import db_constructor

router = APIRouter(
    prefix=settings.server_run_cfg.api_version,
    tags=["Wallets"],
)


# тут по хорошему добавить limit/offset но в задании не указано, и в тестовых данных не так много объектов
@router.get("/all_ids", response_model=list[ResponseWalletIds])
async def get_all_wallet_id(
    session: AsyncSession = Depends(db_constructor.get_session),
):
    return await get_all_wallet_id_crud(session=session)


@router.get(
    "/{wallet_uuid}",
    response_model=ResponseBalanceForWalletSchema,
)
async def get_wallet_by_id(
    wallet_uuid: Annotated[uuid.UUID, Path(description="Идентификатор кошелька")],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    current_wallet = await get_wallet_by_id_crud(
        wallet_uuid=wallet_uuid,
        session=session,
    )
    if current_wallet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet for this uuid was not found",
        )
    return current_wallet


@router.post("/{wallet_uuid}/operation", response_model=ResponseWalletSchema)
async def edit_wallet_balance(
    wallet_uuid: Annotated[uuid.UUID, Path(description="Идентификатор кошелька")],
    data_in: Annotated[
        WalletOperationSchema, Body(description="Даные для выполнения операции")
    ],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    current_wallet = await edit_wallet_balance_crud(
        data_in=data_in, session=session, wallet_uuid=wallet_uuid
    )
    if current_wallet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet for this uuid was not found",
        )
    elif not current_wallet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough money in the balance",
        )
    return current_wallet
