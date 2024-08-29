from sqlalchemy import Column, String, Enum, DateTime, BINARY, Integer, Float, Text, Boolean  # Import Boolean type
from sqlalchemy.dialects.mysql import ENUM as MySQLEnum, BINARY as MySQLBinary
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum
from datetime import datetime
import uuid

from app.config.db_config import Base

# Step 1: Define the Enum for Vehicle Type
class VehicleTypeEnum(PyEnum):  # Using Python's Enum class
    TCT = "TCT"
    PDV = "PDV"
    TVV = "TVV"
    TOV = "TOV"
    PCT = "PCT"
    TDBEV = "TDBEV"
    SCRAPE = "SCRAPE"

# Step 2: Define the Enum for Barrier Status
class BarrierStatusEnum(PyEnum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

# Step 3: Define the AllotedTags Model
class AllotedTags(Base):
    __tablename__ = "alloted_tags"

    id = Column(MySQLBinary(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    rfidTag = Column(String(255), nullable=False)
    typeOfVehicle = Column(MySQLEnum(VehicleTypeEnum), nullable=False)
    vehicleNumber = Column(String(100), nullable=False)
    regDate = Column(Text, nullable=False)  
    regTime = Column(Text, nullable=False)  
    blacklisted = Column(Boolean, default=False, nullable=False)

    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(AllotedTags, self).__init__(**kwargs)
        if isinstance(self.id, uuid.UUID):
            self.id = self.id.bytes
