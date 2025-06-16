from pydantic import BaseModel
from typing import Optional


class AssetBase(BaseModel):
    name: str
    amount: float
    type: str

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[str] = None

class AssetRead(AssetBase):
    id: int

    class Config:
        orm_mode = True