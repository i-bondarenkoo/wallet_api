import pytest
import httpx
import pytest_asyncio
from app.main import app
import asyncio
from app.database.db_constructor import db_constructor, test_db_constructor


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """
    На Windows asyncio по умолчанию использует ProactorEventLoop,
    который ломается с asyncpg.
    Здесь переключаем на SelectorEventLoop.
    """
    if (
        asyncio.get_event_loop_policy().__class__.__name__
        == "WindowsProactorEventLoopPolicy"
    ):
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scrope="function")
async def client():
    transport = httpx.ASGITransport(
        app=app,
    )
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as async_cli:
        yield async_cli


@pytest_asyncio.fixture(scope="function")
async def override_get_session():
    async with test_db_constructor.session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
def setup_test_db_session():
    async def _override_get_session():
        async with test_db_constructor.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

    app.dependency_overrides[db_constructor.get_session] = _override_get_session
    yield
    app.dependency_overrides.clear()
