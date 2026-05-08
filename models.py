import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from database import Base


class User(Base):
    __tablename__ = "users2"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    otp = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)


class CompanyProfile(Base):
    __tablename__ = "company_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users2.id"), unique=True, nullable=False)
    data = Column(JSON, nullable=False)
    user = relationship("User")