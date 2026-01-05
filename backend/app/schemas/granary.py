from pydantic import BaseModel
from typing import Optional

class GranaryConfigBase(BaseModel):
    temperature_threshold_high: float = 30.0
    temperature_threshold_low: float = 0.0
    humidity_threshold_high: float = 60.0
    warning_enabled: int = 1

class GranaryConfigCreate(GranaryConfigBase):
    pass

class GranaryConfigResponse(GranaryConfigBase):
    id: int
    granary_id: int
    
    class Config:
        from_attributes = True

class GranaryBase(BaseModel):
    name: str
    capacity: float
    current_stock: float = 0.0

class GranaryCreate(GranaryBase):
    depot_id: int
    config: Optional[GranaryConfigCreate] = None

class GranaryResponse(GranaryBase):
    id: int
    depot_id: int
    config: Optional[GranaryConfigResponse] = None

    class Config:
        from_attributes = True
