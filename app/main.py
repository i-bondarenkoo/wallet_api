from fastapi import FastAPI
import uvicorn
from app.core.config import settings

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.server_run_cfg.host,
        port=settings.server_run_cfg.port,
        reload=settings.server_run_cfg.reload,
    )
