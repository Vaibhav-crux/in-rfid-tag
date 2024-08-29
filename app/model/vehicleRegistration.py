from sqlalchemy import Column, String, DateTime, Text, Enum
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


# Step 3: Define the InternalRFID Model
class VehicleRegistration(Base):
    __tablename__ = "vehicle_registration"

    id = Column(MySQLBinary(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    rfidTag = Column(String(255), nullable=False)
    typeOfVehicle = Column(MySQLEnum(VehicleTypeEnum), nullable=False)  # Using MySQL ENUM
    vehicleNumber = Column(String(100), nullable=False)
    doNumber = Column(String(100), nullable=True)
    transporter = Column(String(255), nullable=True)
    driverOwner = Column(String(255), nullable=True)
    weighbridgeNo = Column(String(100), nullable=True)
    visitPurpose = Column(String(255), nullable=True)
    placeToVisit = Column(String(255), nullable=True)
    personToVisit = Column(String(255), nullable=True)
    validityTill = Column(String(255), nullable=True)
    section = Column(String(255), nullable=True)
    
    # New Fields
    registerDate = Column(Text, nullable=False)  
    registerTime = Column(Text, nullable=False)
    user = Column(String(255), nullable=True)
    shift = Column(String(100), nullable=True)
    loading = Column(Text, nullable=True)  
    
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(VehicleRegistration, self).__init__(**kwargs)
        if isinstance(self.id, uuid.UUID):
            self.id = self.id.bytes
