from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint
from datetime import datetime

Base = declarative_base()

class SparePart(Base):
    __tablename__ = "spare_parts"
    
    id = Column(Integer, primary_key=True, index=True)
    spare_code = Column(String(50), nullable=False, index=True)
    spare_name = Column(String(255), nullable=False)
    spare_description = Column(Text)
    spare_type = Column(String(50), nullable=False)
    spare_status = Column(String(50), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    sync_period = Column(Integer, nullable=False)
    last_sync_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
__table_args__ = (
    UniqueConstraint('spare_code', 'sync_period', name='uq_spare_sync'),
)