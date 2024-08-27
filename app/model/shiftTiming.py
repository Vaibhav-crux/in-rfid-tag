from sqlalchemy import Column, String, Time, DateTime
from sqlalchemy.dialects.mysql import BINARY as MySQLBinary
from datetime import datetime
import uuid
from app.config.db_config import Base


# Step 2: Define the Model
class ShiftTiming(Base):
    __tablename__ = "shift_timing"

    id = Column(MySQLBinary(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    shift_name = Column(String(50), nullable=False, unique=True)
    from_time = Column(Time, nullable=False)
    to_time = Column(Time, nullable=False)

    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(ShiftTiming, self).__init__(**kwargs)
        if isinstance(self.id, uuid.UUID):
            self.id = self.id.bytes
