from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.core.db import Base

class Granary(Base):
    __tablename__ = "granaries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    depot_id = Column(Integer, ForeignKey("depots.id"), nullable=False)
    capacity = Column(Float, nullable=False, comment="Capacity in tons")
    current_stock = Column(Float, default=0.0)

    # Relationships
    depot = relationship("Depot", back_populates="granaries")
    config = relationship("GranaryConfig", uselist=False, back_populates="granary", cascade="all, delete-orphan")

class GranaryConfig(Base):
    __tablename__ = "granary_configs"

    id = Column(Integer, primary_key=True, index=True)
    granary_id = Column(Integer, ForeignKey("granaries.id"), unique=True, nullable=False)
    
    # Configuration fields
    temperature_threshold_high = Column(Float, default=30.0)
    temperature_threshold_low = Column(Float, default=0.0)
    humidity_threshold_high = Column(Float, default=60.0)
    warning_enabled = Column(Integer, default=1) # 0: False, 1: True (SQLite doesn't have native Boolean)
    
    # Relationships
    granary = relationship("Granary", back_populates="config")
