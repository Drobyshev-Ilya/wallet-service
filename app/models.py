from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.sql import func
from .database import Base

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(String, primary_key=True)
    balance = Column(Numeric(precision=18, scale=2), default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
