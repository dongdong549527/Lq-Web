from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.db import Base
from datetime import datetime

class Depot(Base):
    __tablename__ = "depots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, comment="粮库名称")
    address = Column(Text, nullable=True, comment="粮库地址")
    contact_person = Column(String, nullable=True, comment="联系人")
    phone = Column(String, nullable=True, comment="电话")
    province = Column(String, nullable=True, comment="省份")
    created_at = Column(DateTime, default=datetime.utcnow, comment="安装时间")

    # Relationships
    granaries = relationship("Granary", back_populates="depot", cascade="all, delete-orphan")
    users = relationship("User", back_populates="depot")
