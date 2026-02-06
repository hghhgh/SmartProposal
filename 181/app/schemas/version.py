# app/schemas/version.py
from pydantic import BaseModel, Field

class PackageVersion(BaseModel):
    name: str = Field(..., example="fastapi")
    version: str = Field(..., example="0.95.1")
