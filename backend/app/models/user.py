from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False, comment="用户名")
    hashed_password = Column(String, nullable=False, comment="密码")
    email = Column(String, unique=True, index=True, nullable=True, comment="邮箱")
    role = Column(Integer, default=0, comment="权限") # 0: User, 1: Admin
    depot_id = Column(Integer, ForeignKey("depots.id"), nullable=True, comment="粮库ID")
    full_name = Column(String, nullable=True, comment="姓名")
    phone = Column(String, nullable=True, comment="联系电话")
    is_active = Column(Boolean, default=True, comment="是否使用")

    # Relationships
    depot = relationship("Depot", back_populates="users")
