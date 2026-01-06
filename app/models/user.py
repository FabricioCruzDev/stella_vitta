from sqlalchemy import Column, String, ForeignKey, Numeric, Boolean, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class UserType(Base):
    __tablename__ = "user_type"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    user = relationship("User", back_populates="user_type")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="retail")
    user_type_id = Column(Integer, ForeignKey("user_type.id"), nullable=False)

    user_type = relationship("UserType", back_populates="user")