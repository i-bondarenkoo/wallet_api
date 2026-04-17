from fastapi import FastAPI
import uvicorn
from app.core.config import settings
from app.views.wallet import router as wallet_router

app = FastAPI()
app.include_router(wallet_router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.server_run_cfg.host,
        port=settings.server_run_cfg.port,
        reload=settings.server_run_cfg.reload,
    )
