from sqlalchemy import Column, String, Enum, Integer, DateTime, Text
from sqlalchemy.dialects.mysql import ENUM as MySQLEnum, BINARY as MySQLBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
import uuid

from app.config.db_config import Base


# Step 2: Define the Model
class DeleteRifdRecord(Base):
    __tablename__ = "delete_rfid_record"

    id = Column(MySQLBinary(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    username = Column(String(255), nullable=False)
    permission = Column(Text, nullable=False)
    rfidTag = Column(String(255), nullable=False)
    vehicleNumber = Column(String(100), nullable=False)

    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(DeleteRifdRecord, self).__init__(**kwargs)
        if isinstance(self.id, uuid.UUID):
            self.id = self.id.bytes
