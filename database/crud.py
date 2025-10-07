from sqlalchemy import create_engine, and_
from sqlalchemy.orm import Session
from config.settings import settings
from database.models import SparePart, Base
from datetime import datetime
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import Session

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        return Session(bind=self.engine)
    
    def get_active_parts(self, sync_period: int = None):
        session = self.get_session()
        try:
            query = session.query(SparePart).filter(SparePart.is_active == True)
            if sync_period:
                query = query.filter(SparePart.sync_period == sync_period)
            return query.all()
        finally:
            session.close()
    
    def update_spare_parts(self, current_parts: list, sync_period: int):
        session = self.get_session()
        try:
            existing_parts = session.query(SparePart).filter(
                SparePart.sync_period == sync_period
            ).all()
            
            existing_codes = {part.spare_code for part in existing_parts}
            current_codes = {part['spareCode'] for part in current_parts}
            
            deleted_codes = existing_codes - current_codes
            for code in deleted_codes:
                part = session.query(SparePart).filter(
                    SparePart.spare_code == code,
                    SparePart.sync_period == sync_period
                ).first()
                if part:
                    part.is_active = False
                    part.last_sync_at = datetime.utcnow()
            
            for part_data in current_parts:
                existing_part = session.query(SparePart).filter(
                    SparePart.spare_code == part_data['spareCode'],
                    SparePart.sync_period == sync_period
                ).first()
                
                if existing_part:
                    existing_part.spare_name = part_data['spareName']
                    existing_part.spare_description = part_data['spareDescription']
                    existing_part.spare_type = part_data['spareType']
                    existing_part.spare_status = part_data['spareStatus']
                    existing_part.price = part_data['price']
                    existing_part.quantity = part_data['quantity']
                    existing_part.updated_at = datetime.fromisoformat(part_data['updatedAt'].replace('Z', '+00:00'))
                    existing_part.is_active = True
                    existing_part.last_sync_at = datetime.utcnow()
                else:
                    new_part = SparePart(
                        spare_code=part_data['spareCode'],
                        spare_name=part_data['spareName'],
                        spare_description=part_data['spareDescription'],
                        spare_type=part_data['spareType'],
                        spare_status=part_data['spareStatus'],
                        price=part_data['price'],
                        quantity=part_data['quantity'],
                        updated_at=datetime.fromisoformat(part_data['updatedAt'].replace('Z', '+00:00')),
                        sync_period=sync_period,
                        is_active=True,
                        last_sync_at=datetime.utcnow()
                    )
                    session.add(new_part)
            
            session.commit()
            return len(current_parts)
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_parts_for_report(self, sync_period: int = None):
        session = self.get_session()
        try:
            query = session.query(SparePart).filter(SparePart.is_active == True)
            if sync_period:
                query = query.filter(SparePart.sync_period == sync_period)
            
            all_parts = query.all()
            
            def numeric_key(part):
                try:
                    return int(part.spare_code.split('-')[1])
                except (IndexError, ValueError):
                    return 0
            
            return sorted(all_parts, key=numeric_key)
            
        finally:
            session.close()