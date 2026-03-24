import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.core.database import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(String, unique=True, index=True)
    access_token = Column(String)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
