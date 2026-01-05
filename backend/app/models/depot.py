from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.db import Base

# Association Table for Many-to-Many Relationship between User and Depot
user_depot_association = Table(
    "user_depot_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("depot_id", Integer, ForeignKey("depots.id"), primary_key=True),
)

class Depot(Base):
    __tablename__ = "depots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    location = Column(String, nullable=True)

    # Relationships
    managers = relationship("User", secondary=user_depot_association, back_populates="depots")
    granaries = relationship("Granary", back_populates="depot", cascade="all, delete-orphan")
