from fastapi import FastAPI
from app.api.vault_api import router as vault_router

app = FastAPI(title="Vault Key Management")

# Mount Vault router
app.include_router(vault_router, prefix="/vault", tags=["Vault"])
