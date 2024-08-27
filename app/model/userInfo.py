from sqlalchemy import Column, String, Enum, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import ENUM as MySQLEnum, BINARY as MySQLBinary
from datetime import datetime
from enum import Enum as PyEnum
import uuid

from app.config.db_config import Base

# Step 1: Define the Enum
class AuthTypeEnum(PyEnum):  # Using Python's Enum class
    ADMIN = "Admin"
    USER = "User"

# Step 2: Define the Model
class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(MySQLBinary(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    authType = Column(Enum(AuthTypeEnum), nullable=False)
    empId = Column(String(50), nullable=True)
    fullName = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    desigantion = Column(String(255), nullable=True)
    Address = Column(String(255), nullable=True)
    mobileNumber = Column(String(255), nullable=True)
    organisation = Column(String(255), nullable=True)

    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
