import pytest
import asyncio
from app.database.models.wallet import Wallet
from sqlalchemy import select
from app.database.db_constructor import test_db_constructor


@pytest.mark.asyncio
async def test_get_wallet_by_id(
    client,
    create_wallet,
):
    response = await client.get(
        f"/api/v1/wallets/{create_wallet.id}",
    )
    assert response.status_code == 200
    data: dict = response.json()
    assert data["id"] == str(create_wallet.id)
    assert data["balance"] == create_wallet.balance


@pytest.mark.asyncio
async def test_get_wallet_by_id_false(
    client,
    create_wallet,
):
    response = await client.get(
        f"/api/v1/wallets/{'77ad66ce-a9cb-44e5-a7a2-0920e5901ec5'}",
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_withdraw_balance(
    client,
    create_wallet,
    make_data_withdraw,
):
    list_operations: list = []
    for _ in range(5):
        task = client.post(
            f"/api/v1/wallets/{create_wallet.id}/operation",
            json=make_data_withdraw.model_dump(),
        )
        list_operations.append(task)
    responses = await asyncio.gather(*list_operations)
    for r in responses:
        r.json()
        assert r.status_code == 200
    async with test_db_constructor.session_factory() as session:
        stmt = select(Wallet).where(Wallet.id == create_wallet.id)
        result = await session.execute(stmt)
        row_db = result.scalars().first()
        assert row_db.balance == 0


@pytest.mark.asyncio
async def test_mix_balance(
    client,
    create_wallet,
    make_data_withdraw,
    make_data_deposit,
):
    list_operations: list = []
    for _ in range(3):
        task = client.post(
            f"/api/v1/wallets/{create_wallet.id}/operation",
            json=make_data_withdraw.model_dump(),
        )
        list_operations.append(task)
    for _ in range(2):
        task = client.post(
            f"/api/v1/wallets/{create_wallet.id}/operation",
            json=make_data_deposit.model_dump(),
        )
        list_operations.append(task)
    responses = await asyncio.gather(*list_operations)
    for r in responses:
        r.json()
        assert r.status_code == 200
    async with test_db_constructor.session_factory() as session:
        stmt = select(Wallet).where(Wallet.id == create_wallet.id)
        result = await session.execute(stmt)
        row_db = result.scalars().first()
        assert row_db.balance == create_wallet.balance - (
            make_data_withdraw.amount * 3
        ) + (make_data_deposit.amount * 2)


@pytest.mark.asyncio
async def test_zero_balance(
    client,
    create_wallet2,
    make_data_withdraw,
):

    response = await client.post(
        f"/api/v1/wallets/{create_wallet2.id}/operation",
        json=make_data_withdraw.model_dump(),
    )

    assert response.status_code == 400
    error_data = response.json()
    assert "detail" in error_data
    assert error_data["detail"] == "Not enough money in the balance"
