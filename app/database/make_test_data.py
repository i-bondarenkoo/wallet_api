import asyncio
from app.database.models.wallet import Wallet
from app.database.db_constructor import db_constructor


async def make_test_data():
    async with db_constructor.session_factory() as session:
        wallet1 = Wallet(
            balance=1500,
        )
        wallet2 = Wallet(
            balance=0,
        )
        wallet3 = Wallet(
            balance=5000,
        )
        session.add_all(
            [
                wallet1,
                wallet2,
                wallet3,
            ]
        )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(make_test_data())
