from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DepotBase(BaseModel):
    name: str
    address: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    province: Optional[str] = None

class DepotCreate(DepotBase):
    pass

class DepotUpdate(DepotBase):
    pass

class DepotResponse(DepotBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
