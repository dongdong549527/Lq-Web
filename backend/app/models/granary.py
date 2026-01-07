from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.db import Base
from datetime import datetime

class Granary(Base):
    __tablename__ = "granaries"

    id = Column(Integer, primary_key=True, index=True)
    depot_id = Column(Integer, ForeignKey("depots.id"), nullable=False, comment="粮库ID")
    name = Column(String, index=True, nullable=False, comment="粮仓名称")
    last_collected_at = Column(DateTime, nullable=True, comment="最后采集时间")
    collection_status = Column(Integer, default=0, comment="采集状态") # 0: Idle, 1: Collecting

    # Relationships
    depot = relationship("Depot", back_populates="granaries")
    config = relationship("GranaryConfig", uselist=False, back_populates="granary", cascade="all, delete-orphan")
    info = relationship("GranaryInfo", uselist=False, back_populates="granary", cascade="all, delete-orphan")
    data_records = relationship("GranaryData", back_populates="granary", cascade="all, delete-orphan")

class GranaryConfig(Base):
    __tablename__ = "granary_configs"

    id = Column(Integer, primary_key=True, index=True)
    granary_id = Column(Integer, ForeignKey("granaries.id"), unique=True, nullable=False)
    
    extension_number = Column(Integer, nullable=True, comment="分机号")
    temp_collector_count = Column(Integer, nullable=True, comment="温度采集器数量")
    th_collector_count = Column(Integer, nullable=True, comment="温湿度采集器数量")
    start_index = Column(Integer, nullable=True, comment="起始编号")
    end_index = Column(Integer, nullable=True, comment="结束编号")
    th_index = Column(Integer, nullable=True, comment="温湿度编号")
    cable_count = Column(Integer, nullable=True, comment="电缆根数")
    cable_point_count = Column(Integer, nullable=True, comment="电缆点数")
    total_collector_count = Column(Integer, nullable=True, comment="采集器总数")
    mqtt_topic_sub = Column(String, nullable=True, comment="mqtt接收主题")
    mqtt_topic_pub = Column(String, nullable=True, comment="mqtt发送主题")
    collection_device = Column(Integer, nullable=True, comment="采集设备")

    granary = relationship("Granary", back_populates="config")

class GranaryInfo(Base):
    __tablename__ = "granary_infos"

    id = Column(Integer, primary_key=True, index=True)
    granary_id = Column(Integer, ForeignKey("granaries.id"), unique=True, nullable=False)
    
    manager = Column(String, nullable=True, comment="仓管员")
    design_capacity = Column(Float, nullable=True, comment="设计储量")
    actual_capacity = Column(Float, nullable=True, comment="实际储量")
    storage_nature = Column(String, nullable=True, comment="存储性质")
    variety = Column(String, nullable=True, comment="品种")
    entry_time = Column(DateTime, nullable=True, comment="入仓时间")
    origin = Column(String, nullable=True, comment="产地")
    grade = Column(String, nullable=True, comment="粮食等级")
    rough_rice_yield = Column(Float, nullable=True, comment="出糙率（容重）")
    moisture = Column(Float, nullable=True, comment="水分")
    remark = Column(Text, nullable=True, comment="备注")

    granary = relationship("Granary", back_populates="info")

class GranaryData(Base):
    __tablename__ = "granary_data"

    id = Column(Integer, primary_key=True, index=True)
    granary_id = Column(Integer, ForeignKey("granaries.id"), nullable=False)
    
    collected_at = Column(DateTime, default=datetime.utcnow, comment="采集时间")
    sequence_number = Column(Integer, nullable=True, comment="编号")
    temperature_values = Column(JSON, nullable=True, comment="温度值")
    humidity_values = Column(Float, nullable=True, comment="温湿度值") 

    granary = relationship("Granary", back_populates="data_records")
