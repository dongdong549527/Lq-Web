from pydantic import BaseModel
from typing import List, Optional

class DepotBase(BaseModel):
    name: str
    location: Optional[str] = None

class DepotCreate(DepotBase):
    pass

class DepotResponse(DepotBase):
    id: int
    
    class Config:
        from_attributes = True
