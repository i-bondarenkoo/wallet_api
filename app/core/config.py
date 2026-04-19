from pydantic_settings import BaseSettings
from pydantic import BaseModel


class ServerRunCfg(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True
    api_version: str = "/api/v1/wallets"


class Settings(BaseSettings):
    test_db_url: str = (
        "postgresql+asyncpg://test123:test123@localhost:5438/test_demo_wallet"
    )
    db_url: str = "postgresql+asyncpg://user:password@localhost:5439/demo_wallet"
    db_echo: bool = True
    # db_echo: bool = False
    server_run_cfg: ServerRunCfg = ServerRunCfg()


settings = Settings()
