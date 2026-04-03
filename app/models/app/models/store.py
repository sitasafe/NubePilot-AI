from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base
import datetime

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(String, unique=True, index=True)
    access_token = Column(String)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)