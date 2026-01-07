from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# GranaryConfig Schemas
class GranaryConfigBase(BaseModel):
    extension_number: Optional[int] = None
    temp_collector_count: Optional[int] = None
    th_collector_count: Optional[int] = None
    start_index: Optional[int] = None
    end_index: Optional[int] = None
    th_index: Optional[int] = None
    cable_count: Optional[int] = None
    cable_point_count: Optional[int] = None
    total_collector_count: Optional[int] = None
    mqtt_topic_sub: Optional[str] = None
    mqtt_topic_pub: Optional[str] = None
    collection_device: Optional[int] = None

class GranaryConfigCreate(GranaryConfigBase):
    pass

class GranaryConfigResponse(GranaryConfigBase):
    id: int
    granary_id: int
    class Config:
        from_attributes = True

# GranaryInfo Schemas
class GranaryInfoBase(BaseModel):
    manager: Optional[str] = None
    design_capacity: Optional[float] = None
    actual_capacity: Optional[float] = None
    storage_nature: Optional[str] = None
    variety: Optional[str] = None
    entry_time: Optional[datetime] = None
    origin: Optional[str] = None
    grade: Optional[str] = None
    rough_rice_yield: Optional[float] = None
    moisture: Optional[float] = None
    remark: Optional[str] = None

class GranaryInfoCreate(GranaryInfoBase):
    pass

class GranaryInfoResponse(GranaryInfoBase):
    id: int
    granary_id: int
    class Config:
        from_attributes = True

# GranaryData Schemas
class GranaryDataBase(BaseModel):
    sequence_number: Optional[int] = None
    temperature_values: Optional[Dict[str, Any]] = None # JSON
    humidity_values: Optional[float] = None

class GranaryDataCreate(GranaryDataBase):
    pass

class GranaryDataResponse(GranaryDataBase):
    id: int
    granary_id: int
    collected_at: datetime
    class Config:
        from_attributes = True

# Granary Schemas
class GranaryBase(BaseModel):
    name: str
    collection_status: int = 0

class GranaryCreate(GranaryBase):
    depot_id: int
    config: Optional[GranaryConfigCreate] = None
    info: Optional[GranaryInfoCreate] = None

class GranaryResponse(GranaryBase):
    id: int
    depot_id: int
    last_collected_at: Optional[datetime] = None
    config: Optional[GranaryConfigResponse] = None
    info: Optional[GranaryInfoResponse] = None
    
    class Config:
        from_attributes = True
