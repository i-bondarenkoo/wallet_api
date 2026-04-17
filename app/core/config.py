from pydantic_settings import BaseSettings
from pydantic import BaseModel


class ServerRunCfg(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://user:password@localhost:5439/demo_wallet"
    db_echo: bool = True
    # db_echo: bool = False
    server_run_cfg: ServerRunCfg = ServerRunCfg()


settings = Settings()
